"""Pruebas funcionales de la Mesa de Soporte TI.

Ejecutar:  python -m unittest -v test_app
(usa solo la librería estándar; cada prueba trabaja con una BD temporal limpia)
"""
import os
import sqlite3
import tempfile
import unittest

import app as mesa


def ticket_valido(**extra):
    d = {"solicitante": "Juan Pérez", "titulo": "Pantalla parpadea",
         "descripcion": "El monitor parpadea cada pocos minutos.",
         "categoria_id": "1", "prioridad": "Alta"}
    d.update(extra)
    return d


class MesaTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        mesa.app.config["DATABASE"] = os.path.join(self.tmp.name, "test.db")
        mesa.app.config["TESTING"] = True
        mesa.init_db(con_datos=True)
        self.client = mesa.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def q(self, sql, params=()):
        con = sqlite3.connect(mesa.app.config["DATABASE"])
        con.row_factory = sqlite3.Row
        filas = con.execute(sql, params).fetchall()
        con.close()
        return filas

    # CP-01 · RF-01 / RF-02
    def test_cp01_registrar_ticket_valido(self):
        r = self.client.post("/tickets/nuevo", data=ticket_valido(), follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"TCK-0006", r.data)                       # id único
        fila = self.q("SELECT * FROM tickets WHERE codigo='TCK-0006'")[0]
        self.assertEqual(fila["estado"], "Nuevo")                # estado inicial
        self.assertTrue(fila["fecha_creacion"])                  # fecha de creación

    # CP-02 · CAL-01 validaciones
    def test_cp02_validaciones_rechazan_datos_invalidos(self):
        casos = [("solicitante", ""), ("titulo", "abc"), ("descripcion", "corta"),
                 ("categoria_id", ""), ("categoria_id", "999"), ("prioridad", "Urgentísima")]
        antes = len(self.q("SELECT id FROM tickets"))
        for campo, valor in casos:
            with self.subTest(campo=campo, valor=valor):
                r = self.client.post("/tickets/nuevo", data=ticket_valido(**{campo: valor}))
                self.assertEqual(r.status_code, 200)
                self.assertIn(b"flash error", r.data)
                self.assertEqual(len(self.q("SELECT id FROM tickets")), antes)

    # CP-03 · RF-03
    def test_cp03_listado_muestra_estado_prioridad_responsable(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        for texto in (b"TCK-0001", b"Soporte Nivel 1", "Crítica".encode(), b"En proceso"):
            self.assertIn(texto, r.data)

    # CP-04 · RF-04
    def test_cp04_asignar_responsable_y_cambiar_estado(self):
        r = self.client.post("/tickets/1", data={"responsable_id": "1", "estado": "En proceso"},
                             follow_redirects=True)
        self.assertIn(b"Solicitud actualizada", r.data)
        fila = self.q("SELECT * FROM tickets WHERE id=1")[0]
        self.assertEqual((fila["estado"], fila["responsable_id"]), ("En proceso", 1))
        self.assertEqual(len(self.q("SELECT * FROM historial_cambios WHERE ticket_id=1")), 2)

    def test_cp05_no_avanzar_estado_sin_responsable(self):
        r = self.client.post("/tickets/1", data={"responsable_id": "", "estado": "Resuelto"})
        self.assertIn(b"Debe asignar un responsable", r.data)
        self.assertEqual(self.q("SELECT estado FROM tickets WHERE id=1")[0]["estado"], "Nuevo")

    def test_cp06_estado_invalido_rechazado(self):
        r = self.client.post("/tickets/2", data={"responsable_id": "1", "estado": "Inventado"})
        self.assertIn("Estado inválido".encode(), r.data)

    # CP-07 · RF-05
    def test_cp07_filtros(self):
        r = self.client.get("/?estado=Cerrado")
        self.assertIn(b"TCK-0005", r.data)
        self.assertNotIn(b"TCK-0001", r.data)
        r = self.client.get("/?prioridad=Cr%C3%ADtica")
        self.assertIn(b"TCK-0004", r.data)
        self.assertNotIn(b"TCK-0002", r.data)
        r = self.client.get("/?categoria=1")
        self.assertIn(b"TCK-0001", r.data)
        self.assertNotIn(b"TCK-0002", r.data)

    # CP-08 · RF-06
    def test_cp08_resumen_total_y_por_estado(self):
        html = self.client.get("/").data.decode()
        self.assertIn("<span>5</span>Total", html)
        self.assertIn("<span>1</span>Nuevo", html)
        self.assertIn("<span>2</span>En proceso", html)

    # CP-09 · CAL-01 manejo de errores
    def test_cp09_rutas_inexistentes_404(self):
        self.assertEqual(self.client.get("/tickets/9999").status_code, 404)
        self.assertEqual(self.client.get("/ruta-inexistente").status_code, 404)

    # CP-10 · BD-01 persistencia
    def test_cp10_persistencia_en_bd(self):
        self.client.post("/tickets/nuevo", data=ticket_valido(titulo="Teclado dañado"))
        self.assertTrue(self.q("SELECT * FROM tickets WHERE titulo='Teclado dañado'"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
