# Resumen Semgrep (análisis local previo al push)

## Herramienta
- Semgrep (imagen Docker `returntocorp/semgrep:latest`)
- Reglas: `p/security-audit` + `p/owasp-top-ten`

## Alcance analizado
- `app/`
- `server.js`
- `config/`

## Resultados reales (ejecución local)

| Severidad | Cantidad |
|-----------|----------|
| ERROR     | 3        |
| WARNING   | 13       |
| **Total** | **16**   |

## Hallazgos ERROR (bloquean Quality Gate)

Regla: `javascript.lang.security.audit.code-string-concat.code-string-concat`

| Archivo | Línea | Descripción |
|---------|-------|-------------|
| `app/routes/contributions.js` | 32 | `eval(req.body.preTax)` – SSJS injection |
| `app/routes/contributions.js` | 33 | `eval(req.body.afterTax)` – SSJS injection |
| `app/routes/contributions.js` | 34 | `eval(req.body.roth)` – SSJS injection |

## Hallazgos WARNING relevantes (no bloquean por política ERROR)

- Open redirect en `app/routes/index.js` (línea 72)
- Configuración insegura de cookies de sesión en `server.js`
- Enlaces HTTP en páginas tutorial

## Interpretación
Los 3 hallazgos ERROR corresponden a la vulnerabilidad intencional A1 (Injection) de NodeGoat mediante `eval()` sobre entrada de usuario. La política del Quality Gate (`severity == ERROR`) **debe fallar** en el estado inicial.

## Artefactos esperados en GitHub Actions
- `semgrep-results` → `semgrep-results.json`
- `semgrep-results` → `semgrep-results.sarif`
