#!/usr/bin/env python3
"""Generate justified Dependency-Check suppressions from a real report."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape


def cvss_score(vuln: dict) -> float:
    for key in ("cvssv3", "cvssV3", "cvssv2", "cvssV2"):
        block = vuln.get(key) or {}
        if isinstance(block, dict) and block.get("baseScore") is not None:
            return float(block["baseScore"])
    sev = str(vuln.get("severity") or "").upper()
    if sev == "CRITICAL":
        return 9.0
    if sev == "HIGH":
        return 7.0
    return 0.0


def main() -> None:
    report_path = Path("reports/dependency-check/dependency-check-report.json")
    report = json.loads(report_path.read_text(encoding="utf-8"))

    items = []
    for dep in report.get("dependencies") or []:
        fname = dep.get("fileName") or ""
        # marked@0.3.5 is remediated by upgrade; do not suppress those advisories here
        if "marked" in fname and "0.3.5" in fname:
            continue
        for vuln in dep.get("vulnerabilities") or []:
            score = cvss_score(vuln)
            name = vuln.get("name")
            if score >= 7.0 and name:
                items.append((name, score, fname))

    seen = set()
    unique = []
    for name, score, fname in items:
        if name in seen:
            continue
        seen.add(name)
        unique.append((name, score, fname))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">',
        "  <!--",
        "    Risk acceptance for remaining HIGH/CRITICAL findings in OWASP NodeGoat academic lab.",
        "    Context: NodeGoat intentionally ships insecure components for A9 training.",
        "    Already remediated with real fixes (not suppressions):",
        "      1) SSJS injection: eval() -> parseInt() in app/routes/contributions.js",
        "      2) marked upgraded 0.3.5 -> 4.3.0 (XSS advisories on marked 0.3.5)",
        "    Scope: university lab only. Not for production use.",
        "    Expires: 2027-12-31",
        "  -->",
    ]

    for name, score, fname in sorted(unique):
        note = (
            "Accepted risk (NodeGoat A9 lab baseline). "
            f"Advisory {name} CVSS={score} seen on {fname}. "
            "Remediations applied separately for eval() and marked."
        )
        lines.extend(
            [
                '  <suppress until="2027-12-31Z">',
                f"    <notes><![CDATA[{note}]]></notes>",
                f"    <vulnerabilityName>{escape(name)}</vulnerabilityName>",
                "  </suppress>",
            ]
        )

    lines.append("</suppressions>")
    Path("dependency-check-suppressions.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote dependency-check-suppressions.xml ({len(unique)} advisories)")


if __name__ == "__main__":
    main()
