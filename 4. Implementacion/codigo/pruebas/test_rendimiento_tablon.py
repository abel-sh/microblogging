"""Prueba del rnf 9.3: el tablón se muestra en menos de 3 segundos.

El rnf dice "con el juego de datos de prueba" y no fija cuántos datos son. Acá se
eligió un volumen bastante mayor al de una demostración (5.000 mensajes y 500
republicaciones). Se mide el tiempo del servidor, de punta a punta (consultas,
armado del tablón y dibujo de la plantilla), sin red ni navegador.
"""

from __future__ import annotations

import random
import time
import unittest

from werkzeug.security import generate_password_hash

from miblog.acceso_datos.conexion import obtener_conexion, transaccion

from pruebas.ayudas import PruebaConApp, crear_mensaje, crear_usuario, en, republicar, seguir

TIEMPO_MAXIMO_SEGUNDOS = 3  # rnf 9.3
CANTIDAD_DE_USUARIOS = 100
CANTIDAD_DE_MENSAJES = 5000
CANTIDAD_DE_REPUBLICACIONES = 500
CANTIDAD_DE_SEGUIDOS = 20


class PruebaRendimientoTablon(PruebaConApp):
    def test_rnf_9_3_el_tablon_tarda_menos_de_tres_segundos(self):
        azar = random.Random(7)  # semilla fija: siempre los mismos datos
        mensajes_de_cada_usuario = {}
        republicaciones_por_usuario = {}

        with self.app.app_context(), transaccion():
            con = obtener_conexion()
            clave_hash = generate_password_hash("clave1234")
            ids = [
                crear_usuario(con, f"u{n}", clave_hash=clave_hash if n == 1 else "x")
                for n in range(1, CANTIDAD_DE_USUARIOS + 1)
            ]
            ana = ids[0]
            seguidos = set(ids[1 : 1 + CANTIDAD_DE_SEGUIDOS])
            for seguido in seguidos:
                seguir(con, ana, seguido)

            autores = {}
            for n in range(CANTIDAD_DE_MENSAJES):
                autor = azar.choice(ids)
                id_mensaje = crear_mensaje(con, autor, f"Mensaje {n} con #tema{n % 50}",
                                           en(-azar.randint(0, 60 * 24 * 30)))
                autores[id_mensaje] = autor
                mensajes_de_cada_usuario.setdefault(autor, []).append(id_mensaje)

            pares = set()
            while len(pares) < CANTIDAD_DE_REPUBLICACIONES:
                pares.add((azar.choice(ids), azar.choice(list(autores))))
            for republicador, id_mensaje in pares:
                republicar(con, republicador, id_mensaje, en(-azar.randint(0, 60 * 24 * 30)))
                republicaciones_por_usuario.setdefault(republicador, []).append(id_mensaje)

        # Lo que el tablón de ana tiene que mostrar: sus mensajes y los de sus seguidos,
        # más las republicaciones hechas por ella o por sus seguidos.
        visibles = {ana} | seguidos
        esperadas = sum(len(mensajes_de_cada_usuario.get(u, [])) for u in visibles) + sum(
            len(republicaciones_por_usuario.get(u, [])) for u in visibles
        )

        cliente = self.app.test_client()
        cliente.post("/sesion/iniciar", data={"nombre_usuario": "u1", "clave": "clave1234"})
        inicio = time.perf_counter()
        respuesta = cliente.get("/tablon")
        segundos = time.perf_counter() - inicio

        html = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        # Se comprueba que la página tiene todo lo que tenía que tener: un tiempo bueno
        # con una página casi vacía no probaría nada.
        self.assertEqual(html.count('<li class="tarjeta'), esperadas)
        self.assertLess(segundos, TIEMPO_MAXIMO_SEGUNDOS,
                        f"El tablón tardó {segundos:.2f} s (máximo: {TIEMPO_MAXIMO_SEGUNDOS} s).")


if __name__ == "__main__":
    unittest.main()