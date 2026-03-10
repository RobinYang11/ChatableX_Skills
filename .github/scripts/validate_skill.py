#!/usr/bin/env python3
"""Validate SKILL.md files in a PR.

Checks:
1. SKILL.md exists in each skill directory
2. YAML frontmatter is valid
3. Required fields (name, description, version) are present
4. File size limits (single file < 1MB, skill folder < 5MB)
5. No unexpected top-level files
"""

import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB
MAX_SKILL_SIZE = 5 * 1024 * 1024  # 5 MB
REQUIRED_FIELDS = ["name", "description"]
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def get_changed_skills() -> set[str]:
    """Find skill directories that have changes in the current PR."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/review...HEAD"],
        capture_output=True, text=True,
    )
    changed = set()
    for line in result.stdout.strip().splitlines():
        if line.startswith("skills/"):
            parts = line.split("/")
            if len(parts) >= 2:
                changed.add(parts[1])
    return changed


def validate_skill(skill_dir: Path) -> list[str]:
    """Validate a single skill directory. Returns list of error messages."""
    errors = []
    skill_md = skill_dir / "SKILL.md"

    # Check SKILL.md exists
    if not skill_md.exists():
        errors.append(f"Missing SKILL.md in {skill_dir.name}/")
        return errors

    # Check file sizes
    total_size = 0
    for f in skill_dir.rglob("*"):
        if f.is_file():
            size = f.stat().st_size
            total_size += size
            if size > MAX_FILE_SIZE:
                errors.append(f"{f.relative_to(skill_dir)} exceeds 1MB ({size / 1024 / 1024:.1f}MB)")
    if total_size > MAX_SKILL_SIZE:
        errors.append(f"Skill folder exceeds 5MB ({total_size / 1024 / 1024:.1f}MB)")

    # No restriction on top-level files or directories — users can include
    # LICENSE, README, extra docs, etc. alongside SKILL.md.

    # Parse frontmatter
    content = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        errors.append("SKILL.md missing or malformed YAML frontmatter (must start with ---)")
        return errors

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in frontmatter: {e}")
        return errors

    if not isinstance(frontmatter, dict):
        errors.append("Frontmatter must be a YAML mapping (key: value)")
        return errors

    # Check required fields
    for field in REQUIRED_FIELDS:
        val = frontmatter.get(field)
        if not val or (isinstance(val, str) and not val.strip()):
            errors.append(f"Required frontmatter field '{field}' is missing or empty")

    # Validate name format
    name = frontmatter.get("name", "")
    if name and not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$", name) and len(name) > 1:
        errors.append(f"name '{name}' should be lowercase with hyphens (e.g. 'my-skill-name')")

    # Validate version format
    version = frontmatter.get("version", "")
    if version and not re.match(r"^\d+\.\d+\.\d+", version):
        errors.append(f"version '{version}' should follow semver (e.g. '1.0.0')")

    # Validate Python scripts syntax
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for py_file in scripts_dir.glob("*.py"):
            try:
                compile(py_file.read_text(encoding="utf-8"), str(py_file), "exec")
            except SyntaxError as e:
                errors.append(f"Syntax error in {py_file.name}: {e}")

    return errors


def main():
    skills_root = Path("skills")
    if not skills_root.exists():
        print("No skills/ directory found.")
        sys.exit(0)

    changed = get_changed_skills()
    if not changed:
        # If we can't detect changed skills, validate all
        changed = {d.name for d in skills_root.iterdir() if d.is_dir()}

    all_errors: dict[str, list[str]] = {}
    for skill_name in sorted(changed):
        skill_dir = skills_root / skill_name
        if not skill_dir.exists():
            continue
        errors = validate_skill(skill_dir)
        if errors:
            all_errors[skill_name] = errors

    if all_errors:
        print("❌ Skill validation failed:\n")
        for name, errors in all_errors.items():
            print(f"  📁 {name}/")
            for err in errors:
                print(f"     • {err}")
            print()
        sys.exit(1)
    else:
        print(f"✅ All {len(changed)} skill(s) passed validation.")
        sys.exit(0)


if __name__ == "__main__":
    main()
