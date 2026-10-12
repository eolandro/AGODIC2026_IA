import json
import re
import unicodedata


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


def clasificar(mensaje, tabla):
    palabras = sorted(set(tokenizar(mensaje)))
    conocidas = [palabra for palabra in palabras if palabra in tabla]
    probabilidades = [tabla[palabra]["probabilidad_spam_dada_palabra"] for palabra in conocidas]

    if not probabilidades:
        return "no_spam", 0.0, conocidas, 0, 0

    votos_spam = sum(1 for probabilidad in probabilidades if probabilidad > 0.5)
    votos_no_spam = len(probabilidades) - votos_spam
    resultado = "spam" if votos_spam > votos_no_spam else "no_spam"
    consenso = votos_spam / len(probabilidades)
    return resultado, consenso, conocidas, votos_spam, votos_no_spam


def main():
    with open("conocimiento_probabilistico.json", "r", encoding="utf-8") as archivo:
        tabla = json.load(archivo)["tokens"]

    with open("bandeja_prueba.txt", "r", encoding="utf-8") as archivo:
        mensajes = [linea.strip() for linea in archivo if linea.strip()]

    if len(mensajes) != 10:
        raise ValueError("Se requieren exactamente 10 mensajes nuevos.")

    clasificados = []
    print("CLASIFICADOR POR CONSENSO DEMOCRÁTICO")

    for numero, mensaje in enumerate(mensajes, 1):
        etiqueta, consenso, tokens, votos_spam, votos_no_spam = clasificar(mensaje, tabla)
        clasificados.append({
            "id": numero,
            "mensaje": mensaje,
            "tokens_conocidos": tokens,
            "votos_spam": votos_spam,
            "votos_no_spam": votos_no_spam,
            "consenso_spam": round(consenso, 4),
            "clasificacion": etiqueta
        })
        print(f"{numero}. {etiqueta.upper()} | consenso spam: {consenso:.2%}")

    with open("predicciones_spam.json", "w", encoding="utf-8") as archivo:
        json.dump(clasificados, archivo, ensure_ascii=False, indent=4)

    print("Archivo predicciones_spam.json generado correctamente.")


if __name__ == "__main__":
    main()
