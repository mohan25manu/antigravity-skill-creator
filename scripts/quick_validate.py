#!/usr/bin/env python3
"""
Enhanced validation script for skills.
Checks metadata, structure, and internal consistency.
"""

import sys
import os
import re
import yaml
from pathlib import Path

def validate_skill(skill_path):
    """Deep validation of a skill"""
    skill_path = Path(skill_path).resolve()

    # 1. Basic Structure Checks
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, f"Missing {skill_md}"

    content = skill_md.read_text()
    
    # 2. YAML Frontmatter Validation
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid or missing YAML frontmatter in SKILL.md"

    try:
        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"YAML Syntax Error: {e}"

    required_fields = ['name', 'description']
    for field in required_fields:
        if field not in frontmatter:
            return False, f"Missing required field '{field}' in frontmatter"

    # 3. Kebab-case name check
    name = str(frontmatter['name'])
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, f"Skill name '{name}' must be kebab-case (lowercase, digits, hyphens)"

    # 4. Semantic Validation: Path Checking
    # Search for common path patterns in the body of the markdown
    body = content[match.end():]
    
    # Simple regex to find scripts, references, and assets references
    # Look for paths starting with scripts/, references/, or assets/
    referenced_paths = re.findall(r'(?:scripts|references|assets)/[\w\.-]+', body)
    
    errors = []
    for rel_path in set(referenced_paths):
        full_path = skill_path / rel_path
        if not full_path.exists():
            errors.append(f"Referenced file not found: {rel_path}")

    if errors:
        return False, "\n".join(errors)

    return True, f"Skill '{name}' is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
