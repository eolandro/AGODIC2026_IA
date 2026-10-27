
from pathlib import Path
import random


def leer_tablero(nombre_archivo):
    ruta = Path(__file__).resolve().parent / nombre_archivo
    tablero = {}

    with open(ruta, "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            linea = linea.strip()

            if not linea or linea.startswith("#"):
                continue

            if "=" not in linea:
                raise ValueError(
                    f"Formato incorrecto en la linea {numero_linea}."
                )

            clave, valor = linea.split("=", 1)
            tablero[clave.strip()] = valor.strip()

    return tablero


def validar_probabilidad(nombre, valor):
    if not 0 <= valor <= 1:
        raise ValueError(f"{nombre} debe estar entre 0 y 1.")


def calcular_bayes(prob_bomba, prob_positivo_bomba,
                   prob_positivo_sin_bomba):
    numerador = prob_positivo_bomba * prob_bomba
    denominador = (
        numerador
        + prob_positivo_sin_bomba * (1 - prob_bomba)
    )

    if denominador <= 0:
        raise ValueError("No se puede calcular Bayes con estos datos.")

    return numerador / denominador


def actualizar_probabilidad(prob_anterior, resultado,
                            sensibilidad, falso_positivo):
    if resultado == "positivo":
        prob_bomba = sensibilidad
        prob_no_bomba = falso_positivo
    else:
        prob_bomba = 1 - sensibilidad
        prob_no_bomba = 1 - falso_positivo

    numerador = prob_bomba * prob_anterior
    denominador = (
        numerador + prob_no_bomba * (1 - prob_anterior)
    )

    if denominador <= 0:
        raise ValueError("No se puede actualizar la probabilidad.")

    return numerador / denominador


def main():
    print("=" * 48)
    print("       TOMA DE DECISIONES CON BAYES")
    print("                 BOOM_BAY")
    print("=" * 48)

    try:
        datos = leer_tablero("tablero.txt")

        campos = [
            "CASILLAS",
            "BOMBAS",
            "DETECTORES",
            "POSICIONES_BOMBAS",
            "PROB_DETECTOR_POSITIVO_CON_BOMBA",
            "PROB_DETECTOR_POSITIVO_SIN_BOMBA",
            "UMBRAL_REVISION"
        ]

        for campo in campos:
            if campo not in datos:
                raise ValueError(f"Falta el dato: {campo}")

        casillas = int(datos["CASILLAS"])
        bombas = int(datos["BOMBAS"])
        detectores = int(datos["DETECTORES"])

        posiciones_bombas = [
            int(p.strip())
            for p in datos["POSICIONES_BOMBAS"].split(",")
        ]

        sensibilidad = float(
            datos["PROB_DETECTOR_POSITIVO_CON_BOMBA"]
        )
        falso_positivo = float(
            datos["PROB_DETECTOR_POSITIVO_SIN_BOMBA"]
        )
        umbral = float(datos["UMBRAL_REVISION"])

        if casillas <= 0:
            raise ValueError("CASILLAS debe ser mayor que cero.")

        if not 0 <= bombas <= casillas:
            raise ValueError("La cantidad de bombas no es valida.")

        if detectores < 0:
            raise ValueError("DETECTORES no puede ser negativo.")

        if len(posiciones_bombas) != bombas:
            raise ValueError(
                "La cantidad de posiciones debe coincidir con BOMBAS."
            )

        if len(set(posiciones_bombas)) != bombas:
            raise ValueError("Hay posiciones de bombas repetidas.")

        if any(p < 1 or p > casillas for p in posiciones_bombas):
            raise ValueError("Hay una bomba fuera del tablero.")

        validar_probabilidad("Sensibilidad", sensibilidad)
        validar_probabilidad("Falso positivo", falso_positivo)
        validar_probabilidad("Umbral", umbral)

        prob_inicial = bombas / casillas
        bombas_reales = set(posiciones_bombas)

        probabilidades = {
            p: prob_inicial for p in range(1, casillas + 1)
        }

        print("\n1. TABLERO LEIDO DESDE ARCHIVO")
        print("-" * 38)
        print(f"Casillas: {casillas}")
        print(f"Bombas: {bombas}")
        print(f"Detectores: {detectores}")
        print(f"Probabilidad inicial: {prob_inicial:.2%}")

        print("\nMapa predefinido:")
        print(" ".join(f"[{p:02d}]" for p in range(1, casillas + 1)))

        prob_positivo = calcular_bayes(
            prob_inicial, sensibilidad, falso_positivo
        )

        print("\n2. PROBABILIDAD DE BAYES POR DETECTOR POSITIVO")
        print("-" * 38)
        print(f"P(Bomba | D+) = {prob_positivo:.6f}")
        print(f"Porcentaje: {prob_positivo:.2%}")

        print("\n3. SIMULACION DE DETECTORES")
        print("-" * 38)
        print(f"Ingresa una casilla del 1 al {casillas}.")
        print("Escribe 0 para terminar.")

        usados = 0

        while usados < detectores:
            entrada = input(
                f"\nDetector {usados + 1}/{detectores}. Casilla: "
            ).strip()

            try:
                posicion = int(entrada)
            except ValueError:
                print("Escribe un numero entero.")
                continue

            if posicion == 0:
                break

            if not 1 <= posicion <= casillas:
                print(
                    f"Selecciona una casilla entre 1 y {casillas}."
                )
                continue

            if posicion in bombas_reales:
                positivo = random.random() < sensibilidad
            else:
                positivo = random.random() < falso_positivo

            resultado = "positivo" if positivo else "negativo"

            anterior = probabilidades[posicion]
            actualizada = actualizar_probabilidad(
                anterior, resultado, sensibilidad, falso_positivo
            )

            probabilidades[posicion] = actualizada
            usados += 1

            print(f"Resultado del detector: {resultado.upper()}")
            print(f"Probabilidad anterior: {anterior:.2%}")
            print(f"Probabilidad actualizada: {actualizada:.2%}")

            print("\n4. DECISION")

            if actualizada >= umbral:
                print("Revisar prioritariamente esta casilla.")
            else:
                print("Mantener esta casilla en observacion.")

        print("\n5. RESUMEN DE PROBABILIDADES")
        print("-" * 38)

        for posicion, probabilidad in probabilidades.items():
            print(f"Casilla {posicion:02d}: {probabilidad:.2%}")

        print("\nSimulacion finalizada correctamente.")

    except FileNotFoundError:
        print("\nERROR: No se encontro tablero.txt.")
        print("Coloca ambos archivos en la misma carpeta.")

    except (ValueError, KeyError) as error:
        print(f"\nERROR: {error}")

    except OSError as error:
        print(f"\nERROR al leer el archivo: {error}")


if __name__ == "__main__":
    main()
