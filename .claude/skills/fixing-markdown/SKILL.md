---
name: fixing-markdown
description: Validate and fix markdown formatting in files and folders. Use when the user wants to check formatting, validate markdown, fix lint errors, revisar formato, validar notas, comprobar markdown, arreglar markdown, limpiar markdown, or clean up files.
---

# /fixing-markdown — Validate and Fix Markdown

Run `markdownlint-cli2` + `prettier` to auto-fix markdown formatting issues.

## Usage

```text
/fixing-markdown <target>
```

**Arguments:**

- `target` (Required):
  - **File path**: Single file (e.g., `src/content/posts/2025-11-30-example.md`)
  - **Folder path**: All .md files recursively (e.g., `src/content/posts`)

**No argument = show this usage.**

## Prerequisites

**Run _initializing-environment first** to ensure Node.js environment is ready.

Tools required in `.claude/_tooling/node_modules/`:

- `markdownlint-cli2`
- `prettier`

## Commands

### Single File

```bash
# Step 1: Fix structural issues
node .claude/_tooling/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs --config .claude/_tooling/.markdownlint-cli2.jsonc "path/to/file.md"

# Step 2: Format (table alignment, spacing)
node .claude/_tooling/node_modules/prettier/bin/prettier.cjs --config .claude/_tooling/.prettierrc --write "path/to/file.md"
```

### Folder (recursive)

```bash
# Step 1: Fix structural issues
node .claude/_tooling/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs --config .claude/_tooling/.markdownlint-cli2.jsonc "path/to/folder/**/*.md"

# Step 2: Format
node .claude/_tooling/node_modules/prettier/bin/prettier.cjs --config .claude/_tooling/.prettierrc --write "path/to/folder/**/*.md"
```

## Examples

```text
/fixing-markdown src/content/posts/2025-11-30-navaja-pdfly.md
→ Fixes and formats specific file

/fixing-markdown src/content/posts
→ Fixes and formats all .md files in posts/ recursively

/fixing-markdown .claude/skills
→ Fixes and formats all .md files in skills/ recursively
```

## Output Format

### Clean File

```text
Fixing: src/content/posts/2025-11-30-navaja-pdfly.md

markdownlint: 0 errors
prettier: formatted

✅ Done
```

### With Issues Fixed

```text
Fixing: src/content/posts/2013-12-23-ip-fija-systemd.md

markdownlint: 2 errors fixed
prettier: formatted

✅ Done
```

## Tools

| Tool              | Purpose                                                      |
| ----------------- | ------------------------------------------------------------ |
| markdownlint-cli2 | Structural fixes (headings, lists, code blocks, blank lines) |
| prettier          | Visual formatting (table alignment, consistent spacing)      |

## Rules Enforced

### markdownlint-cli2 (`.claude/_tooling/.markdownlint-cli2.jsonc`)

| Rule  | Description                     |
| ----- | ------------------------------- |
| MD001 | Heading levels increment by one |
| MD003 | ATX style headings (`##`)       |
| MD004 | Dash (`-`) for unordered lists  |
| MD009 | No trailing whitespace          |
| MD010 | No hard tabs                    |
| MD012 | Max 1 consecutive blank line    |
| MD022 | Blank lines around headings     |
| MD031 | Blank lines around code blocks  |
| MD032 | Blank lines around lists        |
| MD047 | File ends with newline          |

### prettier (`.claude/_tooling/.prettierrc`)

- Table column alignment
- Consistent spacing
- Prose wrap preserved (no line breaking)

## Behavior

1. **Check argument**: If no target provided, show usage and exit
2. **Run initializing-environment**: Ensure Node.js environment is ready
3. **Detect target type**: file or folder
4. **Run markdownlint-cli2**: Fix structural issues
5. **Run prettier**: Format visual appearance
6. **Report**: Show results from both tools

## Notes

- Config files: `.claude/_tooling/.markdownlint-cli2.jsonc`, `.claude/_tooling/.prettierrc`
- Requires: Node.js environment (handled by initializing-environment)
