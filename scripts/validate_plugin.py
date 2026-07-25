#!/usr/bin/env python3
"""Validate the mingli-fortune plugin manifests, skill, and cross-references.

Catches the failure modes that break a marketplace install silently:
malformed JSON, drifted version numbers between the two ecosystems'
manifests, manifest paths pointing at files that do not exist, and skill
docs referencing reference files that were renamed or removed.

Run with no arguments from the repo root. Exits non-zero on any failure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Claude Code truncates skill descriptions past this length.
MAX_SKILL_DESCRIPTION = 1024

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def resolve(declared: str) -> Path:
    """Resolve a manifest-declared, repo-root-relative path.

    Use an explicit prefix strip: str.lstrip('./') strips *characters*, so it
    would turn './.mcp.json' into 'mcp.json'.
    """
    rel = str(declared)
    if rel.startswith("./"):
        rel = rel[2:]
    return ROOT / rel


def load_json(rel: str) -> dict | None:
    path = ROOT / rel
    if not path.is_file():
        fail(f"{rel}: missing")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{rel}: invalid JSON — {exc}")
        return None


def check_all_json_parses() -> None:
    for path in sorted(ROOT.rglob("*.json")):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{path.relative_to(ROOT)}: invalid JSON — {exc}")


def check_versions_match(claude: dict | None, codex: dict | None) -> None:
    if not claude or not codex:
        return
    cv, xv = claude.get("version"), codex.get("version")
    if cv is None:
        fail(".claude-plugin/plugin.json: no version field")
    if xv is None:
        fail(".codex-plugin/plugin.json: no version field")
    if cv is not None and xv is not None and cv != xv:
        fail(
            "version drift: .claude-plugin/plugin.json is "
            f"{cv!r} but .codex-plugin/plugin.json is {xv!r}"
        )


def check_manifest_paths(manifest: dict | None, rel: str, keys: tuple[str, ...]) -> None:
    if not manifest:
        return
    for key in keys:
        declared = manifest.get(key)
        if declared is None:
            continue
        if not resolve(declared).exists():
            fail(f"{rel}: {key} points at {declared!r}, which does not exist")


def check_marketplace(marketplace: dict | None) -> None:
    if not marketplace:
        return
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail(".claude-plugin/marketplace.json: no plugins listed")
        return
    for entry in plugins:
        source = entry.get("source")
        if source is None:
            fail(f".claude-plugin/marketplace.json: {entry.get('name')!r} has no source")
            continue
        if not resolve(source).exists():
            fail(
                ".claude-plugin/marketplace.json: "
                f"{entry.get('name')!r} source {source!r} does not exist"
            )


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def check_skills() -> None:
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        fail("skills/: missing")
        return
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        fail("skills/: no SKILL.md found")
        return
    for skill in skill_files:
        rel = skill.relative_to(ROOT)
        fields = parse_frontmatter(skill)
        if fields is None:
            continue
        name = fields.get("name")
        if not name:
            fail(f"{rel}: frontmatter has no name")
        elif name != skill.parent.name:
            fail(
                f"{rel}: frontmatter name {name!r} does not match "
                f"directory {skill.parent.name!r}"
            )
        description = fields.get("description")
        if not description:
            fail(f"{rel}: frontmatter has no description")
        elif len(description) > MAX_SKILL_DESCRIPTION:
            fail(
                f"{rel}: description is {len(description)} chars, "
                f"over the {MAX_SKILL_DESCRIPTION} limit"
            )


def check_reference_links() -> None:
    """Every `references/x.md` mentioned in skill docs must exist."""
    pattern = re.compile(r"`(references/[A-Za-z0-9._/-]+\.md)`")
    for skill_dir in sorted((ROOT / "skills").glob("*")):
        if not skill_dir.is_dir():
            continue
        for doc in sorted(skill_dir.rglob("*.md")):
            for ref in sorted(set(pattern.findall(doc.read_text(encoding="utf-8")))):
                if not (skill_dir / ref).is_file():
                    fail(f"{doc.relative_to(ROOT)}: references missing file {ref!r}")


def check_commands() -> None:
    for cmd in sorted((ROOT / "commands").glob("*.md")):
        fields = parse_frontmatter(cmd)
        if fields is not None and not fields.get("description"):
            fail(f"{cmd.relative_to(ROOT)}: frontmatter has no description")


def main() -> int:
    check_all_json_parses()

    claude = load_json(".claude-plugin/plugin.json")
    codex = load_json(".codex-plugin/plugin.json")
    marketplace = load_json(".claude-plugin/marketplace.json")
    load_json(".mcp.json")
    load_json(".codex-plugin/mcp.json")

    check_versions_match(claude, codex)
    check_manifest_paths(claude, ".claude-plugin/plugin.json", ("skills", "mcpServers"))
    check_manifest_paths(codex, ".codex-plugin/plugin.json", ("skills", "mcpServers"))
    check_marketplace(marketplace)
    check_skills()
    check_reference_links()
    check_commands()

    if errors:
        print(f"validate_plugin: {len(errors)} problem(s)\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("validate_plugin: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
