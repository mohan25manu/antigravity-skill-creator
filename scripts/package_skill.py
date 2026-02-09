#!/usr/bin/env python3
"""
Improved Packaging Script with Pre-validation.
"""

import sys
import shutil
import zipfile
from pathlib import Path
from quick_validate import validate_skill

def package_skill(skill_path, dist_path):
    skill_path = Path(skill_path).resolve()
    dist_path = Path(dist_path).resolve()
    dist_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Validate before packaging
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"FAILED TO PACKAGE: Validation Error\n{message}")
        sys.exit(1)
        
    # 2. Package
    skill_name = skill_path.name
    zip_name = dist_path / f"{skill_name}.skill"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                # Don't include hidden files or __pycache__
                if not file_path.name.startswith('.') and '__pycache__' not in file_path.parts:
                    zipf.write(file_path, file_path.relative_to(skill_path))
                    
    print(f"Successfully packaged skill to: {zip_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill_directory> [dist_directory]")
        sys.exit(1)
        
    target = sys.argv[1]
    destination = sys.argv[2] if len(sys.argv) > 2 else "./dist"
    package_skill(target, destination)
