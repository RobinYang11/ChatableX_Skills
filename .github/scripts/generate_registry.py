#!/usr/bin/env python3
"""Generate registry.json by scanning all skills/*/SKILL.md frontmatter.

Run by GitHub Actions on every push to main. The output file is committed
back to the repo so clients can fetch it via GitHub Raw CDN:
  https://raw.githubusercontent.com/{owner}/{repo}/main/registry.json

Output format:
{
  "generated_at": "2026-03-10T12:00:00Z",
  "total": 42,
  "categories": ["productivity", "data-analysis", ...],
  "skills": [
    {
      "id": "daily-news-briefing",
      "name": "daily-news-briefing",
      "description": "...",
      "version": "1.0.0",
      "author": "...",
      "category": "productivity",
      "tool_ids": ["google-search", "email-sender"],
      "has_scripts": true,
      "has_references": true,
      "has_assets": false,
      "file_count": 4,
      "total_size": 2048
    },
    ...
  ]
}
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml

SKILLS_DIR = Path("skills")
OUTPUT_FILE = Path("registry.json")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_skill(skill_dir: Path) -> Optional[dict]:
    """Parse a single skill directory and return its index entry."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"  ⚠️  Skipping {skill_dir.name}: no SKILL.md")
        return None

    content = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        print(f"  ⚠️  Skipping {skill_dir.name}: no frontmatter")
        return None

    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        print(f"  ⚠️  Skipping {skill_dir.name}: invalid YAML — {e}")
        return None

    if not isinstance(fm, dict):
        print(f"  ⚠️  Skipping {skill_dir.name}: frontmatter is not a mapping")
        return None

    name = fm.get("name", "")
    description = fm.get("description", "")
    if not name or not description:
        print(f"  ⚠️  Skipping {skill_dir.name}: missing name or description")
        return None

    # Collect file stats
    file_count = 0
    total_size = 0
    for f in skill_dir.rglob("*"):
        if f.is_file():
            file_count += 1
            total_size += f.stat().st_size

    variables = fm.get("variables", [])
    variable_names = []
    if isinstance(variables, list):
        variable_names = [v.get("name", "") for v in variables if isinstance(v, dict)]

    return {
        "id": skill_dir.name,
        "name": name,
        "description": description,
        "version": fm.get("version", "1.0.0"),
        "author": fm.get("author", ""),
        "category": fm.get("category", "other"),
        "tool_ids": fm.get("tool_ids", []),
        "variables": variable_names,
        "has_scripts": (skill_dir / "scripts").is_dir()
            and any((skill_dir / "scripts").iterdir()),
        "has_references": (skill_dir / "references").is_dir()
            and any((skill_dir / "references").iterdir()),
        "has_assets": (skill_dir / "assets").is_dir()
            and any((skill_dir / "assets").iterdir()),
        "file_count": file_count,
        "total_size": total_size,
    }


def main():
    if not SKILLS_DIR.exists():
        print("❌ skills/ directory not found")
        sys.exit(1)

    skills = []
    for child in sorted(SKILLS_DIR.iterdir()):
        if not child.is_dir():
            continue
        print(f"  📦 Scanning {child.name}...")
        entry = parse_skill(child)
        if entry:
            skills.append(entry)

    categories = sorted({s["category"] for s in skills})

    registry = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total": len(skills),
        "categories": categories,
        "skills": skills,
    }

    OUTPUT_FILE.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"\n✅ registry.json generated: {len(skills)} skills, {len(categories)} categories")


if __name__ == "__main__":
    main()
