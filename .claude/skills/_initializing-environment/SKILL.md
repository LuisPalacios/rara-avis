---
name: _initializing-environment
description: Internal skill to initialize Python and Node.js environments. Called by other skills before execution. Not user-invokable.
---

# Environment Setup (Internal)

Ensures Python and Node.js virtual environments are ready before running dependent skills.

## Usage

This skill is called internally by other skills. It is NOT user-invokable.

When another skill needs dependencies, call `_initializing-environment` first:

```text
1. Run _initializing-environment checks
2. If checks pass, proceed with the skill
3. If checks fail, show error and exit
```

## Checks Performed

### 1. Python Environment

```bash
# Check Python3 is available
python3 --version

# Check .claude/_tooling/.venv exists, if not create it
if [ ! -d ".claude/_tooling/.venv" ]; then
    python3 -m venv .claude/_tooling/.venv
fi

# Check requirements are installed
.claude/_tooling/.venv/Scripts/pip.exe show Pillow pymupdf > /dev/null 2>&1
if [ $? -ne 0 ]; then
    .claude/_tooling/.venv/Scripts/pip.exe install -r .claude/_tooling/requirements.txt
fi
```

### 2. Node.js Environment

```bash
# Check Node.js is available
node --version

# Check node_modules exists, if not install
if [ ! -d ".claude/_tooling/node_modules" ]; then
    npm install --prefix .claude/_tooling
fi

# Verify key packages exist
if [ ! -f ".claude/_tooling/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs" ]; then
    npm install --prefix .claude/_tooling
fi
```

## Commands (Windows)

### Python Setup

```bash
# Create venv if missing
python -m venv .claude/_tooling/.venv

# Install requirements
.claude/_tooling/.venv\Scripts\pip.exe install -r .claude/_tooling/requirements.txt

# Verify installation
.claude/_tooling/.venv\Scripts\pip.exe show Pillow pymupdf
```

### Node.js Setup

```bash
# Install dependencies
"C:\Program Files\nodejs\npm.cmd" install --prefix .claude

# Verify installation
node .claude/_tooling/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs --help
```

## Exit Conditions

| Condition           | Action                                          |
| ------------------- | ----------------------------------------------- |
| Python3 not found   | Error: "Python3 not installed"                  |
| Node.js not found   | Error: "Node.js not installed"                  |
| venv creation fails | Error: "Failed to create Python venv"           |
| pip install fails   | Error: "Failed to install Python dependencies"  |
| npm install fails   | Error: "Failed to install Node.js dependencies" |
| All checks pass     | Proceed silently                                |

## Behavior

1. **Check Python3**: Verify `python3 --version` or `python --version` works
2. **Check Node.js**: Verify `node --version` works
3. **Setup Python venv**: Create `.claude/_tooling/.venv/` if missing, install `requirements.txt`
4. **Setup Node.js**: Run `npm install --prefix .claude/_tooling` if `.claude/_tooling/node_modules/` missing
5. **Return**: Success or error message

## Dependencies

### Python (`.claude/_tooling/requirements.txt`)

- `Pillow` — Image processing
- `pymupdf` — PDF processing

### Node.js (`.claude/_tooling/package.json`)

- `markdownlint-cli2` — Markdown linting
- `prettier` — Code formatting

## Settings File (`.claude/settings.json`)

**IMPORTANT: Do NOT modify or remove permissions from this file unless explicitly requested by the user.**

The settings file contains pre-configured permissions for the tooling environment:

```json
{
  "permissions": {
    "allow": [
      "Bash(node:*)",
      "Bash(markdownlint-cli2:*)",
      "Bash(prettier:*)",
      "Bash(.claude/_tooling/.venv/Scripts/python.exe:*)",
      "Bash(.claude/_tooling/.venv/bin/python:*)",
      "Skill(fixing-markdown)",
      "Read(/tmp/**)",
      "Read(//c/tmp/**)"
    ]
  }
}
```

| Permission | Purpose |
| --- | --- |
| `Bash(node:*)` | Run Node.js commands |
| `Bash(markdownlint-cli2:*)` | Run markdown linter |
| `Bash(prettier:*)` | Run code formatter |
| `Bash(.claude/_tooling/.venv/...python...)` | Run Python scripts (reserved for future skills) |
| `Skill(fixing-markdown)` | Allow fixing-markdown skill |
| `Read(/tmp/**)` | Read temporary files (Unix) |
| `Read(//c/tmp/**)` | Read temporary files (Windows) |

**Note:** Python permissions are intentionally kept even if no Python skills are currently active, to support future skill installations.

## Notes

- This skill runs silently when everything is ready
- Only shows output when setup is needed or errors occur
- Other skills should call this at the start of their execution
