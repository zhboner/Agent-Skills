#!/usr/bin/env python3
"""Copy a skill directory to an install location after validation."""

import shutil
import sys
from pathlib import Path
from scripts.quick_validate import validate_skill

EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git"}
EXCLUDE_FILES = {".DS_Store"}


def copy_tree_excluding(src: Path, dst: Path, exclude_dirs: set, exclude_files: set):
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.is_dir():
            if item.name in exclude_dirs:
                continue
            copy_tree_excluding(item, dst / item.name, exclude_dirs, exclude_files)
        elif item.is_file():
            if item.name in exclude_files:
                continue
            shutil.copy2(item, dst / item.name)


def package_skill(skill_path, output_dir=None):
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"Error: Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"Error: Path is not a directory: {skill_path}")
        return None

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: SKILL.md not found in {skill_path}")
        return None

    print(f"Validating skill: {skill_path.name}")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"Validation FAILED: {message}")
        return None
    print(f"Validation PASSED: {message}")

    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
        dest = output_path / skill_name
    else:
        dest = Path.cwd() / skill_name

    if dest.exists():
        print(f"Warning: {dest} already exists, overwriting")
        shutil.rmtree(dest)

    copy_tree_excluding(skill_path, dest, EXCLUDE_DIRS, EXCLUDE_FILES)
    print(f"Skill copied to: {dest}")
    return dest


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python package_skill.py <path/to/skill-folder> [output-directory]"
        )
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
