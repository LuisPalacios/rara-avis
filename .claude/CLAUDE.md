# Rara Avis

A Flappy Bird clone written in Python using Pygame — 100% AI-generated code.

## Project Overview

| Aspect | Details |
| --- | --- |
| Language | Python 3.13 |
| Framework | Pygame 2.6.1 |
| Main file | `rara-avis.py` |
| Assets | Procedurally generated (no external files) |

## Running the Game

```bash
source .venv/bin/activate
python rara-avis.py
```

## Game Controls

| Action | Input |
| --- | --- |
| Flap / Start | `SPACE` or `Mouse Click` |
| Pause | `P` |

## Code Structure

The game is contained in a single file `rara-avis.py` with these classes:

- `Bird` — Player character with physics and animation
- `Pipe` — Randomized obstacles with collision detection
- `Button` — UI button component
- `Particle` — Visual trail effects
- `Cloud` — Background decoration

## Key Constants

| Constant | Value | Description |
| --- | --- | --- |
| `WIDTH, HEIGHT` | 800x600 | Screen dimensions |
| `GRAVITY` | 0.5 | Fall acceleration |
| `FLAP_STRENGTH` | -8 | Jump velocity |
| `PIPE_GAP` | 180 | Space between pipes |
| `PIPE_SPEED` | 3 | Pipe movement speed |

## Skills Available

### User-Invokable

| Skill | Description |
| --- | --- |
| `/fixing-markdown` | Validate and fix markdown formatting with markdownlint + prettier |

### Internal

| Skill | Description |
| --- | --- |
| `_initializing-environment` | Sets up Python/Node.js environments for other skills |

## Tooling

The `.claude/_tooling/` directory contains:

- **Node.js tools**: markdownlint-cli2, prettier (for markdown validation)

Environment setup is handled automatically by the `_initializing-environment` skill.

## Conventions

- Game code follows Pygame patterns
- All graphics are procedurally generated in code
- No external assets required
