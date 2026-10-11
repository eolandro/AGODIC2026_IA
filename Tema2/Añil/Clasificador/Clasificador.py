import json
import re
import string
import sys

archivo_entrada = "mensajes_nuevos.txt"
archivo_tabla = "tabla_probabilidades.json"
archivo_salida = "mensajes_clasificados.json"
spam = "spam"
NOspam = "no_spam"

umbral = 0.5    # P(spam | token) por encima de este valor vota spam; por debajo, no spam

stopwords = {
    # artículos
    "el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del",
    # preposiciones
    "a", "ante", "bajo", "con", "contra", "de", "desde", "durante", "en", "entre",
    "hacia", "hasta", "mediante", "para", "por", "segun", "según", "sin", "sobre", "tras",
    # conectores / conjunciones
    "y", "e", "o", "u", "ni", "pero", "sino", "que", "como", "si", "porque", "pues",
    "aunque", "cuando", "donde", "mientras", "entonces", "ademas", "además",
    # pronombres y negación
    "tu", "tus", "te", "ti", "nos", "no",
}

patrón_dominio = re.compile(r"[a-z0-9\-]+\.[a-z]{2,4}(/|$)", re.IGNORECASE)


def leer_mensajes(ruta):
    with open(ruta, encoding="utf-8") as f:
        return [linea.strip() for linea in f if linea.strip()]

def leer_tabla(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)

def tokenizar(mensaje):
    """Misma tokenización del Detokenizador: minúsculas, sin puntuación; descarta URLs,
    dominios, números y símbolos; quita stopwords. Devuelve un set."""
    tokens = set()
    for fragmento in mensaje.lower().split():
        fragmento = fragmento.strip(string.punctuation + "¡¿")
        if re.search(r"\d|://|www\.", fragmento):
            continue
        if patrón_dominio.search(fragmento):
            continue
        for palabra in re.findall(r"[a-záéíóúüñ]+", fragmento):
            if palabra not in stopwords:
                tokens.add(palabra)
    return tokens

def democracia(probs):
    """Método de consenso: cada token conocido vota spam si P(spam|token) > umbral y
    no spam si P < umbral (P == umbral se abstiene). Gana la mayoría; None si hay empate."""
    votos_spam = sum(1 for p in probs if p > umbral)
    votos_no_spam = sum(1 for p in probs if p < umbral)
    if votos_spam > votos_no_spam:
        return spam
    if votos_spam < votos_no_spam:
        return NOspam
    return None

def clasificar(mensaje):
    """Devuelve (etiqueta, cantidad de tokens conocidos, si se usó desempate)."""
    probs = [tokens_tabla[t]["p_spam"] for t in tokenizar(mensaje) if t in tokens_tabla]
    etiqueta = democracia(probs)
    if etiqueta is None:     # empate o sin tokens conocidos: se decide con la prevalencia
        return (spam if prevalencia_spam >= umbral else NOspam), len(probs), True
    return etiqueta, len(probs), False

def guardar(registros, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)

#-------------------------------------- MAIN --------------------------------------#
ruta_entrada = sys.argv[1] if len(sys.argv) > 1 else archivo_entrada
ruta_salida = sys.argv[2] if len(sys.argv) > 2 else archivo_salida

print("* * * CLASIFICADOR * * *\n")
try:
    mensajes = leer_mensajes(ruta_entrada)
except FileNotFoundError:
    print(f"No se encontró el archivo '{ruta_entrada}'.")
    sys.exit()
try:
    tabla = leer_tabla(archivo_tabla)
except FileNotFoundError:
    print(f"No se encontró el archivo '{archivo_tabla}'. Ejecuta primero el Detokenizador.")
    sys.exit()

tokens_tabla = tabla["tokens"]
prevalencia_spam = tabla["totales"]["prevalencia_spam"]

if len(mensajes) != 10:
    print(f"Aviso: se esperaban 10 mensajes y el archivo tiene {len(mensajes)}.")

print("Método de consenso: democracia\n")
registros = []
for i, m in enumerate(mensajes, 1):
    etiqueta, conocidos, desempate = clasificar(m)
    registros.append({"mensaje": m, "etiqueta": etiqueta})
    nota = "  (desempate por prevalencia)" if desempate else ""
    resumen = m if len(m) <= 55 else m[:52] + "..."
    print(f"{i:>2}. {etiqueta:<8} [{conocidos} tokens] {resumen}{nota}")

guardar(registros, ruta_salida)
total_spam = sum(1 for r in registros if r["etiqueta"] == spam)
print(f"\nArchivo '{ruta_salida}' generado.")
print(f"Spam: {total_spam} | No spam: {len(registros) - total_spam} | Total: {len(registros)}")