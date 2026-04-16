# Rules YAML Specification — Built-in Stack Rules

## Format Specification

Each stack rule file follows this schema. These ship with Crystal and users can override.

---

## react-python-mongo.yaml

```yaml
# Crystal Guard Rules — React + Python (FastAPI) + MongoDB
# Stack ID: react-python-mongo

meta:
  name: "React + Python + MongoDB"
  description: "Rules for full-stack apps with React frontend, Python/FastAPI backend, and MongoDB"
  version: "1.0.0"
  
detection:
  requires_all:
    - file: "package.json"
      contains: "react"
    - file: "requirements.txt"
      contains_any: ["fastapi", "flask", "django"]
    - file: "requirements.txt"
      contains_any: ["pymongo", "motor", "mongoengine"]

architecture:
  frontend:
    root: "frontend/src"
    expected_dirs:
      - path: "components"
        description: "Reusable UI components"
      - path: "pages"
        description: "Page-level components (routes)"
        optional: true
      - path: "hooks"
        description: "Custom React hooks"
        optional: true
      - path: "utils"
        description: "Frontend utility functions"
        optional: true
    
  backend:
    root: "backend"
    expected_dirs:
      - path: "routes"
        description: "API route handlers"
        optional: true
      - path: "services"
        description: "Business logic"
        optional: true
      - path: "models"
        description: "Data models and schemas"
        optional: true
    
  shared:
    required_files:
      - ".gitignore"
      - "README.md"
    recommended_files:
      - ".env.example"
      - "tests/"
    max_root_files: 12
    max_depth: 6

domain_purity:
  frontend:
    file_patterns: ["frontend/**/*.js", "frontend/**/*.jsx", "frontend/**/*.ts", "frontend/**/*.tsx"]
    forbidden:
      - id: "dom-001"
        pattern: "pymongo|MongoClient|mongoose\\.connect|mongodb://"
        message: "Database access detected in frontend code. Frontend should only communicate with backend via API calls."
        suggestion: "Move database operations to a backend service file and create an API endpoint for the frontend to call."
        severity: "critical"
        
      - id: "dom-002"
        pattern: "import\\s+fs|require\\(['\"]fs['\"]\\)|from\\s+pathlib"
        message: "Filesystem access detected in frontend code. Frontend cannot access the server's filesystem."
        suggestion: "If you need file operations, create a backend API endpoint."
        severity: "critical"
        
      - id: "dom-003"
        pattern: "process\\.env\\.(?!REACT_APP_|NEXT_PUBLIC_|VITE_)"
        message: "Server-side environment variable accessed in frontend. Only REACT_APP_ prefixed variables are available in the browser."
        suggestion: "Rename the variable with REACT_APP_ prefix, or move this logic to the backend."
        severity: "high"
        
      - id: "dom-004"
        pattern: "bcrypt|argon2|jwt\\.sign|jsonwebtoken"
        message: "Authentication/cryptographic operations detected in frontend. These should run on the backend for security."
        suggestion: "Move authentication logic to backend middleware or service."
        severity: "high"

  backend_routes:
    file_patterns: ["backend/routes/**/*.py", "backend/**/router*.py"]
    forbidden:
      - id: "dom-010"
        pattern: "collection\\.find|collection\\.insert|db\\[|\\$match|\\$group"
        message: "Direct database queries in route handler. Routes should delegate to service functions."
        suggestion: "Create a service function in /backend/services/ and call it from the route."
        severity: "medium"
    warnings:
      - id: "dom-011"
        condition: "function_lines > 50"
        message: "Route handler exceeds 50 lines. This likely contains business logic that should be in a service."
        suggestion: "Extract business logic into a service function."
        severity: "medium"

  backend_models:
    file_patterns: ["backend/models/**/*.py"]
    forbidden:
      - id: "dom-020"
        pattern: "Request|Response|HTTPException|@app\\.|@router\\."
        message: "HTTP handling code detected in model file. Models should only define data structures."
        suggestion: "Move HTTP handling to route files."
        severity: "medium"

security:
  global:
    file_patterns: ["**/*.py", "**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx", "**/*.env"]
    checks:
      - id: "sec-001"
        name: "Hardcoded API Key"
        pattern: "(api_key|apiKey|API_KEY|api_secret|apiSecret)\\s*[=:]\\s*[\"'][a-zA-Z0-9_\\-]{16,}"
        message: "Hardcoded API key detected. API keys should be in environment variables, never in code."
        suggestion: "Move this key to your .env file and reference it with os.environ.get('YOUR_KEY_NAME')."
        severity: "critical"
        
      - id: "sec-002"
        name: "Hardcoded Password"
        pattern: "(password|passwd|pwd|secret)\\s*[=:]\\s*[\"'][^\"']{4,}"
        message: "Hardcoded password detected. Passwords should never appear in code."
        suggestion: "Use environment variables for secrets. For user passwords, use bcrypt hashing."
        severity: "critical"
        exclude_files: ["*.test.*", "*.spec.*", "*.example*"]
        
      - id: "sec-003"
        name: "Known API Key Format"
        pattern: "sk-[a-zA-Z0-9]{20,}|pk_(test|live)_[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|AKIA[0-9A-Z]{16}"
        message: "Recognized API key format found in code. This is a significant security risk."
        suggestion: "Remove this key immediately, rotate it, and store in .env file."
        severity: "critical"
        
      - id: "sec-004"
        name: "Exposed Environment File"
        check_type: "gitignore_missing"
        target: ".env"
        message: ".env file is not in .gitignore. Your secrets will be committed to git."
        suggestion: "Add '.env' to your .gitignore file immediately."
        severity: "critical"
        
      - id: "sec-005"
        name: "CORS Wildcard"
        pattern: "allow_origins\\s*=\\s*\\[\\s*[\"']\\*[\"']|cors\\(.*origin.*[\"']\\*[\"']"
        message: "CORS is set to allow all origins (*). This allows any website to make requests to your API."
        suggestion: "Set specific allowed origins instead of wildcard. E.g., allow_origins=['https://yourdomain.com']"
        severity: "high"
        
      - id: "sec-006"
        name: "SQL Injection Vector"
        pattern: "f[\"'].*SELECT.*\\{|[\"'].*SELECT.*[\"']\\s*\\+\\s*"
        message: "Potential SQL injection vulnerability. User input may be directly inserted into SQL query."
        suggestion: "Use parameterized queries or an ORM instead of string formatting for SQL."
        severity: "high"

placeholders:
  global:
    checks:
      - id: "hyg-001"
        pattern: "TODO|FIXME|HACK|XXX"
        message: "Unresolved TODO/FIXME comment found. Complete or remove before deploying."
        severity: "low"
        exclude_files: ["*.md", "CONTRIBUTING*", "CHANGELOG*"]
        
      - id: "hyg-002"
        pattern: "example\\.com|test@test\\.com|lorem ipsum|placeholder"
        message: "Placeholder value detected. Replace with real values before deploying."
        severity: "medium"
        exclude_files: ["*.test.*", "*.spec.*", "*.md"]
        
      - id: "hyg-003"
        pattern: "console\\.log\\(|print\\((?!.*file=)"
        message: "Debug logging statement found. Remove or replace with proper logging before deploying."
        severity: "low"
        exclude_files: ["*.test.*"]
        
      - id: "hyg-004"
        pattern: "localhost:\\d{4}"
        message: "Hardcoded localhost URL found. Use environment variables for URLs."
        severity: "medium"
        exclude_files: [".env", ".env.example", "*.md", "*.test.*"]
```

