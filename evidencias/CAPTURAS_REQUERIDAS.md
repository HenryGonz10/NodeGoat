# Capturas requeridas para el informe

Tomar las capturas directamente desde GitHub Actions del repositorio `HenryGonz10/NodeGoat`.

## Secuencia
1. Publicar primero el Commit 1 (`cfadd2d`) y esperar el workflow en **FAILED**.
2. Tomar capturas 1, 2 y 3.
3. Publicar el Commit 2 (remediación) y esperar **SUCCESS**.
4. Tomar capturas 4 y 5.

---

### Captura 1 — Workflow en estado FAILED
**Ubicación:** GitHub → Actions → `DevSecOps Pipeline - SAST SCA SBOM Quality Gate` → ejecución del Commit 1

Debe verse:
- Nombre del workflow
- Identificador/fecha de la ejecución
- Estado **FAILED**
- Jobs: SAST, SCA, SBOM y Quality Gate

### Captura 2 — Detalle del hallazgo que provoca el fallo
**Ubicación:**
- Job **Quality Gate** → log con `QUALITY GATE: FAILED` y los hallazgos Semgrep ERROR (`eval` en `contributions.js`)
- Alternativa: resumen del job SAST o contenido de `semgrep-results.json`

### Captura 3 — Artefactos generados
**Ubicación:** misma ejecución FAILED → sección **Artifacts**

Debe verse:
- `semgrep-results`
- `dependency-check-reports`
- `sbom-cyclonedx`
- (opcional) `quality-gate-summary`

### Captura 4 — Workflow en estado SUCCESS
**Ubicación:** Actions → ejecución posterior a la remediación

Debe verse el workflow en **SUCCESS**.

### Captura 5 — Detalle de jobs exitosos
**Ubicación:** run SUCCESS abierto

Debe verse la lista de jobs en verde, incluyendo **Quality Gate** con `QUALITY GATE: PASSED`.

---

## Recomendaciones
- Usar ventana completa del navegador (repo + workflow visibles).
- Incluir en el informe la URL de cada ejecución.
- No alterar las capturas para cambiar el estado FAILED/SUCCESS.
