import json
import re
import string
import sys

archivo_entrada = "entrenamiento_etiquetado.json"
archivo_salida = "tabla_probabilidades.json"
spam = "spam"
NOspam = "no_spam"

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

def leer_registros(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)

def tokenizar(mensaje):
    """Minúsculas, sin puntuación; descarta URLs, dominios, números y símbolos; quita stopwords.
    Devuelve un set: cada palabra cuenta una sola vez por mensaje."""
    tokens = set()
    for fragmento in mensaje.lower().split():
        fragmento = fragmento.strip(string.punctuation + "¡¿")
        if re.search(r"\d|://|www\.", fragmento):      # URLs y números ($10,000usd, 90%, 7?)
            continue
        if patrón_dominio.search(fragmento):           # dominios sin http (dinerofacil.net)
            continue
        for palabra in re.findall(r"[a-záéíóúüñ]+", fragmento):   # quita ¡ ! ¿ ? , : :) etc.
            if palabra not in stopwords:
                tokens.add(palabra)
    return tokens

def guardar(tabla, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(tabla, f, ensure_ascii=False, indent=2)

#-------------------------------------- MAIN --------------------------------------#
ruta_entrada = sys.argv[1] if len(sys.argv) > 1 else archivo_entrada
ruta_salida = sys.argv[2] if len(sys.argv) > 2 else archivo_salida

print("* * * DETOKENIZADOR * * *\n")
try:
    registros = leer_registros(ruta_entrada)
except FileNotFoundError:
    print(f"No se encontró el archivo '{ruta_entrada}'.")
    sys.exit()

# Conteo de mensajes spam / no spam que contienen cada token
conteo = {}
for r in registros:
    for token in tokenizar(r["mensaje"]):
        conteo.setdefault(token, {spam: 0, NOspam: 0})
        conteo[token][r["etiqueta"]] += 1

total_mensajes = len(registros)
total_spam = sum(1 for r in registros if r["etiqueta"] == spam)
total_no_spam = total_mensajes - total_spam
prevalencia_spam = total_spam / total_mensajes          # P(spam)
prevalencia_no_spam = total_no_spam / total_mensajes    # P(no spam)

# Probabilidad condicional: P(spam | token) = mensajes spam con el token / mensajes con el token
tokens = {}
for token, c in conteo.items():
    total = c[spam] + c[NOspam]
    prob_spam = c[spam] / total
    tokens[token] = {
        "spam": c[spam],
        "no_spam": c[NOspam],
        "p_spam": round(prob_spam, 4),
    }

# Orden: más frecuentes primero (spam + no_spam), luego alfabético
tokens = dict(sorted(tokens.items(), key=lambda t: (-(t[1]["spam"] + t[1]["no_spam"]), t[0])))
tabla = {
    "totales": {
        "mensajes": total_mensajes,
        "spam": total_spam,
        "no_spam": total_no_spam,
        "prevalencia_spam": round(prevalencia_spam, 4),
        "prevalencia_no_spam": round(prevalencia_no_spam, 4),
    },
    "tokens": tokens,
}
guardar(tabla, ruta_salida)
print(f"Mensajes: {total_mensajes} | Spam: {total_spam} | No spam: {total_no_spam}")
print(f"Tokens distintos: {len(tokens)}")
print(f"\n{'token':<15}{'spam':>5}{'no_spam':>9}{'P(spam|t)':>11}")
for token, d in list(tokens.items())[:10]:
    print(f"{token:<15}{d['spam']:>5}{d['no_spam']:>9}{d['p_spam']:>11}")
print(f"\nArchivo '{ruta_salida}' generado.")