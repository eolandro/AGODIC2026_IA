import argparse
import json
import random


def leer_tablero(ruta):
    archivo = open(ruta, encoding="utf-8")
    datos = json.load(archivo)
    archivo.close()
    return datos


def crear_mapa(datos):
    mapa = [[0] * datos["columnas"] for _ in range(datos["filas"])]

    for fila, columna in datos["posiciones_bombas"]:
        mapa[fila][columna] = 1

    return mapa


def leer_sensor(es_bomba, datos):
    probabilidad = datos["sensibilidad"] if es_bomba else datos["falso_positivo"]
    return 1 if random.random() < probabilidad else 0


def revisar(es_bomba, datos):
    lecturas = [leer_sensor(es_bomba, datos), leer_sensor(es_bomba, datos)]

    if lecturas == [0, 0]:
        return lecturas

    lecturas.append(leer_sensor(es_bomba, datos))
    return lecturas


def actualizar(creencia, datos):
    numerador = datos["sensibilidad"] * creencia
    return numerador / (numerador + datos["falso_positivo"] * (1 - creencia))


def calculo_bayes(prior, lecturas, datos):
    creencia = prior

    for _ in range(lecturas.count(1)):
        creencia = actualizar(creencia, datos)

    return creencia


def imprimir_tablero(mapa):
    print("\n================ TABLERO REVELADO ================")

    for fila in mapa:
        print(*fila)

    print("==================================================\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("Tablero", nargs="?", default="tablero.json")
    args = parser.parse_args()

    datos = leer_tablero(args.Tablero)
    random.seed(datos["semilla"])
    mapa = crear_mapa(datos)
    casillas = [casilla for fila in mapa for casilla in fila]
    bombas_total = len(datos["posiciones_bombas"])
    bombas_restantes = bombas_total
    desactivadores = datos["desactivadores"]
    umbral = datos["umbral"]

    print("*************** INICIANDO SIMULACION BOOM_BAY ***************")

    for i, es_bomba in enumerate(casillas):
        lecturas = revisar(es_bomba, datos)

        if 1 not in lecturas:
            print(f"Casilla {i}: Segura {lecturas}")
            continue

        prior = min(1.0, bombas_restantes / (len(casillas) - i))
        bayes = calculo_bayes(prior, lecturas, datos)
        print(f"Casilla {i}: ALERTA {lecturas} | P(Boom) previa: {prior:.4f} -> P(Boom|D+): {bayes:.4f}")

        if desactivadores == 0:
            print("   -> No se desactiva (sin desactivadores)")
            continue

        if bayes < umbral:
            print(f"   -> No se desactiva (probabilidad menor a {umbral})")
            continue

        desactivadores -= 1

        if es_bomba:
            bombas_restantes -= 1
            print(f"   -> Bomba desactivada | Desactivadores restantes: {desactivadores}")
        else:
            print(f"   -> Falso positivo | Desactivadores restantes: {desactivadores}")

        if bombas_restantes == 0:
            print("\nYa no quedan bombas, se termina el recorrido.")
            break

    print("\n=== FIN DE LA SIMULACION ===")
    print(f"Bombas desactivadas: {bombas_total - bombas_restantes}/{bombas_total}")
    print(f"Desactivadores sobrantes: {desactivadores}")
    imprimir_tablero(mapa)


if __name__ == "__main__":
    main()
