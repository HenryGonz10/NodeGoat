# 02 — Remediación controlada

## Problema inicial
1. **SAST ERROR:** `eval(req.body.*)` en `app/routes/contributions.js` (3 hallazgos Semgrep ERROR) → inyección SSJS.
2. **SCA HIGH:** `marked@0.3.5` con advisories reales (p. ej. GHSA-5v2h-r2cx-5xgj, GHSA-x5pg-88wf-qq4p, GHSA-rrrm-qjm4-v8hf, CVSS 7.5).
3. **SCA baseline A9:** múltiples hallazgos CVSS ≥ 7 en dependencias intencionalmente antiguas de NodeGoat.

## Cambios realizados

### 1) Corrección de código (SAST)
| Campo | Detalle |
|-------|---------|
| Archivo | `app/routes/contributions.js` |
| Severidad | Semgrep ERROR |
| Cambio | `eval(...)` → `parseInt(...)` para `preTax`, `afterTax`, `roth` |
| Justificación | Elimina ejecución de input HTTP controlado por el usuario (A1 Injection) |
| Impacto funcional | El flujo de contribuciones mantiene validación numérica; no se eliminan el resto de vulnerabilidades educativas |

### 2) Actualización de dependencia (SCA)
| Campo | Detalle |
|-------|---------|
| Dependencia | `marked` |
| Antes | `0.3.5` |
| Después | `^4.3.0` (lockfile actualizado) |
| Archivo adicional | `server.js` — helper `app.locals.marked = (text) => marked.parse(...)` para compatibilidad con plantillas Swig |
| Justificación | Remediación de XSS conocidos en marked 0.3.5 |
| Impacto funcional | Los memos Markdown continúan renderizándose con `{{ marked(doc.memo) }}` |

### 3) Aceptación de riesgo documentada (SCA restante)
| Campo | Detalle |
|-------|---------|
| Archivo | `dependency-check-suppressions.xml` |
| Qué cubre | Hallazgos npm restantes con CVSS ≥ 7 tras las remediaciones anteriores |
| Justificación | NodeGoat conserva componentes inseguros a propósito (A9). Eliminar todos los HIGH/CRITICAL transitivos alteraría el baseline educativo |
| Controles | Expira `2027-12-31`; el Commit 1 no incluye este archivo; Semgrep permanece activo sin excepciones |
| Alcance | Laboratorio académico; no aplica a producción |

## Resultado posterior
| Control | Resultado |
|---------|-----------|
| Semgrep ERROR | **0** (PASS) |
| Dependency-Check CVSS ≥ 7 (con suppressions) | **0** (PASS) |
| Quality Gate | **PASSED** (validación local; confirmar en GitHub Actions) |
