"""Mesa de Soporte TI - MVP (Flask + SQLite).

Ejecución:
    pip install -r requirements.txt
    python app.py --init      # crea la BD (schema.sql + seed.sql) y termina
    python app.py             # levanta el servidor en http://127.0.0.1:5000
"""
import os
import sqlite3
import sys

from flask import Flask, flash, g, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ESTADOS = ["Nuevo", "En proceso", "Resuelto", "Cerrado"]
PRIORIDADES = ["Baja", "Media", "Alta", "Crítica"]

app = Flask(__name__)
app.config["SECRET_KEY"] = "mesa-soporte-ti-dev"
app.config["DATABASE"] = os.path.join(BASE_DIR, "mesa.db")


# ----------------------------------------------------------------- base de datos
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(con_datos=True):
    db = sqlite3.connect(app.config["DATABASE"])
    with open(os.path.join(BASE_DIR, "schema.sql"), encoding="utf-8") as f:
        db.executescript(f.read())
    if con_datos:
        with open(os.path.join(BASE_DIR, "seed.sql"), encoding="utf-8") as f:
            db.executescript(f.read())
    db.commit()
    db.close()


# ------------------------------------------------------------------ validaciones
def validar_ticket(form, categorias_ids):
    """Devuelve (datos_limpios, lista_de_errores). CAL-01."""
    errores = []
    datos = {
        "solicitante": form.get("solicitante", "").strip(),
        "titulo": form.get("titulo", "").strip(),
        "descripcion": form.get("descripcion", "").strip(),
        "categoria_id": form.get("categoria_id", "").strip(),
        "prioridad": form.get("prioridad", "").strip(),
    }
    if len(datos["solicitante"]) < 3:
        errores.append("El solicitante es obligatorio (mínimo 3 caracteres).")
    if len(datos["titulo"]) < 5:
        errores.append("El título es obligatorio (mínimo 5 caracteres).")
    elif len(datos["titulo"]) > 100:
        errores.append("El título no puede superar los 100 caracteres.")
    if len(datos["descripcion"]) < 10:
        errores.append("La descripción es obligatoria (mínimo 10 caracteres).")
    if not datos["categoria_id"].isdigit() or int(datos["categoria_id"]) not in categorias_ids:
        errores.append("Debe seleccionar una categoría válida.")
    if datos["prioridad"] not in PRIORIDADES:
        errores.append("Debe seleccionar una prioridad válida.")
    return datos, errores


# ------------------------------------------------------------------------ rutas
@app.route("/")
def index():
    db = get_db()
    f_estado = request.args.get("estado", "")
    f_prioridad = request.args.get("prioridad", "")
    f_categoria = request.args.get("categoria", "")

    sql = """SELECT t.*, c.nombre AS categoria, u.nombre AS responsable
             FROM tickets t
             JOIN categorias c ON c.id = t.categoria_id
             LEFT JOIN usuarios u ON u.id = t.responsable_id
             WHERE 1=1"""
    params = []
    if f_estado in ESTADOS:                      # RF-05
        sql += " AND t.estado = ?"
        params.append(f_estado)
    if f_prioridad in PRIORIDADES:
        sql += " AND t.prioridad = ?"
        params.append(f_prioridad)
    if f_categoria.isdigit():
        sql += " AND t.categoria_id = ?"
        params.append(int(f_categoria))
    sql += " ORDER BY t.id DESC"
    tickets = db.execute(sql, params).fetchall()          # RF-03

    # RF-06: resumen total y por estado (sobre todos los tickets)
    total = db.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    por_estado = {e: 0 for e in ESTADOS}
    for fila in db.execute("SELECT estado, COUNT(*) AS n FROM tickets GROUP BY estado"):
        por_estado[fila["estado"]] = fila["n"]

    categorias = db.execute("SELECT * FROM categorias ORDER BY nombre").fetchall()
    return render_template(
        "index.html", tickets=tickets, total=total, por_estado=por_estado,
        categorias=categorias, estados=ESTADOS, prioridades=PRIORIDADES,
        f_estado=f_estado, f_prioridad=f_prioridad, f_categoria=f_categoria,
    )


