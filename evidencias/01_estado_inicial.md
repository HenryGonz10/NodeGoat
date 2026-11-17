# 01 — Estado inicial (vulnerable, Quality Gate debe fallar)

## Commit base analizado
- SHA: `c5cb68a7084e4ae7dcc60e6a98768720a81841e8`
- Mensaje: `Merge pull request #290 from za/add-blank-space`
- Rama de trabajo: `devsecops-pipeline`
- Upstream: `https://github.com/OWASP/NodeGoat.git`
- Fork / origin: `https://github.com/HenryGonz10/NodeGoat.git`

## Resumen técnico del proyecto (antes de cambios)

| Elemento | Valor |
|----------|-------|
| Aplicación | OWASP NodeGoat 1.3.0 (deliberadamente vulnerable) |
| Runtime declarado | Docker `node:12-alpine`; CI histórica 10.x/12.x/14.x; Travis v8/v10/v12 |
| Lockfile | `package-lock.json` (npm) |
| Workflows previos | `.github/workflows/e2e-test.yml`, `lint.yml` (Actions antiguas v1/v2) |
| Config seguridad previa | Sin pipeline DevSecOps SAST/SCA/SBOM/Quality Gate |

### Dependencias obsoletas / de riesgo (package.json)
Entre otras: `marked@0.3.5`, `needle@2.2.4`, `helmet@^2.0.0`, `bcrypt-nodejs@0.0.3`, `mongodb@^2.1.18`. El propio `package.json` documenta componentes inseguros intencionales (A9).

### Patrones detectables por Semgrep
Uso de `eval(req.body.*)` en `app/routes/contributions.js` (SSJS injection), open redirect y cookies de sesión sin flags seguros.

## Análisis ejecutados en la fase inicial

1. **SAST – Semgrep** (`p/security-audit` + `p/owasp-top-ten`)
   - 16 hallazgos totales
   - **3 ERROR** en `app/routes/contributions.js` (`eval`)
2. **SBOM – Syft**
   - CycloneDX `bomFormat=CycloneDX`, `specVersion=1.7`
   - **422 componentes**
3. **SCA – npm audit (referencia)**
   - high: 67, critical: 39 (total high+critical: 106)
4. **SCA – OWASP Dependency-Check** (con `--nvdDatafeed` tras fallo de NVD API sin key)
   - Dependencias: **37**
   - Vulnerabilidades CVSS ≥ 7.0: **54**
   - Exit code: **15** (falla por `--failOnCVSS 7`)
   - Reportes: HTML + JSON

## Por qué el Quality Gate debe fallar

Política:
- Semgrep severity **ERROR** → FAIL
- Dependency-Check **CVSS >= 7.0** → FAIL

En el estado inicial existen **3 hallazgos Semgrep ERROR** por `eval()` sobre input HTTP, suficiente para:

`QUALITY GATE: FAILED`

Además, el inventario de dependencias antiguas de NodeGoat aporta hallazgos SCA con CVSS ≥ 7.0.

## Artefactos del workflow

| Artefacto GHA | Contenido |
|---------------|-----------|
| `semgrep-results` | `semgrep-results.json`, `semgrep-results.sarif`, `sast-status.txt` |
| `dependency-check-reports` | HTML + JSON + `sca-status.txt` |
| `sbom-cyclonedx` | `sbom.cyclonedx.json` + snippets |
| `quality-gate-summary` | resumen PASSED/FAILED |

## Ejecución en GitHub Actions
Registrar aquí la URL del run FAILED tras publicar el Commit 1 en el fork:

- URL FAILED: ____________________________________
