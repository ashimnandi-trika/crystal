"""Tests for the badge generator."""
from __future__ import annotations

import json as jsonlib

from crystal_guard.badge import (
    GRADE_COLORS,
    build_spec,
    to_markdown,
    to_shields_json,
    to_shields_url,
    to_svg,
)


def test_grade_a_is_green():
    spec = build_spec("A", 95)
    assert spec.color == GRADE_COLORS["A"]
    assert "95/100" in spec.message


def test_grade_f_is_red():
    spec = build_spec("F", 20)
    assert spec.color == GRADE_COLORS["F"]


def test_unknown_grade_fallback():
    spec = build_spec("Z", 50)
    # Fallback grey for unknown grades
    assert spec.color == "#95a5a6"


def test_shields_json_is_valid():
    spec = build_spec("B", 80)
    parsed = jsonlib.loads(to_shields_json(spec))
    assert parsed["schemaVersion"] == 1
    assert parsed["label"] == "crystal"
    assert "80/100" in parsed["message"]
    assert parsed["color"] == GRADE_COLORS["B"]


def test_shields_url_format():
    url = to_shields_url(build_spec("A", 95))
    assert url.startswith("https://img.shields.io/badge/")
    assert "crystal" in url
    # Space should be URL-encoded
    assert " " not in url


def test_markdown_is_linkified():
    md = to_markdown(build_spec("A", 95))
    assert md.startswith("[![")
    assert "crystalcodes.dev" in md
    assert "img.shields.io" in md


def test_svg_is_valid_xml():
    svg = to_svg(build_spec("A", 95))
    assert svg.startswith("<svg")
    assert svg.rstrip().endswith("</svg>")
    assert "A 95/100" in svg
    assert GRADE_COLORS["A"].lstrip("#").lower() in svg.lower()
