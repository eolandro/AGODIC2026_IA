# r008_clasificador.py

import csv
import json
import math
import re

ARCHIVO_PRUEBA = "datos/mensajes_prueba.csv"
ARCHIVO_CONOCIMIENTO = "datos/conocimiento.json"
ARCHIVO_RESULTADOS = "datos/resultados_clasificacion.csv"

PALABRAS_IGNORADAS = {
    "a", "al", "ante", "bajo", "con", "contra", "de", "del",
    "desde", "durante", "en", "entre", "hacia", "hasta",
    "para", "por", "según", "sin", "sobre", "tras",
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "y", "e", "o", "u", "ni", "que", "se", "es", "son"
}


def tokenizar(texto):
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ0-9\s]", " ", texto)
    tokens = texto.split()

    return [
        token for token in tokens
        if token not in PALABRAS_IGNORADAS and len(token) > 1
    ]


def cargar_conocimiento():
    with open(ARCHIVO_CONOCIMIENTO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def clasificar_mensaje(mensaje, conocimiento):
    tokens = tokenizar(mensaje)

    clases = conocimiento["clases"]
    probabilidades_previas = conocimiento["probabilidades_previas"]
    probabilidades_condicionales = (
        conocimiento["probabilidades_condicionales"]
    )

    puntajes = {}
    votos = {
        "Spam": 0,
        "No Spam": 0
    }

    for clase in clases:
        puntaje = math.log(probabilidades_previas[clase])

        for token in tokens:
            probabilidad = probabilidades_condicionales[clase].get(
                token,
                1 / (
                    sum(conocimiento["tokens_por_clase"].values()) +
                    len(conocimiento["vocabulario"])
                )
            )

            puntaje += math.log(probabilidad)

        puntajes[clase] = puntaje

    for token in tokens:
        p_spam = probabilidades_condicionales["Spam"].get(token, 0)
        p_no_spam = probabilidades_condicionales["No Spam"].get(token, 0)

        if p_spam > p_no_spam:
            votos["Spam"] += 1
        elif p_no_spam > p_spam:
            votos["No Spam"] += 1

    if votos["Spam"] > votos["No Spam"]:
        consenso = "Spam"
    elif votos["No Spam"] > votos["Spam"]:
        consenso = "No Spam"
    else:
        consenso = max(puntajes, key=puntajes.get)

    prediccion_bayes = max(puntajes, key=puntajes.get)

    return {
        "tokens": tokens,
        "votos_spam": votos["Spam"],
        "votos_no_spam": votos["No Spam"],
        "puntaje_spam": puntajes["Spam"],
        "puntaje_no_spam": puntajes["No Spam"],
        "prediccion_bayes": prediccion_bayes,
        "prediccion_final": consenso
    }


def clasificar():
    conocimiento = cargar_conocimiento()

    with open(ARCHIVO_PRUEBA, "r", encoding="utf-8") as archivo:
        mensajes = list(csv.DictReader(archivo))

    resultados = []

    print("=== R008: CLASIFICADOR ===")

    for registro in mensajes:
        resultado = clasificar_mensaje(
            registro["mensaje"],
            conocimiento
        )

        salida = {
            "id": registro["id"],
            "mensaje": registro["mensaje"],
            "clase_real": registro["clase_real"],
            "clase_predicha": resultado["prediccion_final"],
            "prediccion_bayes": resultado["prediccion_bayes"],
            "votos_spam": resultado["votos_spam"],
            "votos_no_spam": resultado["votos_no_spam"],
            "tokens": " ".join(resultado["tokens"])
        }

        resultados.append(salida)

        print(f"\nMensaje {registro['id']}: {registro['mensaje']}")
        print(f"Tokens: {resultado['tokens']}")
        print(f"Votos Spam: {resultado['votos_spam']}")
        print(f"Votos No Spam: {resultado['votos_no_spam']}")
        print(f"Predicción Bayes: {resultado['prediccion_bayes']}")
        print(f"Predicción final: {resultado['prediccion_final']}")

    with open(ARCHIVO_RESULTADOS, "w", newline="", encoding="utf-8") as archivo:
        campos = [
            "id",
            "mensaje",
            "clase_real",
            "clase_predicha",
            "prediccion_bayes",
            "votos_spam",
            "votos_no_spam",
            "tokens"
        ]

        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(resultados)

    print(f"\nResultados guardados en: {ARCHIVO_RESULTADOS}")


if __name__ == "__main__":
    clasificar()
