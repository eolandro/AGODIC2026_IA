import json
import random
import tempfile
import unittest
from collections import deque
from pathlib import Path
from main import a_estrella, cargar_tablero, MUROS

BASE = Path(__file__).parent


def distancia_bfs(tablero, inicio, fin):
    cola = deque([(inicio, 0)])
    vistos = {inicio}
    while cola:
        (f, c), distancia = cola.popleft()
        if (f, c) == fin:
            return distancia
        for df, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nf, nc = f + df, c + dc
            if 0 <= nf < 10 and 0 <= nc < 10 and (nf, nc) not in vistos and tablero[nf][nc] not in MUROS:
                vistos.add((nf, nc))
                cola.append(((nf, nc), distancia + 1))
    return None


class Pruebas(unittest.TestCase):
    def comprobar_ruta(self, tablero, inicio, fin):
        ruta = a_estrella(tablero, inicio, fin)
        minimo = distancia_bfs(tablero, inicio, fin)
        self.assertEqual(None if ruta is None else len(ruta) - 1, minimo)
        if ruta is not None:
            self.assertEqual((ruta[0], ruta[-1]), (inicio, fin))
            for a, b in zip(ruta, ruta[1:]):
                self.assertEqual(abs(a[0]-b[0])+abs(a[1]-b[1]), 1)
                self.assertNotIn(tablero[b[0]][b[1]], MUROS)

    def test_ambos_json(self):
        for nombre in ('tablero.json', 'tablero_alternativo.json'):
            with self.subTest(nombre=nombre):
                tablero, inicio, fin = cargar_tablero(BASE / nombre)
                self.comprobar_ruta(tablero, inicio, fin)

    def test_sin_camino(self):
        tablero = [['.'] * 10 for _ in range(10)]
        tablero[0][0] = 'R'
        tablero[9][9] = 'B'
        tablero[8][9] = tablero[9][8] = '#'
        self.comprobar_ruta(tablero, (0, 0), (9, 9))

    def test_aleatorios_vs_bfs(self):
        rng = random.Random(2026)
        for _ in range(200):
            tablero = [['#' if rng.random() < .3 else '.' for _ in range(10)] for _ in range(10)]
            tablero[0][0], tablero[9][9] = 'R', 'B'
            self.comprobar_ruta(tablero, (0, 0), (9, 9))

    def test_json_invalidos(self):
        casos = [[], {'tablero': [['.'] * 10] * 9}, {'tablero': [['.'] * 10 for _ in range(10)]}, {'tablero': [['?'] * 10 for _ in range(10)]}]
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / 'test.json'
            for caso in casos:
                archivo.write_text(json.dumps(caso), encoding='utf-8')
                with self.assertRaises(ValueError):
                    cargar_tablero(archivo)


if __name__ == '__main__':
    unittest.main()
