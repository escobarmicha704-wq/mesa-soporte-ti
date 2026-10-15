# Guía paso a paso · Evaluación 3 «Mesa de Soporte TI»

**Integrante:** Michael Mejia (equipo de 1 persona) · **Herramienta de control:** GitHub Projects (Kanban) · **Stack:** Python + Flask + SQLite

> **Cómo usar esta guía:** sigue las secciones en orden. Cada hito (H1 → FINAL) indica qué hacer, qué evidencia guardar y qué rol responde. El código del MVP ya está en este repositorio y pasa 10 pruebas automáticas; tu trabajo es **ejecutar el proceso de gestión de verdad** (tablero, commits, reportes) y registrar la evidencia.

> ⚠️ **Sobre las fechas y la evidencia.** El enunciado exige que el tablero muestre cambios de estado durante el proyecto («no se acepta crear el tablero al final») y la nota 4 penaliza no poder demostrar la gestión progresiva. Las fechas de H1–H4 (29-09 a 07-10) y la entrega (13-10) son anteriores a hoy (14-10). **No retrocedas fechas ni inventes historial**: las capturas y commits deben reflejar lo que realmente hiciste, con sus fechas reales. Si ya tenías tablero o commits de esos días, úsalos. Si no, habla con el docente para acordar fecha/forma de entrega y explica en el informe (sección 10) la desviación real: es un dato legítimo de «planificado vs. real» y puede jugar a tu favor si está bien documentado.

---

