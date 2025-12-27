# Experiment 02: Agentic AI Coding 🤖

Exploring **agentic AI coding assistants** that can autonomously explore, modify, and interact with codebases using local LLMs.

![Status](https://img.shields.io/badge/Status-In_Progress-yellow)
![Mistral](https://img.shields.io/badge/Mistral-Devstral-orange)
![LM Studio](https://img.shields.io/badge/LM_Studio-Local-blue)

## About

This experiment explores using **Mistral Vibe CLI** connected to a local **Devstral** model running in LM Studio to perform agentic coding tasks — where the AI can autonomously use tools to read files, execute commands, search code, and make edits.

## Experiment Ideas

| Idea | Description | Goal |
| ---- | ----------- | ---- |
| **Code Generation** | Generate a complete project from a single prompt (CLI tool, REST API, web scraper) | Test autonomous project creation |
| **Codebase Exploration** | Point Vibe at an unfamiliar repo to explain architecture, find issues, add features | Test code understanding |
| **Bug Fixing** | Create intentionally buggy code and see if Vibe can identify and fix bugs | Test debugging capabilities |
| **Multi-Agent Comparison** | Compare Vibe+Devstral (local) vs cloud models vs other tools (Aider, etc.) | Benchmark different approaches |

---

## Architecture

This experiment uses a **two-machine setup** over LAN:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              LOCAL NETWORK (LAN)                            │
│                                                                             │
│  ┌─────────────────────────┐          ┌─────────────────────────────────┐   │
│  │     WINDOWS PC          │          │         MAC MINI PRO            │   │
│  │     (Development)       │   HTTP   │         (LLM Server)            │   │
│  │                         │ ──────►  │                                 │   │
│  │  ┌───────────────────┐  │  :1234   │  ┌───────────────────────────┐  │   │
│  │  │   Mistral Vibe    │  │          │  │       LM Studio           │  │   │
│  │  │   CLI Client      │  │          │  │                           │  │   │
│  │  └───────────────────┘  │          │  │  ┌─────────────────────┐  │  │   │
│  │           │             │          │  │  │     Devstral        │  │  │   │
│  │           ▼             │          │  │  │  (24B, MLX 4-bit)   │  │  │   │
│  │  ┌───────────────────┐  │          │  │  └─────────────────────┘  │  │   │
│  │  │   Your Project    │  │          │  │                           │  │   │
│  │  │   Codebase        │  │          │  └───────────────────────────┘  │   │
│  │  └───────────────────┘  │          │                                 │   │
│  └─────────────────────────┘          └─────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tools & Models

### Mistral Vibe CLI

[Mistral Vibe](https://docs.mistral.ai/mistral-vibe/introduction) is a command-line coding assistant that provides:

- **Interactive Chat**: Conversational AI that breaks down complex tasks
- **Powerful Toolset**: File manipulation, code searching, git operations, shell commands
- **Project-Aware Context**: Automatically scans file structure and git status
- **Safety First**: Tool execution approval before actions

The source code is available on [GitHub](https://github.com/mistralai/mistral-vibe) under Apache 2.0 license.

### Devstral Model

Using **devstral-small-2-24b-instruct-2512** running locally in LM Studio on macOS with Apple Silicon (64GB unified memory).

---

## Setup Guide: Mistral Vibe + LM Studio

This is the recommended approach for this experiment — running Vibe on your development machine while the LLM runs on a separate Mac over the local network.

### Step 1: Configure LM Studio (Mac)

1. **Download and install** [LM Studio](https://lmstudio.ai/) on your Mac

2. **Download the Devstral model**:
   - Open LM Studio
   - Go to the **Discover** tab
   - Search for `devstral-small-2-24b-instruct`
   - Download a quantized version (e.g., MLX 4-bit for Apple Silicon)

3. **Load the model**:
   - Go to the **Chat** tab (or **Developer** tab)
   - Select the Devstral model from the dropdown
   - Wait for it to load into memory

4. **Enable network access**:
   - Go to **Developer** tab (or Local Server)
   - Toggle **"Start Server"** to ON
   - Toggle **"Serve on Local Network"** to ON
   - Note the **IP address and port** shown (e.g., `http://192.168.1.100:1234`)

5. **Verify the server is running**:

   From your Windows PC, test the connection:

   ```bash
   curl http://<YOUR_MAC_IP>:1234/v1/models
   ```

   You should see a JSON response listing the loaded model.

### Step 2: Install Mistral Vibe (Windows)

1. **Create a virtual environment** (recommended):

   ```bash
   # Navigate to where you want to run Vibe
   cd ~/projects

   # Create and activate a virtual environment
   python -m venv .venv-vibe
   source .venv-vibe/Scripts/activate  # Git Bash
   # or
   .\.venv-vibe\Scripts\Activate.ps1   # PowerShell
   ```

2. **Install Mistral Vibe**:

   ```bash
   pip install mistral-vibe
   ```

3. **Verify installation**:

   ```bash
   vibe --version
   ```

### Step 3: Configure Vibe for LM Studio

Mistral Vibe uses a TOML configuration file. Create or edit the config file:

**Windows (Git Bash):**

```bash
mkdir -p ~/.config/mistral-vibe
nano ~/.config/mistral-vibe/config.toml
```

**Windows (PowerShell):**

```powershell
mkdir -Force "$env:USERPROFILE\.config\mistral-vibe"
notepad "$env:USERPROFILE\.config\mistral-vibe\config.toml"
```

**Configuration content:**

```toml
# Mistral Vibe configuration for LM Studio

[provider]
# Use OpenAI-compatible API mode
type = "openai_compatible"

# Your Mac's IP address on the LAN (from LM Studio)
base_url = "http://192.168.1.100:1234/v1"

# LM Studio ignores this but it's required by the client
api_key = "lm-studio"

# Model name exactly as shown in LM Studio
model = "devstral-small-2-24b-instruct-2512"

[ui]
# Theme: dark, light, dracula, monokai, etc.
theme = "dark"

[tools]
# Require approval before executing shell commands
require_approval = true
```

> **⚠️ Important**: Replace `192.168.1.100` with your Mac's actual IP address!

### Step 4: Run Vibe

1. **Navigate to a project directory**:

   ```bash
   cd /path/to/your/project
   ```

2. **Start Vibe**:

   ```bash
   vibe
   ```

3. **Interact with your codebase**:

   Try prompts like:
   - "Explain the structure of this project"
   - "Find all TODO comments in the codebase"
   - "Create a new Python script that does X"
   - "Refactor this function to be more efficient"

---

## Troubleshooting

### Connection Issues

| Problem | Solution |
| ------- | -------- |
| `Connection refused` | Ensure LM Studio server is running and "Serve on Local Network" is enabled |
| `Timeout` | Check firewall settings on both machines; ensure port 1234 is open |
| `Model not found` | Verify the model name in config matches exactly what LM Studio shows |

### Finding Your Mac's IP Address

On your Mac, run:

```bash
ipconfig getifaddr en0
```

Or check in **System Settings > Network > Wi-Fi > Details > IP Address**.

### Testing the Connection Manually

```bash
# Test if the server is reachable
curl http://<MAC_IP>:1234/v1/models

# Test a simple completion
curl http://<MAC_IP>:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "devstral-small-2-24b-instruct-2512",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## Files in This Experiment

```text
02-agentic-ai-coding/
├── README.md                    # This file
├── config/
│   └── config.toml.example      # Sample Vibe configuration
├── sessions/                    # Saved conversation sessions
└── projects/                    # Projects generated by the agent
```

---

## Resources

- [Mistral Vibe Documentation](https://docs.mistral.ai/mistral-vibe/introduction)
- [Mistral Vibe GitHub](https://github.com/mistralai/mistral-vibe) (Apache 2.0)
- [LM Studio](https://lmstudio.ai/)
- [Devstral Model on HuggingFace](https://huggingface.co/mistralai/Devstral-Small-2412)

---

## Experiment Log

*Document your experiments, observations, and results here...*

### Session 1: Initial Setup

- **Date**:
- **Goal**:
- **Observations**:
- **Results**:
