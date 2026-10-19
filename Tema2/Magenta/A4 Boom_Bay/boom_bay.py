import json
import random

ARCHIVO_TABLERO = "tablero.json"
SENSIBILIDAD = 0.90
TASA_FALSOS_POSITIVOS = 0.20
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

        self.desactivadores_disponibles = datos.get("desactivadores_disponibles", 6)
        
        bombas = sum(1 for fila in tablero for casilla in fila if casilla["bomba"])
        if filas * columnas != 50 or bombas != 2:
            raise ValueError("El tablero debe tener 50 casillas y 2 bombas.")
        return tablero

    def calcular_bayes(self, probabilidad_anterior, resultado_positivo):
        """ Actualización Bayesiana Iterativa """
        if resultado_positivo:
            p_resultado_bomba = SENSIBILIDAD
            p_resultado_segura = TASA_FALSOS_POSITIVOS
        else:
            p_resultado_bomba = 1.0 - SENSIBILIDAD
            p_resultado_segura = 1.0 - TASA_FALSOS_POSITIVOS

        numerador = p_resultado_bomba * probabilidad_anterior
        denominador = numerador + p_resultado_segura * (1.0 - probabilidad_anterior)
        
        if denominador == 0:
            return probabilidad_anterior
        return numerador / denominador

    def detectar(self, casilla):
        """ Simulación del sensor imperfecto """
        probabilidad_positivo = SENSIBILIDAD if casilla["bomba"] else TASA_FALSOS_POSITIVOS
        return self.rng.random() < probabilidad_positivo

    def evaluar_casilla(self, f, c, prior):
        casilla = self.tablero[f][c]
        posterior = prior
        positivos = 0
        negativos = 0

        print(f"\nCasilla ({f}, {c}) - prior: {prior:.2%}")
        for numero in range(1, MAX_EVALUACIONES + 1):
            positivo = self.detectar(casilla)
            casilla["resultados"].append(positivo)

            if positivo:
                positivos += 1
                resultado = "POSITIVO (D+)"
            else:
                negativos += 1
                resultado = "NEGATIVO (D-)"

            posterior = self.calcular_bayes(posterior, positivo)
            print(f"  Evaluación {numero}: {resultado} -> P(Bomba | evidencia) = {posterior:.2%}")

            if numero == 2 and negativos == 2 and positivos == 0:
                print("  Se omite la tercera evaluación por acumulación de negativos.")
                break

        casilla["evaluada"] = True
        casilla["probabilidad"] = posterior
        if positivos >= 2:
            if self.desactivadores_disponibles > 0:
                self.desactivadores_disponibles -= 1
                self.desactivadores_activados += 1
                print("  ¡Alerta! Se aplicó un desactivador de bomba.")
                print(f"  Desactivadores restantes: {self.desactivadores_disponibles}")
            else:
                print("  ¡Sin desactivadores disponibles!")

        print("  Estado real: {}".format("BOMBA" if casilla["bomba"] else "SIN BOMBA"))
        return positivos, negativos, posterior

    def ejecutar(self):
        total = self.filas * self.columnas
        bombas = sum(1 for fila in self.tablero for casilla in fila if casilla["bomba"])
        prior = bombas / total

        print("=" * 60)
        print(" TOMA DE DECISIONES CON BAYES (BOOM_BAY)")
        print("=" * 60)
        print(f"Casillas: {total} | Bombas: {bombas} | Vacías: {total - bombas}")
        print(f"Desactivadores disponibles: {self.desactivadores_disponibles}")
        print(f"Sensibilidad P(D+|Bomba): {SENSIBILIDAD:.0%} | Falsos Positivos P(D+|No Bomba): {TASA_FALSOS_POSITIVOS:.0%}")
        print("=" * 60)
        print(f"P(Bomba) Prior Inicial = {prior:.2%}")
        print(f"P(Bomba | 1er D+) Teórico = {self.calcular_bayes(prior, True):.2%}")
        print("=" * 60)

        resumen = []
        for f in range(self.filas):
            for c in range(self.columnas):
                positivos, negativos, posterior = self.evaluar_casilla(f, c, prior)
                resumen.append((f, c, positivos, negativos, posterior))

        print("\n" + "="*60)
        print("RESUMEN DE RESULTADOS")
        print("="*60)
        print(f"{'Casilla':<10}{'Positivos':<12}{'Negativos':<12}{'P(Bomba|evidencia)'}")
        for f, c, pos, neg, post in resumen[:10]: # Muestra las primeras 10 como vista previa
            print(f"({f},{c}){'':<5}{pos:<12}{neg:<12}{post:.2%}")
        print("... (resto de casillas evaluadas)")

        print(f"\nDesactivadores utilizados: {self.desactivadores_activados}")


def main():
    juego = BoomBay(ARCHIVO_TABLERO)
    juego.ejecutar()


if __name__ == "__main__":
    main()