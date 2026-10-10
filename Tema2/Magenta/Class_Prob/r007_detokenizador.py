# r007_detokenizador.py

import csv
import json
import math
import re
from collections import Counter

ARCHIVO_ENTRENAMIENTO = "datos/mensajes_entrenamiento.csv"
ARCHIVO_CONOCIMIENTO = "datos/conocimiento.json"

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


def cargar_mensajes():
    with open(ARCHIVO_ENTRENAMIENTO, "r", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def generar_conocimiento():
    mensajes = cargar_mensajes()

    conteo_tokens = {
        "Spam": Counter(),
        "No Spam": Counter()
    }

    cantidad_mensajes = {
        "Spam": 0,
        "No Spam": 0
    }

    tokens_por_clase = {
        "Spam": 0,
        "No Spam": 0
    }

    for registro in mensajes:
        clase = registro["clase"]
        tokens = tokenizar(registro["mensaje"])

        cantidad_mensajes[clase] += 1
        conteo_tokens[clase].update(tokens)
        tokens_por_clase[clase] += len(tokens)

    vocabulario = sorted(
        set(conteo_tokens["Spam"]) |
        set(conteo_tokens["No Spam"])
    )

    total_mensajes = len(mensajes)
    probabilidades_previas = {
        clase: cantidad / total_mensajes
        for clase, cantidad in cantidad_mensajes.items()
    }

    probabilidades_condicionales = {
        "Spam": {},
        "No Spam": {}
    }

    tamano_vocabulario = len(vocabulario)

    for token in vocabulario:
        for clase in ["Spam", "No Spam"]:
            frecuencia = conteo_tokens[clase][token]

            probabilidad = (
                frecuencia + 1
            ) / (
                tokens_por_clase[clase] + tamano_vocabulario
            )

            probabilidades_condicionales[clase][token] = probabilidad

    conocimiento = {
        "clases": ["Spam", "No Spam"],
        "cantidad_mensajes": cantidad_mensajes,
        "probabilidades_previas": probabilidades_previas,
        "tokens_por_clase": tokens_por_clase,
        "conteo_tokens": {
            clase: dict(conteo_tokens[clase])
            for clase in ["Spam", "No Spam"]
        },
        "vocabulario": vocabulario,
        "probabilidades_condicionales": probabilidades_condicionales
    }

    with open(ARCHIVO_CONOCIMIENTO, "w", encoding="utf-8") as archivo:
        json.dump(conocimiento, archivo, indent=4, ensure_ascii=False)

    print("=== R007: DETOKENIZADOR ===")
    print(f"Mensajes procesados: {total_mensajes}")
    print(f"Vocabulario generado: {tamano_vocabulario}")
    print(f"Archivo generado: {ARCHIVO_CONOCIMIENTO}")

    print("\nTabla de probabilidades:")
    print(f"{'Token':20} {'P(token|Spam)':20} {'P(token|No Spam)':20}")

    for token in vocabulario:
        p_spam = probabilidades_condicionales["Spam"][token]
        p_no_spam = probabilidades_condicionales["No Spam"][token]

        print(
            f"{token:20} "
            f"{p_spam:<20.6f} "
            f"{p_no_spam:<20.6f}"
        )


if __name__ == "__main__":
    generar_conocimiento()
