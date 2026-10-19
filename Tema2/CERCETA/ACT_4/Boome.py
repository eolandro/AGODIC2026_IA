import json
import random

ARCHIVO_TABLERO = "tablero.json"
SENSIBILIDAD = 0.90
TASA_FALSOS_POSITIVOS = 0.10
SEMILLA = 42
MAX_EVALUACIONES = 3


class BoomBay:
    def __init__(self, archivo_tablero):
        self.rng = random.Random(SEMILLA)
        self.desactivadores_disponibles = 0
        self.desactivadores_activados = 0
        self.tablero = self.leer_tablero(archivo_tablero)
        self.filas = len(self.tablero)
        self.columnas = len(self.tablero[0])

    def leer_tablero(self, archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        filas = datos["filas"]
        columnas = datos["columnas"]
        tablero = []
        for f in range(filas):
            fila = []
            for c in range(columnas):
                fila.append({
                    "bomba": False,
                    "evaluada": False,
                    "resultados": [],
                    "probabilidad": 0.0
                })
            tablero.append(fila)

        for f, c in datos["posiciones_bombas"]:
            tablero[f][c]["bomba"] = True

        self.desactivadores_disponibles = datos["desactivadores_disponibles"]
        if self.desactivadores_disponibles != 6:
            raise ValueError("Deben existir 6 desactivadores disponibles al inicio.")

        bombas = sum(1 for fila in tablero for casilla in fila if casilla["bomba"])
        if filas * columnas != 50 or bombas != 2:
            raise ValueError("El tablero debe tener 50 casillas y 2 bombas.")
        return tablero

    def calcular_bayes(self, probabilidad_anterior, resultado_positivo):
        # Actualiza P(Bomba) según el resultado del detector.
        if resultado_positivo:
            p_resultado_bomba = SENSIBILIDAD
            p_resultado_segura = TASA_FALSOS_POSITIVOS
        else:
            p_resultado_bomba = 1 - SENSIBILIDAD
            p_resultado_segura = 1 - TASA_FALSOS_POSITIVOS

        numerador = p_resultado_bomba * probabilidad_anterior
        denominador = numerador + p_resultado_segura * (1 - probabilidad_anterior)
        if denominador == 0:
            return probabilidad_anterior
        return numerador / denominador

    def detectar(self, casilla):
        # Simula un detector imperfecto.
        if casilla["bomba"]:
            probabilidad_positivo = SENSIBILIDAD
        else:
            probabilidad_positivo = TASA_FALSOS_POSITIVOS
        return self.rng.random() < probabilidad_positivo

    def evaluar_casilla(self, f, c, prior):
        casilla = self.tablero[f][c]
        posterior = prior
        positivos = 0
        negativos = 0

        print("\nCasilla ({}, {}) - prior: {:.2%}".format(f, c, prior))
        for numero in range(1, MAX_EVALUACIONES + 1):
            positivo = self.detectar(casilla)
            casilla["resultados"].append(positivo)

            if positivo:
                positivos += 1
                resultado = "POSITIVO"
            else:
                negativos += 1
                resultado = "NEGATIVO"

            posterior = self.calcular_bayes(posterior, positivo)
            print("  Evaluación {}: {} -> P(Bomba | evidencia) = {:.2%}".format(
                numero, resultado, posterior
            ))

            if numero == 2 and negativos == 2 and positivos == 0:
                print("  Se omite la tercera evaluación por dos negativos.")
                break

        casilla["evaluada"] = True
        casilla["probabilidad"] = posterior

        if positivos == 3 and not casilla["bomba"]:
            if self.desactivadores_disponibles > 0:
                self.desactivadores_disponibles -= 1
                self.desactivadores_activados += 1
                print("  ¡Salvavidas activado! Se consumió un desactivador.")
                print("  Desactivadores restantes: {}".format(self.desactivadores_disponibles))
            else:
                print("  No quedan desactivadores disponibles.")

        print("  Estado real de prueba: {}".format(
            "BOMBA" if casilla["bomba"] else "SIN BOMBA"
        ))
        return positivos, negativos, posterior

    def ejecutar(self):
        total = self.filas * self.columnas
        bombas = sum(1 for fila in self.tablero for casilla in fila if casilla["bomba"])
        prior = bombas / total

        print("=" * 60)
        print("TOMA DE DECISIONES CON BAYES")
        print("=" * 60)
        print("Casillas: {} | Bombas: {} | Sin bomba: {}".format(total, bombas, total - bombas))
        print("Desactivadores disponibles al inicio: {}".format(self.desactivadores_disponibles))
        print("Sensibilidad: {:.0%} | Falsos positivos: {:.0%}".format(
            SENSIBILIDAD, TASA_FALSOS_POSITIVOS
        ))
        print("=" * 60)
        print("P(Bomba) inicial = {:.2%}".format(prior))
        print("P(Bomba | detector positivo) = {:.2%}".format(
            self.calcular_bayes(prior, True)
        ))
        print("=" * 60)

        resumen = []
        for f in range(self.filas):
            for c in range(self.columnas):
                positivos, negativos, posterior = self.evaluar_casilla(f, c, prior)
                resumen.append((f, c, positivos, negativos, posterior))

        print("\nRESUMEN FINAL")
        print("{:<10}{:>1}{:>10}{:>20}".format("Casilla", "Positivos", "Negativos", "P(Bomba|evidencia)"))
        for f, c, positivos, negativos, posterior in resumen:
            print("({},{}){:>10}{:>10}{:>19.2%}".format(
                f, c, positivos, negativos, posterior
            ))

        print("\nDesactivadores activados:", self.desactivadores_activados)
        print("\nTablero real (B=bomba, .=sin bomba):")
        for fila in self.tablero:
            simbolos = []
            for casilla in fila:
                if casilla["bomba"]:
                    simbolos.append("B")
                else:
                    simbolos.append(".")
            print(" ".join(simbolos))


def main():
    juego = BoomBay(ARCHIVO_TABLERO)
    juego.ejecutar()


if __name__ == "__main__":
    main()
