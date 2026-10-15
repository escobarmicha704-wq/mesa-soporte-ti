# Tablero GitHub Projects · plan día por día

Complementa la sección 2 de `GUIA_PASO_A_PASO.md`. Referencias: T01…T31 son las fichas de `backlog.csv`.

> ⚠️ **Fechas reales.** GitHub guarda la fecha real de cada movimiento de ficha y de cada commit; no se puede ni se debe cambiar. Este plan asume que empiezas el 29-09 **si de verdad trabajas esos días**. Si lo ejecutas en otras fechas (por ejemplo, comprimido en pocos días), hazlo igual en el mismo orden, pero declara en el informe las fechas reales. No presentes como hecho el 29-09 algo que hiciste después.

---

## 0. Ajuste previo al tablero: un campo más
Agrega al proyecto el campo **Horas reales** (tipo Number). Sirve para el reporte «planificado vs. real» (comparas con *Estimación (h)*).

## 1. Rutina que se repite cada día de trabajo (10 minutos en total)
**Al empezar**
1. Lee el traspaso del día anterior (plantilla 11.3 de la guía) y pasa las fichas del día de *Backlog* a **Por hacer**.
2. Toma **una** ficha, muévela a **En curso** y asígnate (Assignees: Michael Mejia).

**Mientras trabajas**
3. Cada commit lleva el número de la ficha: `feat: registrar ticket (#16)`.
4. Si algo te frena de verdad: mueve la ficha a **Bloqueado** y llena *Causa / Acción*. Cuando se libere, vuelve a **En curso**.

**Al terminar cada ficha**
5. Muévela a **En revisión/pruebas** (la revisas con el «sombrero» de QA o con la checklist 11.4).
6. Si pasa la revisión: llena **Evidencia** (enlace al commit, documento o captura), **Horas reales**, **Resolución = Terminada** y muévela a **Hecho**.

**Al cerrar el día**
7. Captura de pantalla del **Tablero** con la fecha visible (hora del sistema o nombre del archivo con fecha), y otra de la **Tabla**.
8. Escribe el traspaso al siguiente sombrero y súbelo a `docs/traspasos/`.

Regla de oro: no pases nada a **Hecho** sin Evidencia.

---

## 2. Día 1 · 29-09 · H1 Inicio y planificación (sombrero: Líder y Control)
| Orden | Acción en el tablero | Ficha |
|---|---|---|
| 1 | Crear el repo y el proyecto; configurar columnas y campos (guía 2.1–2.2) | T02, T03 |
| 2 | Cargar las 31 fichas en **Backlog** (script o manual); completar Prioridad, Fecha objetivo, Estimación, Hito, Rol y Tipo | todas |
| 3 | Pasar a **Por hacer** las 7 fichas del día | T01–T07 |
| 4 | Trabajar en este orden: T02 → T03 → T01 → T04 → T05 → T06 → T07 (cada una con la rutina de arriba) | T01–T07 |
| 5 | Crear una ficha de **riesgo** (Tipo Riesgo/Imprevisto) con los riesgos de la guía 4.5 que consideres reales, p. ej. «sobrecarga por equipo unipersonal», con *Causa / Acción* | nueva |

**Evidencia que subes a la ficha:** T01 → `docs/H1_minuta.md`; T02 → enlace del repo; T03 → captura del tablero; T04 → lista de historias; T05 → imagen del modelo conceptual; T06 → foto del boceto; T07 → cronograma preliminar.

**Estado esperado al cierre del día**
| Backlog | Por hacer | En curso | Revisión | Hecho | Bloqueado |
|---|---|---|---|---|---|
| 17 | 7 (T08–T14, movidas al final del día) | 0 | 0 | 7 (T01–T07) | 0 |

**Entregas del hito:** captura del tablero + enlace del repo + minuta (`docs/H1_minuta.md`).
**Traspaso H1 → H2:** terminado T01–T07; en curso nada; bloqueos si los hubo; decisión pendiente: confirmar alcance v1.0.

---

## 3. Día 2 · 30-09 · H2 Línea base (sombrero: Datos, Calidad y Pruebas)
| Orden | Acción | Ficha |
|---|---|---|
| 1 | Leer el traspaso H1→H2; mover T08–T14 a **Por hacer** | — |
| 2 | Alcance v1.0 y backlog priorizado: reordena el tablero por Prioridad y marca Alta/Media/Baja revisadas | T08 |
| 3 | EDT en `docs/` (guía 4.1) | T09 |
| 4 | Recursos, horas y costo (guía 4.2–4.3) | T10 |
| 5 | ER + `schema.sql` (commit `feat(datos): modelo ER y script inicial (#11)`) | T11 |
| 6 | Wireframes de 3 pantallas | T12 |
| 7 | Arquitectura preliminar + revisión cruzada de D1–D4: la ficha T13 pasa por **En revisión/pruebas** y ahí aplicas la checklist 11.4 (Datos revisa, Líder valida) | T13 |
| 8 | Plan de pruebas inicial con los casos CP-01…CP-10 | T14 |
| 9 | Si cambiaste algo del alcance respecto a v0.1, deja la ficha afectada con **Resolución = Replanificada** y anota el motivo | si aplica |

**Evidencia:** T08 → alcance v1.0; T09 → EDT; T10 → tabla de horas/costos; T11 → PNG del ER + commit de `schema.sql`; T12 → imágenes; T13 → documento de arquitectura; T14 → plan de pruebas.

**Estado esperado al cierre**
| Backlog | Por hacer | En curso | Revisión | Hecho | Bloqueado |
|---|---|---|---|---|---|
| 10 | 7 (T15–T21, movidas al final) | 0 | 0 | 14 | 0 |

