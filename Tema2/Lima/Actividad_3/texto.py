import re
import unicodedata

ARTICULOS = {"el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del"}
PREPOSICIONES = {
    "a", "ante", "bajo", "con", "contra", "de", "desde", "durante", "en", "entre",
    "hacia", "hasta", "mediante", "para", "por", "segun", "sin", "sobre", "tras",
}
CONECTORES = {
    "y", "e", "o", "u", "ni", "pero", "sino", "que", "como", "si", "porque", "pues",
    "aunque", "cuando", "donde", "mientras", "entonces", "ademas", "tambien",
}

OTRAS = {
    "yo", "tu", "tus", "te", "ti", "me", "mi", "mis", "se", "su", "sus", "nos",
    "le", "les", "es", "son", "ya", "muy", "mas", "este", "esta", "esto", "no",
}
PALABRAS_VACIAS = ARTICULOS | PREPOSICIONES | CONECTORES | OTRAS


def quitar_acentos(palabra):
    descompuesta = unicodedata.normalize("NFD", palabra)
    return "".join(c for c in descompuesta if unicodedata.category(c) != "Mn")


def tokenizar(mensaje):
    mensaje = re.sub(r"\S*(://|www\.)\S*", " ", mensaje.lower())
    tokens = set()
    for palabra in re.findall(r"[a-záéíóúüñ]+", mensaje):
        palabra = quitar_acentos(palabra)
        if len(palabra) > 1 and palabra not in PALABRAS_VACIAS:
            tokens.add(palabra)
    return tokens