## Índice
1. [Propuesta de solución](#1-propuesta-de-solución)
2. [Configuración de GitHub y del tablero](#2-configuración-de-github-y-del-tablero)
3. [Backlog inicial (31 tareas)](#3-backlog-inicial)
4. [EDT, recursos, horas y costos](#4-edt-recursos-horas-y-costos)
5. [Roles y rotación con una sola persona](#5-roles-y-rotación-con-una-sola-persona)
6. [Hito H1 · Inicio y planificación (29-09)](#6-h1--inicio-y-planificación-29-09)
7. [Hito H2 · Línea base (30-09)](#7-h2--línea-base-30-09)
8. [Hito H3 · MVP funcional v0.1 (06-10)](#8-h3--mvp-funcional-v01-06-10)
9. [Hito H4 · Integración, QA y control (07-10)](#9-h4--integración-qa-y-control-07-10)
10. [Entrega FINAL (13-10)](#10-entrega-final-13-10)
11. [Plantillas](#11-plantillas)
12. [Checklist maestro](#12-checklist-maestro)

---

## 1. Propuesta de solución

### 1.1 Problema y objetivo
**Problema:** la organización recibe requerimientos de soporte por correo, mensajería y conversaciones informales; no hay trazabilidad de responsable, prioridad, estado ni tiempos de atención.

**Objetivo general:** construir un MVP web que permita registrar una solicitud de soporte y seguir su ciclo completo (Nuevo → En proceso → Resuelto → Cerrado) con persistencia en base de datos relacional.

**Objetivos específicos**
1. Centralizar el registro de solicitudes con identificador único y fecha de creación.
2. Permitir asignar responsable y actualizar el estado, dejando historial.
3. Permitir consultar, filtrar y resumir las solicitudes.
4. Gestionar el proyecto con tablero, repositorio, reportes y pruebas trazables.

### 1.2 Alcance
| Dentro del MVP v1.0 | Fuera del alcance (v1.0) |
|---|---|
| RF-01 a RF-06 completos | Autenticación/login y perfiles de usuario |
| BD relacional con usuarios, categorías, tickets e historial | Notificaciones por correo |
| Validaciones, manejo de errores, pruebas funcionales | Medición automática de SLA / tiempos de atención |
| Interfaz web simple (3 pantallas) | Adjuntar archivos, comentarios en tickets |
| Historial de cambios de estado y responsable | Reportes gráficos, exportación, multi-organización |

### 1.3 Requisitos (historias) y criterios de aceptación
| ID | Historia | Criterio de aceptación |
|---|---|---|
| RF-01 | Como solicitante quiero registrar una solicitud con solicitante, título, descripción, categoría y prioridad. | Con datos válidos se guarda; con datos inválidos se muestra el error y no se guarda. |
| RF-02 | Como técnico quiero que cada solicitud tenga id único y fecha de creación. | Se genera `TCK-000N` y la fecha automáticamente; no se repiten. |
| RF-03 | Como técnico quiero listar solicitudes viendo estado, prioridad y responsable. | El listado muestra las tres columnas para cada ticket (— si no hay responsable). |
| RF-04 | Como técnico quiero asignar responsable y cambiar el estado (Nuevo, En proceso, Resuelto, Cerrado). | El cambio persiste y queda en el historial; no se avanza de «Nuevo» sin responsable. |
| RF-05 | Como técnico quiero filtrar por estado, prioridad o categoría. | Cada filtro (solo o combinado) devuelve únicamente los tickets que coinciden. |
| RF-06 | Como jefe de TI quiero un resumen del total y por estado. | Las tarjetas muestran total y conteo por cada uno de los 4 estados. |
| BD-01 | Como organización quiero que los datos se guarden de forma permanente. | Tras reiniciar la app, los tickets siguen en la BD. |
| CAL-01 | Como usuario quiero mensajes claros ante errores. | Validaciones de formulario, páginas 404/500 y evidencia de pruebas. |

### 1.4 Arquitectura (3 capas, intencionalmente pequeña)
```
 Navegador ──HTTP──► Flask (app.py)
                      ├─ Rutas / controladores: "/", "/tickets/nuevo", "/tickets/<id>"
                      ├─ Validaciones (validar_ticket, estados, responsable)
                      └─ Plantillas Jinja2 (templates/*.html) + CSS
                              │ SQL (sqlite3)
                              ▼
                        SQLite: mesa.db  ← creada con schema.sql (+ seed.sql)
```
**Justificación de la tecnología (exigida por el enunciado):** Python + Flask requiere muy poco código y nada de compilación; SQLite es una BD relacional completa sin instalar un servidor; HTML/Jinja2 evita un frontend aparte; `unittest` viene con Python. Es la combinación más corta que cumple «frontend + lógica + BD relacional» y es reproducible con `pip install -r requirements.txt`.

**Decisiones de arquitectura (para la revisión cruzada):**
| # | Decisión | Propone | Revisa | Valida |
|---|---|---|---|---|
| D1 | Flask + SQLite en lugar de Django/MySQL (menos configuración) | Solución y Desarrollo | Datos, Calidad y Pruebas | Líder y Control |
| D2 | Estados y prioridades como restricción `CHECK` en la BD **y** validación en la app | Datos, Calidad y Pruebas | Solución y Desarrollo | Líder y Control |
| D3 | Tabla `historial_cambios` para «cambios relevantes» (BD-01) | Datos, Calidad y Pruebas | Solución y Desarrollo | Líder y Control |
| D4 | Sin login: fuera de alcance por plazo | Líder y Control | Solución y Desarrollo | Datos, Calidad y Pruebas |

### 1.5 Modelo de datos (ER)
```
usuarios (id PK, nombre UNIQUE, email UNIQUE)
categorias (id PK, nombre UNIQUE)
tickets (id PK, codigo UNIQUE, solicitante, titulo, descripcion,
         categoria_id FK→categorias, prioridad CHECK, estado CHECK,
         responsable_id FK→usuarios NULL, fecha_creacion)
historial_cambios (id PK, ticket_id FK→tickets, campo, valor_antes, valor_nuevo, fecha)

Relaciones: categorias 1─N tickets · usuarios 1─N tickets · tickets 1─N historial_cambios
```
El script real está en `schema.sql`. Para el informe, dibuja el diagrama ER en **draw.io** o **dbdiagram.io** (pega las tablas de arriba) y expórtalo como PNG.

### 1.6 Interfaces (wireframes a dibujar en H2)
Dibuja 3 pantallas en papel/Excalidraw/draw.io; la app ya implementa este diseño:
1. **Listado (`/`)**: barra con tarjetas de resumen (Total, Nuevo, En proceso, Resuelto, Cerrado) · fila de filtros (estado, prioridad, categoría) · tabla de tickets.
2. **Nueva solicitud (`/tickets/nuevo`)**: formulario con los 5 campos y botón «Registrar».
3. **Detalle (`/tickets/<id>`)**: ficha del ticket · selectores de responsable y estado · historial de cambios.

---

## 2. Configuración de GitHub y del tablero

### 2.1 Repositorio (obligatorio)
1. En github.com → **New repository** → nombre `mesa-soporte-ti` → *Private* o *Public* (si es privado, agrega al docente como colaborador) → marca *Add a README*.
2. En tu PC:
   ```bash
   git clone https://github.com/<tu-usuario>/mesa-soporte-ti.git
   cd mesa-soporte-ti
   git config user.name  "Michael Mejia"
   git config user.email "<tu correo de GitHub>"
   ```
3. Copia aquí los archivos de este proyecto y haz el primer commit:
   ```bash
   git add .
   git commit -m "feat: estructura inicial del proyecto"
   git push origin main
   ```

### 2.2 Proyecto (tablero Kanban)
1. En el perfil o en el repo → pestaña **Projects** → **New project** → plantilla **Board** (Kanban) → nombre `Mesa de Soporte TI`.
2. Abre el proyecto → **Settings** (⚙) → vincula el repositorio (**Manage access / Link a repository**).
3. **Columnas (campo Status).** En *Settings → Fields → Status* deja exactamente estas 6 opciones, en este orden:

   | Orden | Columna |
   |---|---|
   | 1 | Backlog |
   | 2 | Por hacer |
   | 3 | En curso |
   | 4 | En revisión/pruebas |
   | 5 | Hecho |
   | 6 | Bloqueado |

4. **Campos personalizados** (*Settings → New field*). Cada tarea debe tener responsable, prioridad, fecha objetivo, estimación y evidencia:

   | Campo | Tipo | Valores / uso |
   |---|---|---|
   | **Assignees** (nativo) | — | Michael Mejia (responsable) |
   | Prioridad | Single select | Alta · Media · Baja |
   | Fecha objetivo | Date | fecha límite de la tarea |
   | Estimación (h) | Number | horas estimadas |
   | Evidencia | Text | enlace al commit, captura o documento |
   | Hito | Single select | H1 · H2 · H3 · H4 · FINAL |
   | Rol | Single select | Líder y Control · Solución y Desarrollo · Datos, Calidad y Pruebas |
   | Tipo | Single select | Historia · Tarea · Riesgo/Imprevisto · Cambio |
   | Resolución | Single select | Terminada · Pendiente · Descartada · Replanificada |
   | Causa / Acción | Text | solo para Bloqueado y Riesgo/Imprevisto |

5. **Vistas** (pestañas del proyecto; son evidencia de cada hito):
   - **Tablero** (Board, agrupado por Status) → la captura principal de cada hito.
   - **Tabla** (Table) con columnas: Título, Assignees, Status, Prioridad, Fecha objetivo, Estimación, Hito, Rol, Evidencia.
   - **Cierre** (Table, *Group by* Resolución) → la «vista final donde se distingan tareas terminadas, pendientes y descartadas/replanificadas».
   - **Cronograma** (Roadmap, usando Fecha objetivo) → apoya el cronograma del informe.
6. **Insights** (pestaña ~ gráficos): crea un gráfico *Current iteration / Status* y uno de *burn-up* para mostrar avance en el reporte.

### 2.3 Cargar el backlog (31 tareas)
**Opción A (rápida, con `gh`):** instala GitHub CLI, `gh auth login`, y desde la carpeta del repo ejecuta `bash docs/crear_issues.sh`. Luego, en el proyecto: **+ Add item → Add items from repository** y selecciona todos los issues. *(Script generado sin probar contra GitHub; si falla algún comando, usa la opción B.)*
**Opción B (manual):** en el tablero escribe `+ Add item` y copia título/valores desde `docs/backlog.csv` (columnas ya alineadas con los campos del tablero).

Completa en cada tarea: Assignee, Prioridad, Fecha objetivo, Estimación, Hito, Rol y Tipo. Todas empiezan en **Backlog**; las del hito actual pásalas a **Por hacer**.

### 2.4 Reglas de trabajo con el tablero (para que haya trazabilidad real)
- Mueve la ficha **en el momento** (Por hacer → En curso → En revisión/pruebas → Hecho). El historial de GitHub registra la fecha.
- Una tarea solo pasa a **Hecho** cuando tiene el campo *Evidencia* con enlace (commit, PR, captura, documento).
- Si algo te frena, mueve la ficha a **Bloqueado** y completa *Causa / Acción*. Si surge un riesgo o imprevisto, crea una ficha Tipo «Riesgo/Imprevisto».
- Vincula commits con tareas escribiendo `#N` (número de issue) en el mensaje: `feat: registrar ticket (#16)`; cerrar con `closes #16`.
- Convención de commits: `feat:`, `fix:`, `test:`, `docs:`. Un commit por cambio lógico (los commits de cada rol son la evidencia de participación).

---

## 3. Backlog inicial

Fuente completa: `docs/backlog.csv`. Resumen (31 tareas, **50,5 h**):

| ID | Tarea | Rol | Hito | Prio. | Horas |
|---|---|---|---|---|---|
| T01 | Definir problema, objetivo y alcance v0.1 | Líder | H1 | Alta | 1,5 |
| T02 | Crear repositorio Git y README inicial | Desarrollo | H1 | Alta | 0,5 |
| T03 | Crear tablero con columnas y campos | Líder | H1 | Alta | 0,5 |
| T04 | Redactar 6-10 historias/requisitos | Líder | H1 | Alta | 1,5 |
| T05 | Modelo de datos conceptual | Datos/QA | H1 | Media | 1,0 |
| T06 | Boceto inicial de interfaz y arquitectura | Desarrollo | H1 | Media | 1,5 |
| T07 | Cronograma preliminar y minuta H1 | Líder | H1 | Media | 1,0 |
| T08 | Alcance v1.0 y backlog priorizado | Líder | H2 | Alta | 1,5 |
| T09 | EDT | Líder | H2 | Alta | 1,0 |
| T10 | Recursos, horas y costos | Líder | H2 | Alta | 1,5 |
| T11 | Modelo ER + `schema.sql` inicial | Datos/QA | H2 | Alta | 2,0 |
| T12 | Wireframes de 3 pantallas | Desarrollo | H2 | Media | 2,0 |
| T13 | Arquitectura preliminar documentada | Desarrollo | H2 | Media | 1,0 |
| T14 | Plan de pruebas inicial | Datos/QA | H2 | Media | 1,5 |
| T15 | Estructura base Flask + SQLite | Desarrollo | H3 | Alta | 2,0 |
| T16 | RF-01/RF-02 Registrar solicitud | Desarrollo | H3 | Alta | 2,5 |
| T17 | RF-03 Listar solicitudes | Desarrollo | H3 | Alta | 1,5 |
| T18 | RF-04 Asignar responsable y estado | Desarrollo | H3 | Alta | 2,0 |
| T19 | Datos de prueba (`seed.sql`) | Datos/QA | H3 | Media | 1,0 |
| T20 | Pruebas funcionales iniciales y defectos | Datos/QA | H3 | Alta | 2,0 |
| T21 | Reporte de avance N.º 1 | Líder | H3 | Media | 1,5 |
| T22 | RF-05 Filtros | Desarrollo | H4 | Alta | 1,5 |
| T23 | RF-06 Resumen | Desarrollo | H4 | Alta | 1,0 |
| T24 | Validaciones y manejo de errores (CAL-01) | Datos/QA | H4 | Alta | 2,0 |
| T25 | Pruebas de integración, defectos y retest | Datos/QA | H4 | Alta | 2,0 |
| T26 | Análisis y registro del cambio/imprevisto | Líder | H4 | Media | 1,5 |
| T27 | Reporte de avance N.º 2 | Líder | H4 | Media | 1,5 |
| T28 | README de ejecución y reproducibilidad | Desarrollo | FINAL | Alta | 1,0 |
| T29 | Informe final y anexos | Líder | FINAL | Alta | 6,0 |
| T30 | Matriz de rotación y contribuciones | Líder | FINAL | Media | 1,0 |
| T31 | Presentación breve y demo | Líder | FINAL | Alta | 2,5 |

Cumple el mínimo de ≥10 tareas «desglosadas en trabajo verificable»: cada una tiene un entregable concreto que se enlaza como evidencia.

---

## 4. EDT, recursos, horas y costos

### 4.1 EDT (estructura de desglose del trabajo)
```
1. Mesa de Soporte TI
├─ 1.1 Gestión del proyecto
│   ├─ 1.1.1 Planificación (alcance, EDT, cronograma)        T01 T04 T07 T08 T09
│   ├─ 1.1.2 Recursos y costos                               T10
│   ├─ 1.1.3 Control (tablero, reportes, cambios)            T03 T21 T26 T27
│   └─ 1.1.4 Cierre (informe, matriz de roles, demo)         T29 T30 T31
├─ 1.2 Diseño
│   ├─ 1.2.1 Modelo de datos (conceptual, ER)                T05 T11
│   └─ 1.2.2 Interfaces y arquitectura                       T06 T12 T13
├─ 1.3 Construcción
│   ├─ 1.3.1 Repositorio y base técnica                      T02 T15
│   ├─ 1.3.2 Registro y gestión de solicitudes (RF-01..04)   T16 T17 T18
│   └─ 1.3.3 Consulta y resumen (RF-05, RF-06)               T22 T23
└─ 1.4 Calidad
    ├─ 1.4.1 Datos de prueba                                 T19
    ├─ 1.4.2 Plan y ejecución de pruebas                     T14 T20 T25
    ├─ 1.4.3 Validaciones y errores (CAL-01)                 T24
    └─ 1.4.4 Reproducibilidad (README)                       T28
```

### 4.2 Recursos
| Tipo | Recurso | Costo |
|---|---|---|
| Humano | 1 integrante (Michael Mejia) en 3 roles rotativos | por horas (ver 4.3) |
| Técnico | PC personal, Python 3, Flask, SQLite, Git, VS Code | $0 (software libre) |
| Plataforma | GitHub (repo + Projects, plan gratuito) | $0 |
| Otros | Internet, energía (estimación) | incluido en contingencia |

### 4.3 Estimación de horas y costo
**Supuesto (declaralo así en el informe y ajústalo si tu docente indica otro valor):** valor hora de referencia de **$6.000 CLP**.

| Hito | Horas | Costo (CLP) |
|---|---|---|
| H1 · Inicio y planificación | 7,5 | 45.000 |
| H2 · Línea base | 10,5 | 63.000 |
| H3 · MVP v0.1 | 12,5 | 75.000 |
| H4 · Integración y QA | 9,5 | 57.000 |
| FINAL · Entrega | 10,5 | 63.000 |
| **Subtotal** | **50,5 h** | **303.000** |
| Contingencia 10 % | — | 30.300 |
| **Total estimado** | | **333.300** |

Por rol: Líder y Control 22,5 h · Solución y Desarrollo 16,5 h · Datos, Calidad y Pruebas 11,5 h.
En el informe (sección 10) compara estas horas con las **horas reales** que registres.

### 4.4 Cronograma (fechas de referencia del curso)
| Fecha | Hito | Entregable clave |
|---|---|---|
| 29-09 | H1 | Tablero + repo + minuta |
| 30-09 | H2 | Línea base: EDT, ER, wireframes, plan de pruebas |
| 06-10 | H3 | MVP v0.1 (RF-01 a RF-04) + Reporte N.º 1 |
| 07-10 | H4 | MVP v0.9 (RF-05/06) + cambio + Reporte N.º 2 |
| 13-10 | FINAL | MVP v1.0 + informe + demo |

### 4.5 Riesgos iniciales
| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Una sola persona: sobrecarga y sin revisión por pares | Alta | Alta | Revisión cruzada formal entre «sombreros» (checklists de la sección 11) |
| Poco tiempo para desarrollo e informe | Alta | Alta | Alcance mínimo + stack simple; MVP priorizado |
| Fallo de entorno (Python/Flask no instala) | Media | Media | README claro, `requirements.txt`, probar en limpio antes de entregar |
| Pérdida de evidencia del tablero | Media | Alta | Capturas con fecha en cada hito + exportar tabla CSV |

---

## 5. Roles y rotación con una sola persona

La regla del enunciado es que cada integrante ejerza **los tres roles al menos una vez** y que cada cambio tenga traspaso. Con un solo integrante, la forma defendible es: **Michael ocupa un «sombrero» responsable por hito**, sigue la ruta del «Integrante A» de la tabla sugerida, y deja un **traspaso escrito** (sección 11.3) al cambiar de sombrero.

| Fecha | Líder de Proyecto y Control | Solución y Desarrollo | Datos, Calidad y Pruebas |
|---|---|---|---|
| 29-09 (H1) | **Michael Mejia** | — (tareas de apoyo) | — |
| 30-09 (H2) | — | — | **Michael Mejia** |
| 06-10 (H3) | — | **Michael Mejia** | — |
| 07-10 (H4) | Integración conjunta: Michael Mejia (los 3 roles) | | |

*Interpretación:* el «rol responsable del hito» firma el traspaso y responde por el resultado; las tareas de los otros roles dentro del mismo hito quedan marcadas con su campo *Rol* en el tablero (así se ven las tres competencias). Indica en el informe, sin rodeos, que el equipo es unipersonal y que la revisión cruzada se hizo cambiando de sombrero con las listas de verificación. Confirma con tu docente que acepta esta adaptación.

**Revisión cruzada de arquitectura** (obligatoria): para cada decisión de la tabla 1.4, deja registrado: propuesta (Desarrollo) → revisión (Datos/QA, usa la checklist 11.4) → validación (Líder: ¿cabe en alcance, recursos y plazo?). Se registra en `docs/decisiones.md` o como comentarios en el issue.

---

## 6. H1 · Inicio y planificación (29-09)
**Rol responsable:** Líder de Proyecto y Control. **Tareas:** T01–T07. **Tiempo:** ~7,5 h.

**Pasos**
1. Crea el repo y haz el primer commit (sección 2.1) → T02.
2. Crea el proyecto, columnas y campos (sección 2.2) → T03.
3. Escribe en `docs/H1_minuta.md`: problema, objetivo, **alcance v0.1** (qué incluye / qué queda fuera, sección 1.2) → T01.
4. Redacta **6–10 historias/requisitos** (usa la tabla 1.3: RF-01 a RF-06 + BD-01 + CAL-01) → T04.
5. Dibuja el **modelo de datos conceptual** (entidades: Ticket, Usuario, Categoría, Historial) → T05.
6. Haz un **boceto** a mano de la interfaz y el diagrama de arquitectura (sección 1.4) → T06.
7. Cronograma preliminar (tabla 4.4) y minuta del hito → T07.
8. Carga las 31 tareas (sección 2.3). Mueve las de H1 a *Por hacer → En curso → Hecho* a medida que las terminas.

**Evidencia obligatoria (solo evidenciar el inicio, no es informe):** ✅ captura del tablero · ✅ enlace del repositorio · ✅ minuta de hito (`docs/H1_minuta.md`).
**Traspaso a H2:** plantilla 11.3.

---

## 7. H2 · Línea base (30-09)
**Rol responsable:** Datos, Calidad y Pruebas. **Tareas:** T08–T14. **Tiempo:** ~10,5 h.

**Pasos**
1. **Alcance v1.0** y backlog priorizado (Alta/Media/Baja; orden de construcción RF-01→04 en H3, RF-05/06 en H4) → T08.
2. **EDT** (sección 4.1) → T09.
3. **Recursos, estimación de horas y financiera** (4.2 y 4.3) → T10.
4. **Modelo ER + script inicial**: dibuja el ER (1.5) y guarda `schema.sql` en el repo → T11.
5. **Wireframes** de las 3 pantallas (1.6) → T12.
6. **Arquitectura preliminar** (1.4 + decisiones D1–D4 con revisión cruzada) → T13.
7. **Plan de pruebas inicial**: objetivo, alcance, tipos (funcional e integración), criterios de entrada/salida, entorno y la matriz de casos CP-01…CP-10 (sección 11.5) → T14.
8. Cronograma y fechas actualizados (4.4).

**Evidencia obligatoria:** ✅ tablero actualizado (captura) · ✅ diagrama ER · ✅ planificación v1.0 (EDT, horas, costos, cronograma).
*No se entrega aún:* este material alimenta los capítulos **5, 6 y 8** del informe final: guárdalo en `docs/`.

---

## 8. H3 · MVP funcional v0.1 (06-10)
**Rol responsable:** Solución y Desarrollo. **Tareas:** T15–T21. **Tiempo:** ~12,5 h.

**Pasos**
1. Prepara el entorno y ejecuta la app (README): `pip install -r requirements.txt` → `python app.py --init` → `python app.py`.
2. Implementa/confirma por tarea, **con un commit por tarea** referenciando el issue:
   - T15 estructura base + conexión BD · T16 registrar (RF-01/02) · T17 listar (RF-03) · T18 asignar y estado (RF-04) · T19 `seed.sql`.
3. **Commits de los «tres integrantes»:** el enunciado pide commits de cada integrante. Como eres uno, deja commits con tu cuenta en cada «sombrero», usando prefijos claros: `feat:` (desarrollo), `test:`/`docs(datos):` (datos y QA), `docs(gestión):` (líder). Menciónalo en el informe.
4. **Pruebas funcionales iniciales** (T20): ejecuta `python -m unittest -v test_app` y también prueba a mano el flujo. Registra cada defecto encontrado en el tablero (Tipo *Tarea*, etiqueta `defecto`) y en la tabla 11.6.
5. **Reporte de Avance N.º 1** (plantilla 11.1): planificado vs. real, defectos, riesgos y bloqueos (T21).
6. Registra al menos un **Bloqueado o Riesgo** en el tablero si ocurre (causa + acción).

**Demo parcial (practícala antes):** abrir la app → registrar un ticket → ver que se guarda en la BD → verlo en el listado → asignar responsable → cambiar estado.
**Evidencia obligatoria:** ✅ demo · ✅ Reporte de Avance N.º 1 · ✅ captura del tablero · ✅ evidencia de pruebas y defectos (salida de `unittest` + tabla de defectos).
Alimenta los capítulos **9, 10 y 12** del informe.

---

## 9. H4 · Integración, QA y control (07-10)
**Rol:** integración conjunta (los tres roles). **Tareas:** T22–T27. **Tiempo:** ~9,5 h.

**Pasos**
1. RF-05 filtros (T22) y RF-06 resumen (T23).
2. Validaciones y manejo de errores (T24): formulario, estados válidos, responsable obligatorio al avanzar, páginas 404/500.
3. Pruebas funcionales y de **integración** (T25): corre la suite completa, ejecuta la matriz manual (11.5), registra defectos, corrige y haz **retest** (deja cada defecto con estado *Abierto → Corregido → Retest OK*).
4. **Cambio/imprevisto** (T26): documenta **uno real** con la plantilla 11.2. Ejemplos de cambios legítimos *si realmente ocurrieron*: «no avanzar de Nuevo sin responsable» (cambio de regla de negocio), «agregar tabla `historial_cambios` para cumplir BD-01 / "cambios relevantes"», o un imprevisto como un fallo de entorno o menos horas disponibles. Si tuviste un cambio real de alcance/cronograma, actualiza el alcance a v1.0 y el cronograma, y deja la ficha en el tablero (Tipo *Cambio*; estado *Replanificada* si algo se movió).
5. **Reporte de Avance N.º 2** (11.1) (T27).
6. Cierra tareas pendientes; etiqueta como *Descartada/Replanificada* lo que no se hará.

**Evidencia obligatoria:** ✅ MVP v0.9 (tag `v0.9` en Git) · ✅ registro del cambio · ✅ Reporte de Avance N.º 2 · ✅ matriz/capturas de pruebas.
```bash
git tag -a v0.9 -m "MVP v0.9 - integración H4" && git push origin v0.9
```
Alimenta los capítulos **10, 11 y 12**.

---

## 10. Entrega FINAL (13-10)
**Tareas:** T28–T31. **Tiempo:** ~10,5 h.

### 10.1 Paquete a entregar (una carpeta con nombres claros)
```
Entrega_Evaluacion3_Michael_Mejia/
├─ 01_Informe_Final.pdf        (o .docx)
├─ 02_Enlaces.txt              (URL del repositorio + URL del tablero)
├─ 03_Base_de_datos/           schema.sql, seed.sql
├─ 04_Pruebas/                 plan, matriz de casos, registro de defectos/retest, salida de unittest
├─ 05_Presentacion.pdf/.pptx   (breve)
├─ 06_Matriz_Rotacion.pdf      (firmada)
└─ 07_Capturas_Tablero/        H1, H2, H3, H4, final (con fecha) + export CSV
```
Cierra con `git tag -a v1.0 -m "MVP v1.0 entrega final"` y `git push origin v1.0`.

### 10.2 Informe final (12–18 páginas sin portada, índice ni anexos)
Debe **explicar decisiones**, no ser un álbum de capturas. De dónde sale cada capítulo:

| N.º | Sección | Contenido / fuente |
|---|---|---|
| 1 | Portada e identificación | Nombre, asignatura, docente, fecha, enlace al repo |
| 2 | Resumen ejecutivo | 1 página: problema, solución, resultado, horas/costo, estado final |
| 3 | Problema, objetivo y alcance | Secciones 1.1 y 1.2 de esta guía |
| 4 | Requisitos y criterios de aceptación | Tabla 1.3 |
| 5 | Planificación | EDT, backlog, hitos, cronograma (H2) |
| 6 | Recursos H/T/económicos | Secciones 4.2 y 4.3 |
| 7 | Organización, roles y rotación | Sección 5 + matriz firmada + traspasos |
| 8 | Diseño de solución | Arquitectura, wireframes, ER, justificación del stack |
| 9 | Herramienta de control | GitHub Projects: columnas, campos, vistas y evolución del tablero (capturas H1→final) |
| 10 | Reportes de avance | Reportes 1 y 2: planificado vs. real, bloqueos, decisiones |
| 11 | Cambio/imprevisto de H4 | Ficha 11.2 y su efecto en alcance/cronograma |
| 12 | Calidad y pruebas | Casos ejecutados, defectos, retest, resultado del MVP, pendientes |
| 13 | Conclusiones y lecciones | Qué funcionó, qué no, trabajar solo con tres roles, qué mejorarías |
| 14 | Referencias | Documentación de Flask, SQLite, GitHub Projects, enunciado |
| 15 | Anexos | Capturas, enlaces, `schema.sql`, commits, arquitectura, interfaces, pruebas, contribución por rol |

### 10.3 Evidencias del tablero (sección 8 del enunciado)
- ≥10 tareas con responsable y fecha ✔ (31)
- Cambios de estado durante el proyecto (historial real) ✔
- Al menos un elemento **Bloqueado** o **Riesgo/Imprevisto** con causa y acción ✔
- Captura/export del tablero **por hito** ✔
- **Vista «Cierre»** con terminadas / pendientes / descartadas-replanificadas ✔

### 10.4 Presentación y demo (5–7 min)
1. Problema y objetivo (30 s) · 2. Alcance y arquitectura (1 min) · 3. Demo en vivo: registrar → guardar → listar → asignar → cambiar estado → filtrar → resumen (2–3 min) · 4. Tablero y trazabilidad: mostrar historial, commits, reportes (1 min) · 5. Calidad: 10 pruebas, defectos y retest (1 min) · 6. Lecciones y cierre (30 s).
Prepara de antemano: `python app.py --init` para tener datos limpios, y una captura de respaldo por si falla algo.

### 10.5 Verificación de reproducibilidad (haz esto en una carpeta limpia)
```bash
git clone <URL> prueba && cd prueba
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py --init && python -m unittest -v test_app
python app.py   # abrir http://127.0.0.1:5000
```

---

## 11. Plantillas

### 11.1 Reporte de avance (N.º 1 / N.º 2)
```markdown
# Reporte de Avance N.º _  ·  Fecha: __-__-____  ·  Autor/rol: Michael Mejia / ______
## 1. Resumen (2-3 líneas)
## 2. Planificado vs. real
| Tarea | Estimado (h) | Real (h) | Estado | Desvío y motivo |
## 3. Avance global: ___ de 31 tareas Hecho (__ %)  ·  Horas usadas ___ de 50,5
## 4. Defectos (abiertos/cerrados) · ## 5. Riesgos y bloqueos (causa, acción, responsable)
## 6. Decisiones tomadas · ## 7. Plan próximo hito · ## 8. Enlaces (tablero, commits)
```

### 11.2 Registro de cambio/imprevisto (H4)
```markdown
# Cambio/Imprevisto C-01  ·  Fecha: ____
- Descripción: ____  - Tipo: cambio de alcance / imprevisto técnico / de recursos
- Cómo se detectó: ____
- Impacto  → Alcance: ___  Cronograma: ± __ h  Costo: ± $___  Riesgos: ___
- Alternativas evaluadas: A) ___ B) ___  - Decisión y justificación: ____
- Aprobado por (rol Líder y Control): ____
- Acciones: ____ (tareas creadas/replanificadas: #__ )  - Evidencia: commit/captura
```

### 11.3 Traspaso de rol (breve)
```markdown
# Traspaso  ·  De: ______ (rol) → A: ______ (rol)  ·  Fecha: ____
- Qué quedó terminado: ____       - Qué está en curso: ____
- Qué está bloqueado: ____        - Evidencia existente (enlaces): ____
- Decisión que debe continuar el nuevo responsable: ____
```
Guárdalos en `docs/traspasos/` (H1→H2, H2→H3, H3→H4).

### 11.4 Checklist de revisión cruzada
- **Datos/QA revisa lo técnico:** ¿el modelo cubre RF y BD-01? ¿hay claves y restricciones? ¿se puede probar cada requisito? ¿los datos de prueba cubren todos los estados y prioridades?
- **Líder valida:** ¿cabe en alcance v1.0? ¿en las horas y plazo? ¿riesgos nuevos? ¿quedó documentada la decisión?

### 11.5 Matriz de casos de prueba (ya implementados en `test_app.py`)
| Caso | Requisito | Descripción | Resultado esperado |
|---|---|---|---|
| CP-01 | RF-01/02 | Registrar ticket válido | Se guarda con `TCK-0006`, estado Nuevo y fecha |
| CP-02 | RF-01/CAL-01 | Datos inválidos (6 variantes) | Error visible; no se guarda |
| CP-03 | RF-03 | Abrir listado | Se ven estado, prioridad y responsable |
| CP-04 | RF-04 | Asignar responsable + estado | Persiste y deja 2 registros de historial |
| CP-05 | RF-04 | Avanzar sin responsable | Rechazado con mensaje |
| CP-06 | RF-04 | Estado inválido | Rechazado |
| CP-07 | RF-05 | Filtrar por estado/prioridad/categoría | Solo coincidencias |
| CP-08 | RF-06 | Resumen | Total 5; conteos por estado correctos |
| CP-09 | CAL-01 | Ruta/ticket inexistente | Página 404 |
| CP-10 | BD-01 | Persistencia | Registro presente en la BD |

**Resultado de la última ejecución (automática): 10/10 OK.** Agrega a la evidencia la salida de `python -m unittest -v test_app` y una captura de pruebas manuales del navegador.

### 11.6 Registro de defectos
| ID | Fecha | Caso | Descripción | Severidad | Estado | Retest |
|---|---|---|---|---|---|---|
| D-01 | | | | | Abierto/Corregido | OK/Falla |

*(Registra solo los defectos que **realmente** encuentres. Si no hay ninguno, deja constancia de que el retest no halló fallas.)*

### 11.7 Matriz de rotación y contribuciones (va en el informe, firmada)
| Hito | Fecha | Rol responsable | Integrante | Entregables principales | Commits/tareas (#) | Traspaso |
|---|---|---|---|---|---|---|
| H1 | 29-09 | Líder y Control | Michael Mejia | | | |
| H2 | 30-09 | Datos, Calidad y Pruebas | Michael Mejia | | | |
| H3 | 06-10 | Solución y Desarrollo | Michael Mejia | | | |
| H4 | 07-10 | Integración conjunta | Michael Mejia | | | |
Firma: ____________ Michael Mejia

---

## 12. Checklist maestro
**Repositorio:** ☐ commits frecuentes con `#issue` ☐ tags `v0.9` y `v1.0` ☐ README ejecutable ☐ `schema.sql` y `seed.sql`
**Tablero:** ☐ 6 columnas ☐ campos completos ☐ ≥10 tareas ☐ un Bloqueado/Riesgo con causa y acción ☐ capturas H1–H4 y final ☐ vista Cierre
**Producto:** ☐ RF-01…RF-06 ☐ BD-01 ☐ CAL-01 ☐ `unittest` 10/10 ☐ demo ensayada
**Informe:** ☐ 15 secciones ☐ 12–18 páginas ☐ decisiones explicadas ☐ planificado vs. real ☐ matriz firmada ☐ anexos
**Paquete:** ☐ informe PDF/DOCX ☐ enlaces repo y tablero ☐ scripts BD ☐ pruebas ☐ presentación ☐ matriz de rotación