**Entregas del hito:** tablero actualizado + diagrama ER + planificación v1.0 (no se entregan aún como informe; se guardan para los capítulos 5, 6 y 8).
**Traspaso H2 → H3:** terminado T08–T14; decisiones D1–D4 validadas; para Desarrollo: construir RF-01 a RF-04 primero.

---

## 4. Día 3 · 06-10 · H3 MVP funcional v0.1 (sombrero: Solución y Desarrollo)
| Orden | Acción | Ficha |
|---|---|---|
| 1 | Leer el traspaso; mover T15–T21 a **Por hacer** | — |
| 2 | Entorno y estructura base Flask + SQLite | T15 |
| 3 | RF-01/RF-02 registrar solicitud | T16 |
| 4 | RF-03 listar | T17 |
| 5 | RF-04 asignar responsable y cambiar estado | T18 |
| 6 | `seed.sql` con datos de prueba | T19 |
| 7 | Ejecutar `python -m unittest -v test_app` y probar a mano; **cada defecto real** = una ficha nueva (Tipo Tarea, etiqueta `defecto`, estado Por hacer/En curso) | T20 + D-xx |
| 8 | Reporte de Avance N.º 1: planificado vs. real usando *Estimación* y *Horas reales* (plantilla 11.1) | T21 |
| 9 | Cualquier tarea que no alcances a terminar: **Resolución = Replanificada** y moverla al día siguiente | si aplica |

**Evidencia:** T15–T18 → commits (hash) y capturas de la app; T19 → commit de `seed.sql`; T20 → salida de `unittest` y tabla de defectos; T21 → `docs/Reporte_Avance_1.md`.
**Commits:** usa prefijos distintos según el sombrero: `feat:` (desarrollo), `test:`/`docs(datos):` (QA), `docs(gestión):` (líder).

**Estado esperado al cierre** (sin contar fichas de defectos)
| Backlog | Por hacer | En curso | Revisión | Hecho | Bloqueado |
|---|---|---|---|---|---|
| 3 | 6 (T22–T27, movidas al final) | 0 | 0 | 21 | 0 |

**Entregas del hito:** demo parcial (abrir app → registrar → guardar en BD → listar → asignar responsable → cambiar estado) + Reporte N.º 1 + captura del tablero + evidencia de pruebas/defectos.
**Traspaso H3 → H4:** terminado RF-01 a RF-04; defectos abiertos: lista; decisión: agregar filtros y resumen, validar y cerrar defectos.

---

## 5. Día 4 · 07-10 · H4 Integración, QA y control (los tres roles)
| Orden | Acción | Ficha |
|---|---|---|
| 1 | Mover T22–T27 a **Por hacer**; dividir la jornada en bloques: Desarrollo → QA → Líder | — |
| 2 | RF-05 filtros | T22 |
| 3 | RF-06 resumen | T23 |
| 4 | Validaciones y manejo de errores | T24 |
| 5 | Integración completa, pruebas, corrección y **retest** de cada defecto (ficha del defecto: Por hacer → En curso → En revisión/pruebas → Hecho) | T25 + D-xx |
| 6 | **Cambio/imprevisto real:** crear la ficha (Tipo **Cambio** o **Riesgo/Imprevisto**), completar *Causa / Acción*; usar la plantilla 11.2; actualizar alcance y cronograma si corresponde | T26 |
| 7 | Reporte de Avance N.º 2 | T27 |
| 8 | Etiquetar como **Descartada** o **Replanificada** lo que no se hará; commit y tag `v0.9` | — |

**Sobre el cambio/imprevisto:** solo documenta uno que de verdad ocurrió durante tu trabajo (por ejemplo, un requisito que reinterpretaste, un fallo de entorno o menos horas disponibles). Si no ocurrió ninguno, coméntalo con tu docente en vez de inventarlo.

**Estado esperado al cierre**
| Backlog | Por hacer | En curso | Revisión | Hecho | Bloqueado |
|---|---|---|---|---|---|
| 0 | 4 (T28–T31, movidas al final) | 0 | 0 | 27 | 0 |

**Entregas del hito:** MVP v0.9 (tag) + registro del cambio + Reporte N.º 2 + matriz/capturas de pruebas.

---

## 6. Día 5 · 13-10 · FINAL (integración, cierre y entrega)
| Orden | Acción | Ficha |
|---|---|---|
| 1 | README y prueba en carpeta limpia (guía 10.5) | T28 |
| 2 | Informe final: 15 secciones, capturas H1→H4 en la sección 9 | T29 |
| 3 | Matriz de rotación y contribuciones, firmada | T30 |
| 4 | Presentación y ensayo de la demo | T31 |
| 5 | **Vista «Cierre»**: revisa que *toda* ficha tenga Resolución (Terminada / Pendiente / Descartada / Replanificada) | todas |
| 6 | Tag `v1.0`, captura final del tablero y de la vista Cierre; si la vista tiene opción de exportar, descarga la tabla (si no, captura) | — |

**Estado esperado al cierre:** 31 fichas en **Hecho** (salvo las que justificadamente quedaron *Descartada/Replanificada*), 0 en Bloqueado.
**Entregas:** informe + enlace del repo + enlace del tablero + presentación/demo + paquete de la guía 10.1.

---

## 7. Qué NO debe pasar
- Todas las fichas movidas a **Hecho** el mismo día al final (se nota en el historial).
- Fichas en **Hecho** sin *Evidencia*.
- Ningún **Bloqueado** ni **Riesgo/Imprevisto** en todo el proyecto: el enunciado pide al menos uno «si ocurre», con causa y acción; si de verdad no ocurrió, explícalo en el informe.
- Commits sin referencia a fichas: pierdes trazabilidad tarea ↔ código.
