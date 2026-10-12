import json
import re
import unicodedata
from collections import Counter


PALABRAS_VACIAS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del",
    "a", "ante", "bajo", "con", "contra", "de", "desde", "durante", "en", "entre",
    "hacia", "hasta", "para", "por", "segun", "sin", "sobre", "tras", "y", "e", "o",
    "u", "ni", "que", "pero", "sino", "aunque", "porque", "como", "cuando", "donde",
    "si", "entonces", "ademas", "tambien", "ya"
}


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")


def tokenizar(texto):
    palabras = re.findall(r"[a-z0-9]+", normalizar(texto))
    return [palabra for palabra in palabras if palabra not in PALABRAS_VACIAS and len(palabra) > 1]


def main():
    with open("corpus_etiquetado.json", "r", encoding="utf-8") as archivo:
        mensajes = json.load(archivo)

    if len(mensajes) != 10:
        raise ValueError("Se requieren exactamente 10 mensajes etiquetados.")

    cantidad_spam = sum(1 for item in mensajes if item["etiqueta"] == "spam")
    cantidad_no_spam = len(mensajes) - cantidad_spam
    conteo_spam = Counter()
    conteo_no_spam = Counter()

    for item in mensajes:
        palabras = set(tokenizar(item["mensaje"]))
        if item["etiqueta"] == "spam":
            conteo_spam.update(palabras)
        else:
            conteo_no_spam.update(palabras)

    probabilidad_spam = (cantidad_spam + 1) / (len(mensajes) + 2)
    probabilidad_no_spam = 1 - probabilidad_spam
    vocabulario = sorted(set(conteo_spam) | set(conteo_no_spam))
    tabla = {}

    for palabra in vocabulario:
        p_palabra_spam = (conteo_spam[palabra] + 1) / (cantidad_spam + 2)
        p_palabra_no_spam = (conteo_no_spam[palabra] + 1) / (cantidad_no_spam + 2)
        numerador = p_palabra_spam * probabilidad_spam
        p_spam_palabra = numerador / (
            numerador + p_palabra_no_spam * probabilidad_no_spam
        )
        tabla[palabra] = {
            "apariciones_spam": conteo_spam[palabra],
            "apariciones_no_spam": conteo_no_spam[palabra],
            "probabilidad_spam_dada_palabra": round(p_spam_palabra, 6)
        }

    resultado = {
        "total_mensajes": len(mensajes),
        "mensajes_spam": cantidad_spam,
        "mensajes_no_spam": cantidad_no_spam,
        "probabilidad_spam": round(probabilidad_spam, 6),
        "tokens": tabla
    }

    with open("conocimiento_probabilistico.json", "w", encoding="utf-8") as archivo:
        json.dump(resultado, archivo, ensure_ascii=False, indent=4)

    print("DETOKENIZADOR")
    print(f"Tokens obtenidos: {len(vocabulario)}")
    print("Archivo conocimiento_probabilistico.json generado correctamente.")


if __name__ == "__main__":
    main()
