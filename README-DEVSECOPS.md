# DevSecOps Pipeline — OWASP NodeGoat

## Objetivo
Implementación de un pipeline DevSecOps sobre OWASP NodeGoat (aplicación deliberadamente vulnerable) para la práctica de Seguridad en Aplicaciones: SAST, SCA, SBOM, publicación de artefactos y Quality Gate con evidencia FAILED → remediación → SUCCESS.

## Repositorio
- Upstream OWASP: `https://github.com/OWASP/NodeGoat.git`
- Fork de trabajo: `https://github.com/HenryGonz10/NodeGoat.git`
- Rama: `devsecops-pipeline`

## Herramientas
- **GitHub Actions** — orquestación CI/CD
- **Semgrep** — SAST (`p/security-audit`, `p/owasp-top-ten`)
- **OWASP Dependency-Check** — SCA con `--failOnCVSS 7`
- **Anchore Syft / sbom-action** — SBOM CycloneDX JSON

## Flujo

```
Código
  → SAST (Semgrep)
  → SCA (Dependency-Check)
  → SBOM (Syft CycloneDX)
  → Quality Gate
  → Artefactos (siempre publicados)
  → Resultado FAILED / SUCCESS
```

Workflow: `.github/workflows/devsecops-pipeline.yml`  
Nombre visible: `DevSecOps Pipeline - SAST SCA SBOM Quality Gate`

Triggers: `push`/`pull_request` en `main` y `master`, más `workflow_dispatch`.

## Política del Quality Gate
- Hallazgo Semgrep con severidad **ERROR** → **FAIL**
- Vulnerabilidad Dependency-Check con **CVSS >= 7.0** → **FAIL**
- El job `quality-gate` imprime `QUALITY GATE: FAILED` o `QUALITY GATE: PASSED` y determina el estado final del workflow
- Los artefactos se conservan aunque el gate falle

## Remotes

```bash
git remote -v
# origin    https://github.com/HenryGonz10/NodeGoat.git
# upstream  https://github.com/OWASP/NodeGoat.git
```

No realizar push al repositorio oficial de OWASP (`upstream`).

## Cómo publicar la evidencia FAILED y SUCCESS

Si se publican ambos commits de una sola vez, Actions reflejará principalmente el estado del último commit. Para conservar evidencia FAILED:

```bash
# A) Publicar SOLO Commit 1 (Quality Gate FAILED esperado)
git push -u origin cfadd2d:refs/heads/devsecops-pipeline
# Esperar Actions → FAILED → capturas 1-3

# B) Publicar remediación (Quality Gate SUCCESS esperado)
git push origin HEAD:refs/heads/devsecops-pipeline
# Esperar Actions → SUCCESS → capturas 4-5
```

Opcional: configurar secret `NVD_API_KEY` en Settings → Secrets → Actions.

## Cómo ejecutar

### En GitHub Actions
1. Push a `origin` (`HenryGonz10/NodeGoat`)
2. Abrir **Actions**
3. Seleccionar `DevSecOps Pipeline - SAST SCA SBOM Quality Gate`
4. Revisar jobs, logs del Quality Gate y descargar artefactos
5. Re-ejecutar con **Run workflow** si es necesario

### Semgrep local (Docker)
```bash
docker run --rm -v "${PWD}:/src" returntocorp/semgrep semgrep scan \
  --config p/security-audit --config p/owasp-top-ten \
  --json --output /src/reports/semgrep-results.json \
  --sarif-output /src/reports/semgrep-results.sarif \
  /src/app /src/server.js /src/config
```

### SBOM local (Syft)
```bash
docker run --rm -v "${PWD}:/src" -w /src anchore/syft:latest dir:. -o cyclonedx-json=sbom.cyclonedx.json
```

### SCA local (Dependency-Check)
```bash
docker run --rm \
  -v "${PWD}:/src" \
  -v dependency-check-data:/usr/share/dependency-check/data \
  owasp/dependency-check:latest \
  --scan /src --project "OWASP NodeGoat" \
  --format HTML --format JSON \
  --out /src/reports/dependency-check \
  --failOnCVSS 7 --enableExperimental \
  --nvdDatafeed "https://dependency-check.github.io/DependencyCheck_Builder/nvd_cache/nvdcve-{0}.json.gz"
```

### Quality Gate local
```bash
python scripts/quality_gate.py \
  --semgrep reports/semgrep-results.json \
  --dependency-check reports/dependency-check/dependency-check-report.json \
  --threshold 7.0 \
  --output evidencias/quality-gate-resumen.md
```

## Artefactos

| Nombre en Actions | Contenido |
|-------------------|-----------|
| `semgrep-results` | JSON + SARIF Semgrep |
| `dependency-check-reports` | HTML/JSON SCA |
| `sbom-cyclonedx` | `sbom.cyclonedx.json` + snippets |
| `quality-gate-summary` | Resumen PASSED/FAILED |

## Evidencias
Ver carpeta `evidencias/` y `evidencias/CAPTURAS_REQUERIDAS.md`.

## Seguridad
- Solo análisis del repositorio / laboratorio
- Sin ataques a sistemas externos
- Sin credenciales ni API keys en el código (usar GitHub Secrets)
