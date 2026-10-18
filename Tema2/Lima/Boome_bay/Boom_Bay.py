
import argparse
import json
import random
from pathlib import Path


def leer_tablero(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        tablero = json.load(archivo)

    requeridos = ["filas", "columnas", "bomba", "sensibilidad",
                  "falso_positivo", "umbral", "desactivadores"]
    faltan = [k for k in requeridos if k not in tablero]
    if faltan:
        raise ValueError(f"Faltan claves en el tablero: {faltan}")

    f, c = tablero["bomba"]
    if not (0 <= f < tablero["filas"] and 0 <= c < tablero["columnas"]):
        raise ValueError("La bomba está fuera del tablero")
    return tablero

def bayes(prior, sensibilidad, falso_positivo):
    p_bomba = sensibilidad * prior
    p_vacia = falso_positivo * (1 - prior)
    total = p_bomba + p_vacia
    return p_bomba / total if total > 0 else 0.0


class BoomBay:
    SIM_SIN_REVISAR = "?"
    SIM_REVISADA    = "."
    SIM_BOOME       = "R"
    SIM_DESARMADA   = "B"
    SIM_EXPLOTO     = "X"
    SIM_FALSA       = "D"

    def __init__(self, tablero, rng):
        self.filas          = tablero["filas"]
        self.columnas       = tablero["columnas"]
        self.total          = self.filas * self.columnas
        self.bomba          = tuple(tablero["bomba"])
        self.sensibilidad   = tablero["sensibilidad"]
        self.falso_positivo = tablero["falso_positivo"]
        self.umbral         = tablero["umbral"]
        self.desactivadores = tablero["desactivadores"]
        self.rng            = rng

        self.ruta = []
        for f in range(self.filas):
            cols = range(self.columnas)
            if f % 2 == 1:
                cols = reversed(cols)
            self.ruta += [(f, c) for c in cols]

        self.revisadas = 0
        self.pos       = None
        self.marcas    = {}
        self.Estado    = "ready"
        self.Resultado = ""

    def detector(self, casilla):
        p_positivo = self.sensibilidad if casilla == self.bomba else self.falso_positivo
        return 1 if self.rng.random() < p_positivo else 0

    def evaluar(self, casilla):
        lectura = self.detector(casilla)
        print(f"Casilla {casilla}: detector = {lectura}")
        if lectura == 0:
            return None

        prior = 1 / (self.total - self.revisadas)
        posterior = bayes(prior, self.sensibilidad, self.falso_positivo)
        print(f"  Intento 1 (prior {prior * 100:.2f}%): "
              f"P(bomba|+) = {posterior * 100:.2f}%")

        for intento in (2, 3):
            lectura = self.detector(casilla)
            if lectura == 1:
                posterior = bayes(posterior, self.sensibilidad, self.falso_positivo)
                print(f"  Intento {intento}: detector = 1 -> "
                      f"P(bomba|+) = {posterior * 100:.2f}%")
            else:
                print(f"  Intento {intento}: detector = 0 -> "
                      f"sin cambio ({posterior * 100:.2f}%)")
        return posterior

    def step(self):
        if self.Estado != "ready":
            return

        casilla   = self.ruta[self.revisadas]
        posterior = self.evaluar(casilla)

        if posterior is not None and posterior >= self.umbral and self.desactivadores > 0:
            self.desactivadores -= 1
            if casilla == self.bomba:
                self.marcas[casilla] = self.SIM_DESARMADA
                self.Estado    = "done"
                self.Resultado = "Bomba desactivada"
                print("  >> Desactivador usado: ¡había una bomba!")
            else:
                self.marcas[casilla] = self.SIM_FALSA
                print("  >> Desactivador usado: falsa alarma, no había bomba")
        elif casilla == self.bomba:
            self.marcas[casilla] = self.SIM_EXPLOTO
            self.Estado    = "dead"
            self.Resultado = "Boome pisó la bomba"
            if posterior is not None and posterior >= self.umbral:
                print("  >> Sin desactivadores disponibles")
        else:
            self.marcas[casilla] = self.SIM_REVISADA

        self.pos = casilla
        self.revisadas += 1

    def __str__(self):
        lineas = []
        for f in range(self.filas):
            fila = ""
            for c in range(self.columnas):
                casilla = (f, c)
                if casilla in self.marcas and self.marcas[casilla] in (
                        self.SIM_DESARMADA, self.SIM_EXPLOTO):
                    fila += self.marcas[casilla]
                elif casilla == self.pos:
                    fila += self.SIM_BOOME
                else:
                    fila += self.marcas.get(casilla, self.SIM_SIN_REVISAR)
            lineas.append("│ " + fila + " │")
        borde = "─" * (self.columnas + 2)
        return "\n".join(["┌" + borde + "┐", *lineas, "└" + borde + "┘",
                          f"Desactivadores restantes: {self.desactivadores}"])


def main():
    parser = argparse.ArgumentParser(description="Boom_Bay: decisiones con Bayes")
    parser.add_argument("tablero", nargs="?",
                        default=Path(__file__).resolve().parent / "tablero.json",
                        help="Archivo JSON con el tablero")
    args = parser.parse_args()

    tablero = leer_tablero(args.tablero)
    rng = random.Random(tablero.get("semilla"))
    boom = BoomBay(tablero, rng)

    print("=== BOOM_BAY ===")
    print(f"Casillas: {boom.total}  |  Umbral: {boom.umbral * 100:.0f}%  |  "
          f"Desactivadores: {boom.desactivadores}")
    print(boom)
    print("─" * 50)

    while boom.Estado == "ready" and boom.revisadas < boom.total:
        boom.step()

    print("─" * 50)
    print(boom)
    print(f"Resultado: {boom.Resultado or 'Terminó el recorrido'}")


if __name__ == "__main__":
    main()
