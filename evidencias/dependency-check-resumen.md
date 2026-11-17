# Resumen SCA — OWASP Dependency-Check

## Herramienta
- OWASP Dependency-Check (Docker `owasp/dependency-check:latest`)
- Política: `--failOnCVSS 7`

## Incidente NVD (real) y solución

| | |
|--|--|
| **Qué ocurrió** | Fallo fatal: `Error updating the NVD Data` / `Invalid API Key, length of 0` |
| **Por qué** | Sin `NVD_API_KEY`, el modo API de Dependency-Check rechaza la clave vacía y no puede inicializar la BD NVD (`No documents exist`) |
| **Solución correcta** | 1) Configurar secret `NVD_API_KEY` (https://nvd.nist.gov/developers/request-an-api-key), **o** 2) Usar `--nvdDatafeed` con mirror JSON 2.0 del proyecto Dependency-Check (implementado en el workflow como fallback) |

## Resultado real de análisis local (con datafeed mirror)

- Dependencias reportadas: **37**
- Vulnerabilidades con **CVSS >= 7.0**: **54**
- Exit code herramienta: **15** (fallo por política `--failOnCVSS 7`)
- Reportes generados: `dependency-check-report.html`, `dependency-check-report.json`

### Ejemplos del reporte

| Paquete | Advisory | CVSS |
|---------|----------|------|
| `marked@0.3.5` | GHSA-5v2h-r2cx-5xgj | 7.5 |
| `marked@0.3.5` | GHSA-x5pg-88wf-qq4p | 7.5 |
| `marked@0.3.5` | GHSA-rrrm-qjm4-v8hf | 7.5 |
| `bson@1.0.9` | GHSA-v8w9-2789-6hhr | 9.8 |
| `mongodb@2.2.36` | GHSA-mh5c-679w-hh4r | 10.0 |
| `decode-uri-component@0.2.0` | GHSA-qr28-fpjm-wq7f | 10.0 |
| `underscore@1.9.1` | GHSA-cf4h-3jhx-xvhq | 9.8 |
| `body-parser@1.18.3` | GHSA-27r3-jxmh-p828 | 7.5 |

## Interpretación
NodeGoat incorpora componentes antiguos de forma intencional (A9). Con umbral CVSS ≥ 7 el job SCA **debe fallar** en el estado inicial y contribuir a `QUALITY GATE: FAILED`.

## Artefacto GHA
- Nombre: `dependency-check-reports`
- Ruta: `reports/dependency-check/`
