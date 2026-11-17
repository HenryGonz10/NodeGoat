====================================================
QUALITY GATE: FAILED
====================================================

Policy:
  - Semgrep severity ERROR        => FAIL
  - Dependency-Check CVSS >= 7.0 => FAIL

SAST (Semgrep): FAIL
Semgrep total findings: 16
Semgrep ERROR findings: 3
  - ERROR javascript.lang.security.audit.code-string-concat.code-string-concat @ app/routes/contributions.js:32
  - ERROR javascript.lang.security.audit.code-string-concat.code-string-concat @ app/routes/contributions.js:33
  - ERROR javascript.lang.security.audit.code-string-concat.code-string-concat @ app/routes/contributions.js:34

SCA (Dependency-Check): FAIL
Dependency-Check dependencies scanned: 37
Vulnerabilities with CVSS >= 7.0: 54
