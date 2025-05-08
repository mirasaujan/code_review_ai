# AI Code-Review Assistant  
*Implementation Design Document — v1.0 (May 2025)*  

---

## Table of Contents
1.  Overview  
2.  System Goals & Non-Goals  
3.  High-Level Architecture  
4.  Execution Flow  
5.  Package / Module Specification  
6.  Configuration Files  
7.  Data Models & Schemas  
8.  LLM Integration Details  
9.  CLI Specification & Usage Examples  
10.  Error-Handling & Time-outs  
11.  Packaging, Installation & Runtime Requirements  
12.  Logging, Metrics & Cost Reporting  
13.  Extensibility Road-map  
14.  Open-Source & Licensing Notes  

---

## 1  Overview
The **AI Code-Review Assistant** is a Python-based command-line tool that scans any codebase (any language) and produces a structured JSON report of rule violations, augmented with Large-Language-Model (LLM) reasoning where deterministic matching is insufficient.

*Version 1* emphasises **breadth** (works on "any text file") over language-specific depth; it therefore avoids heavy grammar parsers such as *tree-sitter* and relies on:

*  textual diff parsing, and
*  LLM prompts for semantic analysis.

Future versions can plug in richer language parsers without altering the public API.

---

## 2  System Goals & Non-Goals
| Aspect | Goal | Non-Goal |
|--------|------|----------|
| **Language support** | Accept any source file as plain text. | Perfect AST-aware analysis in v1. |
| **Security / privacy** | Keep credentials out of VCS; user controls keys. | Advanced in-prompt redaction (future). |
| **Automation depth** | Flag issues (`info / warning / error`). | Auto-fix / code‐transform patches. |
| **Deployment** | Local CLI, no network services required (except LLM calls). | CI pipelines, GitHub Checks in v1. |
| **Output** | Single JSON artefact with findings + cost. | SARIF / Markdown (future add-on). |

---

## 3  High-Level Architecture

```mermaid
flowchart LR
    A[CLI] --> B[File & Diff Collector]
    B --> D[Context Builder]
    D --> E[LLM Back-end(OpenAI / Claude / Gemini / local)]
    E --> F[Finding Collector]
    F --> G[Reporter<br>(JSON writer)]

1.  **Collector**  builds the work-set: changed lines, single files, directories or whole repo.
    
2.  **Context Builder** structures the input as JSON with:
    - Full file content
    - Structured change metadata (line numbers, change types)
    - File metadata (path, language)
    - Related context (commit messages, affected files)
    
3.  **LLM Back-end** performs semantic analysis with structured context.
    
4.  **Reporter**  consolidates everything into  `findings.json`, including token usage and cost.
```

### Context Structure Example
```json
{
  "file": "src/main.py",
  "language": "python",
  "changes": {
    "type": "diff",
    "hunks": [
      {
        "start_line": 45,
        "end_line": 46,
        "before": "def old_function():\n    return None",
        "after": "def new_function():\n    return True"
      }
    ]
  },
  "full_content": "... entire file content ..."
}
```

----------

## 4 Execution Flow

1. **Start-up**  – CLI parses flags, loads  `.env`, YAML rule mapping, and user RuleSets.
    
2. **Target resolution**
    
   - `diff <base>..<head>`  → list of modified files & line spans.
        
   - `file`  /  `dir`  /  `full`  → enumerate files recursively (globs honoured).
        
3. **Deterministic scan**  – Regex & heuristic rules applied to each candidate line/block.
    
4. **LLM scan**  – Batches of unresolved snippets sent to model (≤ 15 s request timeout).
    
5. **Finding merge**  – Duplicate suppression, severity assignment (`info|warning|error`).
    
6. **Report write**  –  `findings.json`  saved to  `--out`  (default  `./code_review_findings.json`).
    
7. **Exit**  – Always  `exit 0`  in v1 (no CI semantics).
    

----------

## 5 Package / Module Specification

| Package | Core Classes / Functions | Notes |
|--------|------|----------|
| `codereview.cli` | `app`  (Typer instance), sub-commands (`diff`,  `file`,  `dir`,  `full`) | Thin layer; no business logic. |
| `codereview.collector` | `GitDiff`,  `DirectoryScanner`,  `FileLoader` | Uses  _GitPython_  or subprocess for diffs. |
| `codereview.rules` | `Rule`,  `RuleSet`,  `RuleRegistry`, utilities for regex / simple DSL evaluation | Loads user-authored YAML; validates schema. |
| `codereview.llm` | `BaseBackend`,  `OpenAIBackend`,  `ClaudeBackend`,  `GeminiBackend`,  `LocalBackend`,  `BackendFactory` | Uniform async  `.review(prompt)->FindingsJSON`. |
| `codereview.prompt` | `PromptBuilder` | Formats system & user messages, injects cost guardrails. |
| `codereview.findings` | `Finding`,  `FindingCollector`, de-dup helpers | Frozen dataclass for immutability. |
| `codereview.report` | `JSONWriter` | Emits final artefact & prints summary. |
| `codereview.config` | `EnvLoader`,  `UserConfig` | Reads  `.env`, merges CLI overrides, holds time-out & cost settings. |

----------

## 6 Configuration Files

### 6.1  `.env`

```ini
`OPENAI_API_KEY=... 
ANTHROPIC_API_KEY=... 
GOOGLE_API_KEY=... 
LLAMA_SERVER_URL=http://localhost:11434` 
```
_Ignored by Git._  Users manage their own secrets.

### 6.2  `rules/`  directory structure

```markdown
rules/
 ├─ stdlib/
 │   ├─ prints.yaml
 │   └─ secrets.yaml
 └─ custom/
 └─ my_team_rules.yaml` 
 ```

