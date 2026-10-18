
import json
from pathlib import Path


# R010: Leer tablero desde archivo
def leer_tablero(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


# R011: Calcular probabilidad de Bayes
def bayes(prior, sensibilidad, falso_positivo, positivo=True):
    if positivo:
        p_evidencia_bomba = sensibilidad
        p_evidencia_sin_bomba = falso_positivo
    else:
        p_evidencia_bomba = 1 - sensibilidad
        p_evidencia_sin_bomba = 1 - falso_positivo

    numerador = p_evidencia_bomba * prior

    denominador = (
        numerador
        + p_evidencia_sin_bomba * (1 - prior)
    )

    if denominador == 0:
        return 0

    return numerador / denominador


def analizar_lecturas(tablero):
    total = tablero["casillas"]
    bombas = len(tablero["bombas"])

    sensibilidad = tablero["sensibilidad"]
    falso_positivo = tablero["falso_positivo"]
    lecturas = tablero["lecturas"]

    prior_inicial = bombas / total

    print("=== BOOM_BAY ===")
    print("Casillas:", total)
    print("Bombas:", bombas)
    print("Desactivadores:", len(tablero["desactivadores"]))
    print("Probabilidad inicial:", round(prior_inicial * 100, 2), "%")

    print("\n=== Recorrido del tablero ===")

    for casilla in range(1, total + 1):
        print("\nBoom esta revisando la casilla:", casilla)

        if str(casilla) not in lecturas:
            print("No hay lectura registrada.")
            continue

        lectura = lecturas[str(casilla)]
        print("Lectura inicial:", lectura)

        # La probabilidad inicial de esta casilla
        prior = prior_inicial

        posterior = bayes(
            prior,
            sensibilidad,
            falso_positivo,
            lectura == "positivo"
        )

        print("Intento 1:", f"{posterior * 100:.2f}%")

        # Si el detector da positivo, hacer dos intentos adicionales
        if lectura == "positivo":
            for intento in range(2, 4):
                print("Realizando intento", intento, "...")

                # Para este ejemplo, se considera que el detector
                # vuelve a dar positivo en los dos intentos.
                posterior = bayes(
                    posterior,
                    sensibilidad,
                    falso_positivo,
                    True
                )

                print(
                    f"Intento {intento}: "
                    f"probabilidad de bomba = {posterior * 100:.2f}%"
                )

            print("Boom terminó los tres intentos.")


def main():
    ruta = Path(__file__).resolve().parent / "tablero.json"
    tablero = leer_tablero(ruta)
    analizar_lecturas(tablero)


if __name__ == "__main__":
    main()
