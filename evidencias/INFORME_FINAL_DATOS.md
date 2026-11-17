# Datos para el informe universitario

> Incluir únicamente resultados obtenidos de ejecuciones reales (local y/o GitHub Actions).

---

### Resumen ejecutivo
Se implementó un pipeline DevSecOps sobre OWASP NodeGoat (aplicación de entrenamiento deliberadamente vulnerable) usando GitHub Actions. El flujo integra SAST con Semgrep, SCA con OWASP Dependency-Check, SBOM CycloneDX con Syft y un Quality Gate que falla ante hallazgos Semgrep ERROR o vulnerabilidades SCA con CVSS ≥ 7.0. El objetivo es demostrar el ciclo hallazgo → FAILED → remediación → SUCCESS.

---

### SAST
- **Herramienta:** Semgrep
- **Configuración:** `p/security-audit` + `p/owasp-top-ten`; artefactos JSON y SARIF
- **Hallazgos fase inicial:**
  - Total: **16** | ERROR: **3** | WARNING: **13**
  - Regla: `javascript.lang.security.audit.code-string-concat.code-string-concat`
  - Archivo: `app/routes/contributions.js` líneas 32–34 (`eval`)
- **Interpretación:** A1 Injection; provoca `QUALITY GATE: FAILED`
- **URL run FAILED:** ____________________________________
- **URL run SUCCESS:** ____________________________________

---

### SCA
- **Herramienta:** OWASP Dependency-Check (`--failOnCVSS 7`)
- **Incidente NVD:** sin API key → `Invalid API Key` / fallo de update; solución: `NVD_API_KEY` o `--nvdDatafeed`
- **npm audit:** critical 39, high 67, total 146
- **Dependency-Check fase inicial:** 37 dependencias; **54** hallazgos CVSS ≥ 7; exit 15
- Ejemplos: `marked@0.3.5` (GHSA CVSS 7.5), `mongodb@2.2.36` (CVSS 10.0), `bson@1.0.9` (CVSS 9.8)

---

### SBOM
- CycloneDX JSON, `specVersion` 1.7, **422** componentes
- Ejemplo: `marked@0.3.5` en `evidencias/sbom-componente-ejemplo.json`

---

### Quality Gate
- Criterio: Semgrep ERROR → FAIL; CVSS ≥ 7 → FAIL
- **Primer resultado:** FAILED (3 ERROR + 54 SCA)
- Remediación y segundo resultado: ver Commit 2 / `02_remediacion.md` / `03_estado_final.md`

---

### Conclusiones
1. El Quality Gate convierte hallazgos SAST/SCA en una decisión de liberación reproducible.
2. NodeGoat permite demostrar A1 y A9 de forma controlada.
3. SCA depende de disponibilidad NVD/datafeed; los fallos deben documentarse.
4. El SBOM aporta inventario verificable de componentes.
5. El ciclo FAILED → remediación → SUCCESS valida el control preventivo del pipeline.
