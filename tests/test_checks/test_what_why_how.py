"""Tests for WHAT/WHY/HOW check."""

from chealth.checks.what_why_how import WhatWhyHow
from chealth.models import CheckContext, Severity


def test_pass_all_covered(make_claude_md, project):
    content = (
        "# Overview\n\n"
        "The purpose of this Python framework is to build APIs.\n\n"
        "## Build\n\n"
        "- Run `python setup.py test`\n"
    )
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = WhatWhyHow().run(ctx)
    assert results[0].severity == Severity.PASS


def test_warn_partial(make_claude_md, project):
    f = make_claude_md("# Project\n\nThis Python framework does things.\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = WhatWhyHow().run(ctx)
    assert results[0].severity == Severity.WARN


def test_danger_none_covered(make_claude_md, project):
    f = make_claude_md("# Notes\n\n- Remember to check the logs\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = WhatWhyHow().run(ctx)
    assert results[0].severity == Severity.DANGER