### 6.3 Sample YAML Schema

```yaml
`# rule file: prints.yaml  
rules:
  - id:  GEN-001  
    name:  Avoid  debug  prints  
    description:  "Debug prints should not be committed."  
    pattern:  "\\bprint\\("  
    severity:  warning  
rule_sets:  
  - name:  default  
    includes:  -  "src/**"  
    excludes:  -  "tests/**"  
    rules:  -  GEN-001` 
```

- End users may add more keys, but  `id`,  `pattern`,  `severity`  are mandatory.
    
- Patterns are treated as raw Python regex strings.
    

----------

## 7 Data Models & Schemas

```python
`# findings.py  
@dataclass(frozen=True) 
class  Finding:
    file: str  # relative path 
    line: int  # 1-based 
    rule_id: str 
    message: str 
    severity: Literal["info", "warning", "error"] 
@dataclass  class  CostSummary:
    provider: str 
    model: str 
    tokens_prompt: int 
    tokens_completion: int 
    cost_usd: float`
``` 

### Output File (`findings.json`)

```jsonc
{
  "version": "1.0",
  "metadata": {
    "timestamp": "2025-05-08T10:15:32Z",
    "mode": "diff",
    "base_ref": "main",
    "head_ref": "feature/xyz",
    "llm": {
      "provider": "openai",
      "model": "gpt-4o",
      "timeout_sec": 15,
      "total_cost_usd": 0.0134
    }
  },
  "findings": [
    {
      "file": "Sources/App/Networking/API.swift",
      "line": 88,
      "rule_id": "GEN-001",
      "severity": "warning",
      "message": "Debug prints should not be committed."
    }
  ]
}
```
----------

## 8 LLM Integration Details

-   **Back-ends shipped**:
    
    -   `openai:gpt-4o`  _(default)_
        
    -   `anthropic:claude-3-haiku`
        
    -   `google:gemini-1.5-pro-latest`
        
    -   `local:llama.cpp`  (HTTP server)
        
-   **Timeout**: 15 s per request (`asyncio.wait_for`).
    
-   **Cost tracking**:
    
    -   Each backend returns  `(prompt_tokens, completion_tokens, cost_usd)`.
        
    -   Aggregated in  `CostSummary`.
        
    -   Printed in CLI footer and saved in report.
        
-   **Prompt format (simplified)**:
    
    ```sql
    
    `system: You are an expert code reviewer. 
    user: 
      <RULES>  
      <CODE_SNIPPET> List any violations in JSON array  with keys:
        file, line, rule_id, message, severity` 
    ```
    
-   **Retries**: Exponential back-off, max 3 attempts on network errors.
    

----------

## 9 CLI Specification

| Command | Example | Meaning |
|--------|------|----------|
| `diff` | `codereview diff main..HEAD` | Review only changed lines. |
| `file` | `codereview file path/to/file.swift` | Single file. |
| `dir` | `codereview dir Sources/` | All files recursively. |
| `full` | `codereview full` | Whole repository. |

### Global flags

| Flag | Default | Description |
|--------|------|----------|
| `--rules-path` | `rules/` | Root folder with YAML rules. |
| `--model` | `openai:gpt-4o` | `<provider>:<model_id>` |
| `--timeout` | `15` | Seconds per LLM request. |
| `--out` | `code_review_findings.json` | Output file. |

----------

## 10 Error-Handling & Time-outs

-   **Collector errors**  (bad Git ref, unreadable file): log and continue.
    
-   **Rule YAML parse error**: abort execution with clear message.
    
-   **LLM timeout**: mark affected snippet with  `"severity": "info", "message": "LLM timeout"`  (不会 abort).
    
-   **Unhandled**  exceptions bubble to CLI, shown with stack-trace (debug).
    

----------

## 11 Packaging & Runtime

-   **Python ≥ 3.12**  enforced by  `pyproject.toml`.
    
-   **Poetry**  for builds;  `poetry install --with cli`.
    
-   **Entry-point**:  `codereview = codereview.cli:app`.
    
-   Distribution under  **MIT license**.
    

### Cross-project compatibility

The script works on any repository—Swift, C#, Bash—because it treats files as opaque text.  
For Swift projects in particular, add to  `Package.swift`  scripts section:

```swift

`// .swiftpm/xcode/scripts/run_code_review.sh 
poetry run codereview diff main..source_branch  --out .build/code_review_findings.json` 
```

----------

## 12 Logging, Metrics & Cost Reporting

-   Uses  **`rich`**  for coloured console logs.
    
-   Levels:  `INFO`  default,  `DEBUG`  via  `--verbose`.
    
-   Cost summary printed like:
    
```bash
── LLM cost ─────────────────────────────
provider/model        $USD    tokens
openai/gpt-4o        0.0134   2 112
``` 

----------

## 13 Extensibility Road-map

| Phase | Feature |
|--------|------|
| **v1.1** | SARIF / Markdown reporters; configurable exit codes. |
| **v2.0** | Optional  _tree-sitter_  language packs for deep static rules. |
| **v2.1** | GitHub / GitLab PR Check integration; annotate diffs. |
| **v3.0** | IDE extensions (VS Code, Xcode source extensions). |
| **v3.1** | Auto-fix suggestions & refactorings (patch hunks). |

----------

## 14 Open-Source & Licensing Notes

 - Core project released under  **MIT**.
    
 - Must vet third-party deps—`gitpython`,  `typer`,  `rich`,  `openai`,  `anthropic`,  `google-generativeai`—to ensure permissive licenses (Apache 2.0 or MIT).
    
 - Users are responsible for accepting respective LLM provider ToS when adding their API keys.