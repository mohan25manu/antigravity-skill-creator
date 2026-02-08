# Antigravity Skill Creator Template

This repository is a **Meta-Skill** designed to help build high-quality, standardized skills for AI agents (specifically Antigravity). It is based on the [Anthropics Skill Creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator).

## Features

- **Standardized Structure**: Enforces the `SKILL.md`, `scripts/`, `references/`, and `assets/` layout.
- **Boilerplate Generator**: `init_skill.py` creates a new skill directory with all the right placeholders.
- **Validation**: `quick_validate.py` ensures your skill metadata is correctly formatted.
- **Packaging**: `package_skill.py` zips your skill into a distributable `.skill` file.

## How to Use

### 1. Initialize a New Skill
```bash
python3 scripts/init_skill.py my-new-skill --path ./output
```

### 2. Validate a Skill
```bash
python3 scripts/quick_validate.py path/to/my-skill
```

### 3. Package a Skill
```bash
python3 scripts/package_skill.py path/to/my-skill ./dist
```

## Creating Better Skills

Refer to the documents in `references/` for best practices:
- [Workflows](references/workflows.md): Sequential and conditional logic.
- [Output Patterns](references/output-patterns.md): Templates for consistent quality.

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE.txt](LICENSE.txt) file for details.
