---
name: skill-creator
description: |
  A meta-skill for creating high-quality agentic skills.
  # TRIGGER SCENARIOS
  - User wants to create a new skill
  - User needs to validate or package an existing skill
---

# Skill Creator

This skill provides a robust toolkit for building, validating, and packaging skills for AI agents.

## Core Features
- **Typed Bootstrapping**: Create skills tailored for specific needs (Workflow, Tool, Knowledge).
- **Semantic Validation**: Ensures all referenced scripts and assets actually exist.
- **Fail-Safe Packaging**: Prevents broken skills from being distributed.
- **Dry-Run Testing**: Verifies Python script syntax and structure.

## Quick Start

### 1. Initialize a Skill
`python scripts/init_skill.py my-skill --type workflow`

### 2. Validate
`python scripts/quick_validate.py output/my-skill`

### 3. Test (Dry Run)
`python scripts/test_skill.py output/my-skill`

### 4. Package
`python scripts/package_skill.py output/my-skill`

## Design Principles
- **Concise is Key**: Keep `SKILL.md` lean. Use `references/` for large docs.
- **Deterministic Complexity**: Use `scripts/` for tasks that need strict reliability.
- **Progressive Disclosure**: Only load what is necessary for the current task.
