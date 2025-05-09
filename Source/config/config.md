# Configuration Module Documentation

## Overview
The configuration module handles environment variables and user configuration settings for the AI Code-Review Assistant. It consists of two main components:

1. Environment Loading (`env.py`)
2. User Configuration (`user.py`)

## Environment Variables (.env)

The system uses a `.env` file for sensitive configuration that should not be committed to version control:

```ini
OPENAI_API_KEY=... 
ANTHROPIC_API_KEY=... 
GOOGLE_API_KEY=... 
LLAMA_SERVER_URL=http://localhost:11434
```

## User Configuration (codereview.yaml)

The main configuration file `codereview.yaml` supports the following structure:

```yaml
# Repository root configuration
version: "1.0"

# File collection patterns
include:
  - "*.py"
  - "*.js"
  - "*.ts"
  - "*.swift"
exclude:
  - "tests/*"
  - "node_modules/*"
  - "*.test.*"
  - "build/*"
  - "dist/*"

# LLM configuration
llm:
  provider: "openai"  # openai, anthropic, google, local
  model: "gpt-4o"     # provider-specific model
  timeout_sec: 15     # per request timeout

# Rules configuration
rules:
  path: "rules/"      # relative to repository root
  mapping: "rules/ruleset_mapping.json"

# Output configuration
output:
  file: "code_review_findings.json"
  format: "json"      # future: sarif, markdown
```

## Module Components

### env.py
- Loads environment variables from `.env` file
- Validates required API keys
- Provides access to environment-specific settings
- Handles missing or invalid environment variables

### user.py
- Loads and validates `codereview.yaml`
- Merges CLI overrides with configuration
- Manages timeouts and other runtime settings
- Provides configuration access to other modules

## Error Handling

- Missing `.env` file: Warns user but continues with default values
- Invalid YAML: Aborts execution with clear error message
- Missing required API keys: Aborts with helpful setup instructions
- Invalid configuration values: Provides specific validation errors

## Usage Example

```python
from config.env import EnvLoader
from config.user import UserConfig

# Load environment variables
env = EnvLoader()
api_key = env.get_api_key("OPENAI")

# Load user configuration
config = UserConfig("codereview.yaml")
timeout = config.get_llm_timeout()
```

## Security Notes

- `.env` file is ignored by Git
- API keys are never logged or exposed in error messages
- Configuration validation happens before any API calls
- Sensitive values are cleared from memory when possible