@app.route("/tickets/nuevo", methods=["GET", "POST"])
def nuevo_ticket():
    db = get_db()
    categorias = db.execute("SELECT * FROM categorias ORDER BY nombre").fetchall()
    ids = {c["id"] for c in categorias}
    datos = {}
    if request.method == "POST":
        datos, errores = validar_ticket(request.form, ids)
        if errores:
            for e in errores:
                flash(e, "error")
        else:
            try:
                cur = db.execute(
                    """INSERT INTO tickets
                       (codigo, solicitante, titulo, descripcion, categoria_id, prioridad)
                       VALUES ('PENDIENTE', ?, ?, ?, ?, ?)""",
                    (datos["solicitante"], datos["titulo"], datos["descripcion"],
                     int(datos["categoria_id"]), datos["prioridad"]),
                )
                nuevo_id = cur.lastrowid                  # RF-02
                db.execute("UPDATE tickets SET codigo = ? WHERE id = ?",
                           (f"TCK-{nuevo_id:04d}", nuevo_id))
                db.execute(
                    "INSERT INTO historial_cambios (ticket_id, campo, valor_antes, valor_nuevo) "
                    "VALUES (?, 'creación', NULL, 'Nuevo')", (nuevo_id,))
                db.commit()
                flash(f"Solicitud TCK-{nuevo_id:04d} registrada correctamente.", "ok")
                return redirect(url_for("detalle_ticket", ticket_id=nuevo_id))
            except sqlite3.Error:
                db.rollback()
                flash("Error al guardar la solicitud. Intente nuevamente.", "error")
    return render_template("nuevo.html", categorias=categorias,
                           prioridades=PRIORIDADES, datos=datos)


@app.route("/tickets/<int:ticket_id>", methods=["GET", "POST"])
def detalle_ticket(ticket_id):
    db = get_db()
    ticket = db.execute(
        """SELECT t.*, c.nombre AS categoria, u.nombre AS responsable
           FROM tickets t JOIN categorias c ON c.id = t.categoria_id
           LEFT JOIN usuarios u ON u.id = t.responsable_id WHERE t.id = ?""",
        (ticket_id,)).fetchone()
    if ticket is None:
        return render_template("error.html", mensaje="La solicitud no existe."), 404

    usuarios = db.execute("SELECT * FROM usuarios ORDER BY nombre").fetchall()

    if request.method == "POST":                          # RF-04
        nuevo_estado = request.form.get("estado", "")
        resp_raw = request.form.get("responsable_id", "")
        ids_usuarios = {u["id"] for u in usuarios}
        errores = []
        if nuevo_estado not in ESTADOS:
            errores.append("Estado inválido.")
        if resp_raw == "":
            nuevo_resp = None
        elif resp_raw.isdigit() and int(resp_raw) in ids_usuarios:
            nuevo_resp = int(resp_raw)
        else:
            nuevo_resp = None
            errores.append("Responsable inválido.")
        if not errores and nuevo_estado in ("En proceso", "Resuelto", "Cerrado") and nuevo_resp is None:
            errores.append("Debe asignar un responsable antes de pasar a "
                           f"'{nuevo_estado}'.")
        if errores:
            for e in errores:
                flash(e, "error")
        else:
            try:
                if nuevo_estado != ticket["estado"]:
                    db.execute("INSERT INTO historial_cambios (ticket_id, campo, valor_antes, valor_nuevo) "
                               "VALUES (?, 'estado', ?, ?)",
                               (ticket_id, ticket["estado"], nuevo_estado))
                if nuevo_resp != ticket["responsable_id"]:
                    nombres = {u["id"]: u["nombre"] for u in usuarios}
                    db.execute("INSERT INTO historial_cambios (ticket_id, campo, valor_antes, valor_nuevo) "
                               "VALUES (?, 'responsable', ?, ?)",
                               (ticket_id, ticket["responsable"], nombres.get(nuevo_resp)))
                db.execute("UPDATE tickets SET estado = ?, responsable_id = ? WHERE id = ?",
                           (nuevo_estado, nuevo_resp, ticket_id))
                db.commit()
                flash("Solicitud actualizada.", "ok")
                return redirect(url_for("detalle_ticket", ticket_id=ticket_id))
            except sqlite3.Error:
                db.rollback()
                flash("Error al actualizar la solicitud.", "error")

    historial = db.execute(
        "SELECT * FROM historial_cambios WHERE ticket_id = ? ORDER BY id DESC",
        (ticket_id,)).fetchall()
    return render_template("detalle.html", t=ticket, usuarios=usuarios,
                           estados=ESTADOS, historial=historial)


@app.errorhandler(404)
def no_encontrado(_e):
    return render_template("error.html", mensaje="Página no encontrada."), 404


@app.errorhandler(500)
def error_interno(_e):
    return render_template("error.html", mensaje="Ocurrió un error interno."), 500


if __name__ == "__main__":
    if "--init" in sys.argv:
        init_db()
        print("Base de datos creada con datos de prueba en", app.config["DATABASE"])
        sys.exit(0)
    if not os.path.exists(app.config["DATABASE"]):
        init_db()
        print("Base de datos creada con datos de prueba.")
    app.run(debug=True)
