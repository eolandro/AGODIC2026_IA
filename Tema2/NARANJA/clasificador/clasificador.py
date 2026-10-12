import os
import sys
from statistics import mean, median, multimode
import json
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


def cargar_mensajes_texto(ruta):
    if ruta.endswith((".json", ".yaml", ".yml")):
        datos = cargar(ruta)
        if isinstance(datos, dict):
            datos = datos.get("mensajes", [])
        return [m["texto"] if isinstance(m, dict) else str(m) for m in datos]
    with open(ruta, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


TABLA = "tabla_probabilidades.json"
ENTRENAMIENTO = "mensajes_etiquetados.json"
SALIDA = "mensajes_clasificados.json"
METODOS = ["media", "mediana", "democracia", "moda"]
N_MENSAJES = 10


def evidencias(texto, tabla):
    return [(t, tabla[t]) for t in tokenizar(texto) if t in tabla]


def clasificar(lista_ev, metodo, umbral):
    if metodo == "moda":
        votos = [sum(1 for _, p in ev if p > umbral) for ev in lista_ev]
        activados = [v for v in votos if v > 0]
        moda = min(multimode(activados)) if activados else None
        return [(moda is not None and v >= moda, v) for v in votos], moda

    resultados = []
    for ev in lista_ev:
        probs = [p for _, p in ev]
        if not probs:
            resultados.append((False, None))
        elif metodo == "media":
            m = mean(probs)
            resultados.append((m > umbral, m))
        elif metodo == "mediana":
            m = median(probs)
            resultados.append((m > umbral, m))
        elif metodo == "democracia":
            a_favor = sum(1 for p in probs if p > umbral)
            en_contra = len(probs) - a_favor
            resultados.append((a_favor > en_contra, f"{a_favor} vs {en_contra}"))
    return resultados, None


def elegir_metodo():
    print("\nMétodo de consenso:")
    for i, m in enumerate(METODOS, 1):
        print(f"  {i}) {m}")
    while True:
        r = input("Elige (1-4) [1]: ").strip() or "1"
        if r in ("1", "2", "3", "4"):
            return METODOS[int(r) - 1]


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Uso: python R008_clasificador.py mensajes_nuevos.txt [metodo] [umbral]")
    mensajes = cargar_mensajes_texto(sys.argv[1])[:N_MENSAJES]
    metodo = sys.argv[2].lower() if len(sys.argv) > 2 else elegir_metodo()
    if metodo not in METODOS:
        raise SystemExit(f"Método no válido. Opciones: {', '.join(METODOS)}")
    umbral = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5

    if os.path.exists(ENTRENAMIENTO):
        vistos = {quitar_acentos(m["texto"]).strip() for m in cargar(ENTRENAMIENTO)["mensajes"]}
        repetidos = [m for m in mensajes if quitar_acentos(m).strip() in vistos]
        if repetidos:
            raise SystemExit("ERROR: estos mensajes ya se usaron en el entrenamiento:\n  - "
                             + "\n  - ".join(repetidos) + "\nUsa 10 mensajes realmente nuevos.")

    datos = cargar(TABLA)
    tabla = {r["token"]: r["P(spam|w)"] for r in datos["tokens"]}
    lista_ev = [evidencias(m, tabla) for m in mensajes]

    print("=" * 60)
    print(f" CLASIFICADOR - método: {metodo.upper()}   umbral: {umbral}")
    print("=" * 60)

    todos = {m: clasificar(lista_ev, m, umbral)[0] for m in METODOS}
    resultado, moda = clasificar(lista_ev, metodo, umbral)
    if metodo == "moda":
        print(f" Moda de tokens de spam por mensaje: {moda}")

    salida = []
    for i, (texto, ev, (es_spam, puntaje)) in enumerate(zip(mensajes, lista_ev, resultado), 1):
        etiqueta = "SPAM" if es_spam else "NO SPAM"
        detalle = ", ".join(f"{t}={p:.2f}" for t, p in ev) or "(ningún token conocido)"
        print(f"\n[{i:>2}] {texto}")
        print(f"     tokens: {detalle}")
        print(f"     puntaje: {puntaje if not isinstance(puntaje, float) else round(puntaje, 3)}  =>  {etiqueta}")
        salida.append({
            "id": i,
            "texto": texto,
            "tokens_en_tabla": {t: p for t, p in ev},
            "puntaje": round(puntaje, 4) if isinstance(puntaje, float) else puntaje,
            "spam": es_spam,
        })

    print("\n Comparativa de métodos (S = spam, - = no spam):")
    print("   msg  " + "  ".join(f"{m:<10}" for m in METODOS))
    for i in range(len(mensajes)):
        print(f"   {i+1:>3}  " + "  ".join(f"{'S' if todos[m][i][0] else '-':<10}" for m in METODOS))

    guardar({
        "descripcion": "Mensajes nuevos etiquetados por el sistema (R008 Clasificador)",
        "metodo_consenso": metodo,
        "umbral": umbral,
        "tabla_usada": TABLA,
        "mensajes": salida,
    }, SALIDA)


if __name__ == "__main__":
    main()
