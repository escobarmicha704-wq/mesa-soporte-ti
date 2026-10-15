# Mesa de Soporte TI (MVP)

Sistema web liviano para registrar y controlar solicitudes de soporte TI: registro, listado, asignación de responsable, cambio de estado, filtros y resumen. Evaluación 3.

**Equipo:** Michael Mejia (roles rotativos: Líder y Control · Solución y Desarrollo · Datos, Calidad y Pruebas)
**Tablero:** _pegar aquí el enlace de GitHub Projects_

## Tecnología (y por qué)
| Capa | Elección | Justificación |
|---|---|---|
| Lenguaje / framework | Python 3 + Flask | Poco código, sin build, plantillas HTML incluidas |
| Base de datos | SQLite | Relacional, sin instalar servidor, un solo archivo |
| Frontend | HTML + CSS (plantillas Jinja2) | Sin dependencias; suficiente para el MVP |
| Pruebas | `unittest` (estándar) | No requiere instalar nada extra |

## Cómo ejecutar
```bash
git clone <URL_DEL_REPOSITORIO>
cd mesa-soporte-ti
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py --init               # crea mesa.db con schema.sql + seed.sql (datos de prueba)
python app.py                      # abrir http://127.0.0.1:5000
```
- Si `mesa.db` no existe, `python app.py` la crea automáticamente con datos de prueba.
- `python app.py --init` recrea la BD desde cero (borra los datos anteriores).

## Pruebas
```bash
python -m unittest -v test_app
```
10 casos (CP-01 a CP-10) que cubren RF-01…RF-06, BD-01 y CAL-01.

## Estructura
```
app.py            lógica de aplicación (rutas, validaciones, acceso a BD)
schema.sql        script de creación de la base de datos
seed.sql          datos de prueba
templates/        interfaces (listado, nueva solicitud, detalle)
static/style.css  estilos
test_app.py       pruebas funcionales automatizadas
docs/             evidencias del proyecto (informe, hitos, pruebas)
```

## Trazabilidad requisito → implementación
| ID | Implementación | Prueba |
|---|---|---|
| RF-01 | `/tickets/nuevo` (formulario) | CP-01 |
| RF-02 | `codigo` TCK-000N + `fecha_creacion` automática | CP-01 |
| RF-03 | `/` listado con estado, prioridad y responsable | CP-03 |
| RF-04 | `/tickets/<id>` asignar responsable y cambiar estado | CP-04, CP-05, CP-06 |
| RF-05 | filtros por estado, prioridad, categoría en `/` | CP-07 |
| RF-06 | tarjetas de resumen (total y por estado) | CP-08 |
| BD-01 | tablas `usuarios`, `categorias`, `tickets`, `historial_cambios` | CP-10 |
| CAL-01 | validaciones, mensajes de error, páginas 404/500, pruebas | CP-02, CP-09 |
