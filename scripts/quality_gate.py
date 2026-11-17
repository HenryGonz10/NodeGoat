#!/usr/bin/env python3
"""
Quality Gate evaluator for NodeGoat DevSecOps pipeline.

Policy:
  - Semgrep finding with severity ERROR  -> FAIL
  - Dependency-Check vulnerability with CVSS >= 7.0 -> FAIL

Exit codes:
  0 = PASSED
  1 = FAILED
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def severity_of_semgrep(finding: dict[str, Any]) -> str:
    extra = finding.get("extra") or {}
    return str(extra.get("severity") or finding.get("severity") or "").upper()


def evaluate_semgrep(path: Path) -> tuple[str, list[str]]:
    if not path.exists():
        return "FAIL", [f"Semgrep report not found: {path}"]

    data = json.loads(path.read_text(encoding="utf-8"))
    results = data.get("results") or []
    errors = [r for r in results if severity_of_semgrep(r) == "ERROR"]

    details: list[str] = []
    details.append(f"Semgrep total findings: {len(results)}")
    details.append(f"Semgrep ERROR findings: {len(errors)}")
    for r in errors[:20]:
        details.append(
            f"  - ERROR {r.get('check_id')} @ {r.get('path')}:{r.get('start', {}).get('line')}"
        )

    return ("FAIL" if errors else "PASS"), details


def cvss_score(vuln: dict[str, Any]) -> float:
    for key in ("cvssv3", "cvssV3", "cvssv2", "cvssV2"):
        block = vuln.get(key)
        if isinstance(block, dict):
            score = block.get("baseScore")
            if score is not None:
                try:
                    return float(score)
                except (TypeError, ValueError):
                    pass

    score = vuln.get("cvssScore")
    if score is not None:
        try:
            return float(score)
        except (TypeError, ValueError):
            pass

    sev = str(vuln.get("severity") or "").upper()
    if sev == "CRITICAL":
        return 9.0
    if sev == "HIGH":
        return 7.0
    return 0.0


def evaluate_dependency_check(path: Path, threshold: float = 7.0) -> tuple[str, list[str]]:
    if not path.exists():
        return "FAIL", [f"Dependency-Check report not found: {path}"]

    data = json.loads(path.read_text(encoding="utf-8"))
    dependencies = data.get("dependencies") or []

    high: list[str] = []
    for dep in dependencies:
        dep_name = dep.get("fileName") or dep.get("packagePath") or dep.get("filePath") or "unknown"
        for vuln in dep.get("vulnerabilities") or []:
            score = cvss_score(vuln)
            if score >= threshold:
                name = vuln.get("name") or vuln.get("source") or "unknown-cve"
                high.append(f"  - {name} CVSS={score} @ {dep_name}")

    details = [
        f"Dependency-Check dependencies scanned: {len(dependencies)}",
        f"Vulnerabilities with CVSS >= {threshold}: {len(high)}",
    ]
    details.extend(high[:30])
    if len(high) > 30:
        details.append(f"  ... and {len(high) - 30} more")

    return ("FAIL" if high else "PASS"), details


def main() -> int:
    parser = argparse.ArgumentParser(description="NodeGoat DevSecOps Quality Gate")
    parser.add_argument("--semgrep", required=True, type=Path)
    parser.add_argument("--dependency-check", required=True, type=Path)
    parser.add_argument("--threshold", type=float, default=7.0)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    sast_status, sast_details = evaluate_semgrep(args.semgrep)
    sca_status, sca_details = evaluate_dependency_check(args.dependency_check, args.threshold)

    overall = "PASSED" if (sast_status == "PASS" and sca_status == "PASS") else "FAILED"

    lines = [
        "====================================================",
        f"QUALITY GATE: {overall}",
        "====================================================",
        "",
        "Policy:",
        "  - Semgrep severity ERROR        => FAIL",
        f"  - Dependency-Check CVSS >= {args.threshold} => FAIL",
        "",
        f"SAST (Semgrep): {sast_status}",
        *sast_details,
        "",
        f"SCA (Dependency-Check): {sca_status}",
        *sca_details,
        "",
    ]
    report = "\n".join(lines)
    print(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")

    return 0 if overall == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
