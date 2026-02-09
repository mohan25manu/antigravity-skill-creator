#!/usr/bin/env python3
"""
Improved Skill Initializer with Typed Templates.
"""

import sys
import argparse
from pathlib import Path

TEMPLATES = {
    "workflow": """---
name: {name}
description: |
  A workflow skill for [High-level Task].
  # TRIGGER SCENARIOS
  - User wants to perform a multi-step [Process]
  - Complex [Data Type] needs to be processed sequentially
---

# {name} Workflow

## Steps
1. **Analyze**: Initial state assessment.
2. **Execute**: Main processing step.
3. **Verify**: Integrity check.

## Details
Refer to [specific references] if needed.
""",
    "tool": """---
name: {name}
description: |
  A tool wrapper skill for [Specific Tool/Script].
  # TRIGGER SCENARIOS
  - User requests [Action] that requires [Script]
  - [Input File] needs to be processed via [Library]
---

# {name} Tool

## Usage
Run the following script:
`python scripts/main.py --input <file>`

## Parameters
- `--input`: Path to the input resource.
""",
    "knowledge": """---
name: {name}
description: |
  A knowledge skill providing context for [Domain].
  # TRIGGER SCENARIOS
  - User asks about [Domain/Service]
  - Reference information for [Schema/Policy] is needed
---

# {name} Knowledge Base

## Overview
This skill provides context about [Domain].

## Key Concepts
- **Concept A**: Description.
- **Concept B**: Description.

## References
Detailed docs are in `references/docs.md`.
"""
}

def init_skill(name, path, skill_type):
    skill_dir = Path(path) / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)
    
    # Create SKILL.md
    template = TEMPLATES.get(skill_type, TEMPLATES["workflow"])
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(template.format(name=name))
    
    print(f"Initialized '{skill_type}' skill at: {skill_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize a new agent skill.")
    parser.add_argument("name", help="Name of the skill (kebab-case)")
    parser.add_argument("--path", default="./output", help="Directory to create skill in")
    parser.add_argument("--type", choices=["workflow", "tool", "knowledge"], default="workflow", help="Type of skill template")
    
    args = parser.parse_args()
    init_skill(args.name, args.path, args.type)
