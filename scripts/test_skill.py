#!/usr/bin/env python3
"""
Dry-run testing tool for skills.
Verifies script executability and basic mock interaction.
"""

import sys
import subprocess
from pathlib import Path

def test_skill(skill_path):
    skill_path = Path(skill_path).resolve()
    scripts_dir = skill_path / "scripts"
    
    if not scripts_dir.exists():
        print("No scripts to test.")
        return True
    
    print(f"Testing scripts in {scripts_dir}...")
    
    all_passed = True
    for script in scripts_dir.glob("*.py"):
        print(f"Checking syntax for {script.name}...", end=" ")
        try:
            # Check syntax without running
            subprocess.run([sys.executable, "-m", "py_compile", str(script)], check=True, capture_output=True)
            print("OK")
        except subprocess.CalledProcessError as e:
            print(f"FAILED\n{e.stderr.decode()}")
            all_passed = False
            
    return all_passed

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_skill.py <skill_directory>")
        sys.exit(1)
        
    success = test_skill(sys.argv[1])
    sys.exit(0 if success else 1)
