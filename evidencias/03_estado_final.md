# 03 — Estado final tras remediación

## Validación local

| Control | Resultado |
|---------|-----------|
| SAST Semgrep (ERROR) | **PASS** — 0 hallazgos ERROR |
| SCA Dependency-Check (CVSS ≥ 7 tras suppressions justificadas) | **PASS** |
| SBOM CycloneDX | Generado / regenerable en CI |
| Quality Gate | **PASSED** |

## Diferencias respecto al estado inicial

| Aspecto | Inicial (Commit 1) | Final (Commit 2) |
|---------|--------------------|------------------|
| `eval(req.body.*)` | Presente (3 ERROR) | Removido → `parseInt` |
| `marked` | 0.3.5 (GHSA XSS CVSS 7.5) | ^4.3.0 + helper `parse` |
| Suppressions SCA | Ausentes | `dependency-check-suppressions.xml` (A9, expira 2027-12-31) |
| Quality Gate | FAILED | PASSED |

## Ejecución en GitHub Actions
Registrar aquí la URL del run SUCCESS tras publicar la remediación:

- URL SUCCESS: ____________________________________

## Artefactos esperados en el run SUCCESS
- `semgrep-results`
- `dependency-check-reports`
- `sbom-cyclonedx`
- `quality-gate-summary` con `QUALITY GATE: PASSED`