---

## generic.yaml (Fallback Rules)

```yaml
# Crystal Guard Rules — Generic (fallback for unrecognized stacks)

meta:
  name: "Generic"
  description: "Basic rules that apply to any project"
  version: "1.0.0"

architecture:
  shared:
    required_files:
      - ".gitignore"
    recommended_files:
      - "README.md"
      - ".env.example"
    max_root_files: 15
    max_depth: 7

security:
  global:
    file_patterns: ["**/*"]
    checks:
      - id: "sec-001"
        name: "Hardcoded API Key"
        pattern: "(api_key|apiKey|API_KEY)\\s*[=:]\\s*[\"'][a-zA-Z0-9_\\-]{16,}"
        message: "Hardcoded API key detected. Use environment variables instead."
        severity: "critical"
      - id: "sec-002"
        name: "Hardcoded Password"
        pattern: "(password|passwd|pwd)\\s*[=:]\\s*[\"'][^\"']{4,}"
        message: "Hardcoded password detected. Never put passwords in code."
        severity: "critical"
      - id: "sec-004"
        name: "Exposed Environment File"
        check_type: "gitignore_missing"
        target: ".env"
        message: ".env not in .gitignore."
        severity: "critical"

placeholders:
  global:
    checks:
      - id: "hyg-001"
        pattern: "TODO|FIXME"
        message: "Unresolved TODO/FIXME found."
        severity: "low"
      - id: "hyg-002"
        pattern: "example\\.com|lorem ipsum"
        message: "Placeholder value detected."
        severity: "medium"
```

---

## How Users Override Rules

Users create `.crystal/rules.yaml` in their project:

```yaml
# Override: disable a rule
overrides:
  disabled_rules:
    - "hyg-003"    # We use console.log for our logging strategy
    - "sec-005"    # CORS wildcard is intentional for our public API

# Override: change severity
  severity_overrides:
    "hyg-001": "medium"   # We take TODOs more seriously

# Add custom rules
custom_rules:
  - id: "custom-001"
    name: "No Inline Styles"
    pattern: "style=\\{\\{"
    files: ["**/*.jsx", "**/*.tsx"]
    message: "Use CSS classes instead of inline styles for consistency."
    severity: "low"
    
  - id: "custom-002"
    name: "No Console Errors Ignored"
    pattern: "catch.*\\{\\s*\\}"
    files: ["**/*.js", "**/*.ts"]
    message: "Empty catch block found. At minimum, log the error."
    severity: "medium"
```
