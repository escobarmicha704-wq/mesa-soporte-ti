# Plan de pruebas · Mesa de Soporte TI

## Objetivo y alcance
Verificar RF-01 a RF-06, BD-01 y CAL-01 del MVP.

## Tipos de prueba
- **Funcional:** cada requisito desde la interfaz o la ruta HTTP.
- **Integración:** flujo completo registrar → asignar → cambiar estado → filtrar → resumen, con persistencia en SQLite.

## Entorno
Python 3, Flask, SQLite; BD recreada con `python app.py --init`; pruebas automáticas con `python -m unittest -v test_app`.

## Criterios
- **Entrada:** BD creada con `schema.sql` y `seed.sql`.
- **Salida:** 100 % de casos críticos OK; defectos de severidad Alta cerrados con retest.

## Casos
| Caso | Requisito | Descripción | Resultado esperado | Resultado (fecha) | Evidencia |
|---|---|---|---|---|---|
| CP-01 | RF-01/02 | Registrar ticket válido | Se guarda con id TCK-0006, estado Nuevo y fecha | | |
| CP-02 | RF-01/CAL-01 | Datos inválidos (6 variantes) | Error visible; no se guarda | | |
| CP-03 | RF-03 | Abrir listado | Se ven estado, prioridad y responsable | | |
| CP-04 | RF-04 | Asignar responsable y estado | Persiste y deja 2 registros en historial | | |
| CP-05 | RF-04 | Avanzar sin responsable | Rechazado con mensaje | | |
| CP-06 | RF-04 | Estado inválido | Rechazado | | |
| CP-07 | RF-05 | Filtrar por estado/prioridad/categoría | Solo coincidencias | | |
| CP-08 | RF-06 | Resumen | Total y conteo por estado correctos | | |
| CP-09 | CAL-01 | Ruta o ticket inexistente | Página 404 | | |
| CP-10 | BD-01 | Persistencia | Registro presente en la BD | | |

## Pruebas manuales adicionales (completar al ejecutarlas)
| ID | Descripción | Resultado | Captura |
|---|---|---|---|
| PM-01 | Reiniciar la app y verificar que los tickets siguen | | |
