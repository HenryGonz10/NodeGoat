# Datos para el informe universitario

> Incluir únicamente resultados obtenidos de ejecuciones reales (local y/o GitHub Actions).

---

### Resumen ejecutivo
Se implementó un pipeline DevSecOps sobre OWASP NodeGoat (aplicación de entrenamiento deliberadamente vulnerable) usando GitHub Actions. El flujo integra análisis estático de código (SAST) con Semgrep, análisis de composición de software (SCA) con OWASP Dependency-Check, generación de SBOM CycloneDX con Syft y un Quality Gate explícito que falla ante hallazgos Semgrep de severidad ERROR o vulnerabilidades SCA con CVSS ≥ 7.0. El objetivo académico es demostrar el ciclo hallazgo → Quality Gate FAILED → remediación controlada → revalidación → SUCCESS, sin atacar sistemas externos y conservando el carácter educativo de NodeGoat.

---

### SAST
- **Herramienta:** Semgrep
- **Configuración:** reglas `p/security-audit` + `p/owasp-top-ten`; artefactos JSON y SARIF
- **Hallazgos (fase inicial):**
  - Total: **16**
  - ERROR: **3** (bloquean Quality Gate)
  - WARNING: **13**
  - Regla ERROR: `javascript.lang.security.audit.code-string-concat.code-string-concat`
  - Archivo: `app/routes/contributions.js` líneas **32, 33, 34**
  - Patrón: `eval(req.body.preTax|afterTax|roth)` → inyección SSJS
- **Interpretación:** evidencia de A1 Injection intencional de NodeGoat; suficiente para `QUALITY GATE: FAILED` en estado inicial.
- **Resultado post-remediación:** 0 hallazgos ERROR (PASS)
- **URL run FAILED:** ____________________________________
- **URL run SUCCESS:** ____________________________________

---

### SCA
- **Herramienta:** OWASP Dependency-Check (`--failOnCVSS 7`)
- **Incidente NVD observado:**
  - **Qué:** fallo al actualizar NVD (`Error updating the NVD Data`)
  - **Por qué:** sin `NVD_API_KEY`, el cliente NVD API rechaza clave vacía
  - **Solución:** (1) secret `NVD_API_KEY`, o (2) `--nvdDatafeed` con mirror JSON 2.0
- **Referencia `npm audit`:**
  - critical: **39**, high: **67**, moderate: 32, low: 8, total: **146**
- **Dependency-Check (fase inicial, datafeed mirror):**
  - Dependencias: **37**
  - Hallazgos CVSS ≥ 7.0: **54**
  - Exit code: **15**
  - Ejemplos:
    - `marked@0.3.5` → GHSA-5v2h-r2cx-5xgj (7.5), GHSA-x5pg-88wf-qq4p (7.5), GHSA-rrrm-qjm4-v8hf (7.5)
    - `mongodb@2.2.36` → GHSA-mh5c-679w-hh4r (10.0)
    - `bson@1.0.9` → GHSA-v8w9-2789-6hhr (9.8)
    - `underscore@1.9.1` → GHSA-cf4h-3jhx-xvhq (9.8)
- **Interpretación:** dependencias antiguas intencionales (A9); el umbral CVSS ≥ 7 contribuye al fallo del gate en la fase inicial.

---

### SBOM
- **Herramienta:** Anchore Syft
- **Formato:** CycloneDX JSON
- **Versión observada:** `specVersion` **1.7**, `bomFormat` **CycloneDX**
- **Componentes:** **422**
- **Ejemplo:** `evidencias/sbom-componente-ejemplo.json`
  - name: `marked`
  - version: `0.3.5`
  - type: `library`
  - purl: `pkg:npm/marked@0.3.5`
- **Campos verificados:** `bomFormat`, `specVersion`, `metadata`, `components`

---

### Quality Gate
- **Criterio:**
  - Semgrep severity ERROR → FAIL
  - Dependency-Check CVSS ≥ 7.0 → FAIL
- **Primer resultado:** **FAILED**
  - Semgrep: 3 ERROR (`eval` en `contributions.js`)
  - SCA: 54 vulnerabilidades CVSS ≥ 7
- **Corrección:** `eval`→`parseInt`; `marked` 0.3.5→4.3.0; suppressions A9 documentadas
- **Segundo resultado (local):** **PASSED**
- **Segundo resultado (GitHub Actions):** registrar URL tras ejecución SUCCESS

---

### Conclusiones
1. Un Quality Gate explícito convierte hallazgos SAST/SCA en una decisión de liberación reproducible.
2. NodeGoat permite demostrar A1 (injection vía `eval`) y A9 (componentes inseguros) de forma controlada.
3. La operatividad de SCA depende de fuentes de vulnerabilidad (NVD API key o datafeed); los fallos de disponibilidad deben documentarse.
4. El SBOM CycloneDX aporta inventario verificable de componentes para trazabilidad.
5. El ciclo FAILED → remediación → SUCCESS evidencia el valor del pipeline como control preventivo.
