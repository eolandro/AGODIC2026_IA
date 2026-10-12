import json
import os
import re
import unicodedata


ARTICULOS = {
    "el", "la", "los", "las", "lo", "un", "una", "unos", "unas",
    "al", "del",  
}
PREPOSICIONES = {
    "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante",
    "en", "entre", "hacia", "hasta", "mediante", "para", "por", "segun",
    "sin", "so", "sobre", "tras", "versus", "via",
}
CONECTORES = {
    "y", "e", "ni", "o", "u", "pero", "mas", "sino", "aunque", "embargo",
  
    "que", "porque", "pues", "como", "si", "entonces", "luego", "asi",
    "tanto", "ya",

    "cuando", "mientras", "donde", "tambien", "ademas", "incluso", "tampoco",
}

PRONOMBRES = {
    "yo", "tu", "el", "ella", "nosotros", "nosotras", "ustedes", "ellos", "ellas",
    "me", "te", "se", "nos", "le", "les", "mi", "mis", "tus", "su", "sus",
    "ti", "conmigo", "contigo", "nuestro", "nuestra", "nuestros", "nuestras",
    "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "esto", "eso",
}
PALABRAS_VACIAS = ARTICULOS | PREPOSICIONES | CONECTORES | PRONOMBRES


def quitar_acentos(texto):
    texto = texto.lower().replace("ñ", "\0")
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.replace("\0", "ñ")


def tokenizar(mensaje):
    texto = quitar_acentos(mensaje)
    palabras = re.findall(r"[a-zñ0-9]+", texto)
    tokens = []
    for p in palabras:
        if p in PALABRAS_VACIAS or len(p) < 2 or p.isdigit():
            continue
        if p not in tokens:
            tokens.append(p)
    return tokens


def guardar(datos, ruta):
    if ruta.endswith((".yaml", ".yml")):
        import yaml  # pip install pyyaml
        with open(ruta, "w", encoding="utf-8") as f:
            yaml.safe_dump(datos, f, allow_unicode=True, sort_keys=False)
    else:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"\n>> Archivo de conocimiento generado: {os.path.abspath(ruta)}")


def cargar(ruta):
    if not os.path.exists(ruta):
        raise SystemExit(f"No existe el archivo '{ruta}'. Ejecuta primero el programa anterior.")
    with open(ruta, encoding="utf-8") as f:
        if ruta.endswith((".yaml", ".yml")):
            import yaml
            return yaml.safe_load(f)
        return json.load(f)


ENTRADA = "mensajes_etiquetados.json"
SALIDA = "tabla_probabilidades.json"


def main():
    datos = cargar(ENTRADA)
    mensajes = datos["mensajes"]
    N = len(mensajes)
    n_spam = sum(1 for m in mensajes if m["spam"])
    n_ham = N - n_spam
    p_spam = n_spam / N

    print("=" * 60)
    print(" DETOKENIZADOR - Tokens por mensaje")
    print("=" * 60)
    conteo = {}  
    for m in mensajes:
        tokens = tokenizar(m["texto"])
        etiqueta = "SPAM" if m["spam"] else "NO SPAM"
        print(f"[{m['id']:>2}] {etiqueta:<8} {tokens}")
        for t in tokens:
            conteo.setdefault(t, [0, 0])
            conteo[t][0 if m["spam"] else 1] += 1

    tabla = []
    descartados = sorted(t for t, (a, b) in conteo.items() if a == 0)
    for token, (a, b) in conteo.items():
        if a == 0:
            continue  
        c, d = n_spam - a, n_ham - b
        p_w = (a + b) / N
        p_w_dado_spam = a / n_spam if n_spam else 0.0
        p_spam_dado_w = a / (a + b)
        bayes = p_w_dado_spam * p_spam / p_w  
        tabla.append({
            "token": token,
            "matriz": {"w_spam": a, "w_no_spam": b, "no_w_spam": c, "no_w_no_spam": d},
            "P(w)": round(p_w, 4),
            "P(w|spam)": round(p_w_dado_spam, 4),
            "P(spam|w)": round(p_spam_dado_w, 4),
            "comprobacion_bayes": round(bayes, 4),
        })
    tabla.sort(key=lambda r: (-r["P(spam|w)"], -(r["matriz"]["w_spam"] + r["matriz"]["w_no_spam"]), r["token"]))

    print("\n" + "=" * 60)
    print(" TABLA DE PROBABILIDADES")
    print("=" * 60)
    print(f" P(spam) = {n_spam}/{N} = {p_spam:.2f}\n")
    print(f" {'token':<16}{'spam':>5}{'¬spam':>7}{'P(spam|w)':>12}")
    for r in tabla:
        mz = r["matriz"]
        print(f" {r['token']:<16}{mz['w_spam']:>5}{mz['w_no_spam']:>7}{r['P(spam|w)']:>12.2f}")

    print(f"\n Tokens descartados (nunca aparecieron en spam): {len(descartados)}")
    print("   " + ", ".join(descartados))

    guardar({
        "descripcion": "Tabla de probabilidades condicionales P(spam|token) (R007 DeTokenizador)",
        "origen": ENTRADA,
        "total_mensajes": N,
        "total_spam": n_spam,
        "total_no_spam": n_ham,
        "P(spam)": round(p_spam, 4),
        "tokens": tabla,
        "tokens_descartados": descartados,
    }, SALIDA)


if __name__ == "__main__":
    main()
