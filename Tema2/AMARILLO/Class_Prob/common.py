"""Funciones compartidas: lectura/escritura (txt, json, yaml) y tokenización."""
import json
import os
import re
import unicodedata

try:
    import yaml                                             
except ImportError:
    yaml = None

try:                                                    
    from nltk.stem.snowball import SnowballStemmer
    _STEMMER = SnowballStemmer("spanish")
except ImportError:
    _STEMMER = None


def quitar_acentos(t):
    """'Cancún' -> 'Cancun'."""
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del",
    "a", "ante", "bajo", "con", "contra", "de", "desde", "en", "entre", "hacia",
    "hasta", "para", "por", "segun", "sin", "sobre", "tras",
    "y", "e", "o", "u", "ni", "que", "pero", "sino", "aunque", "porque", "pues",
    "como", "si", "mas", "cuando", "donde", "mientras", "entonces",
    "me", "te", "se", "nos", "mi", "tu", "su", "es", "son", "fue", "ha", "han",
    "he", "has", "este", "esta", "esto", "ese", "esa", "eso", "muy", "ya",
}


def tokenizar(texto):
    """Minúsculas, sin acentos, separa en palabras."""
    return re.findall(r"[a-z0-9]+", quitar_acentos(texto.lower()))


def limpiar(tokens):
    """Elimina artículos, preposiciones, conectores y palabras de 1 letra."""
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


def raiz(palabra):
    """Raíz en español si nltk está instalado; si no, la palabra tal cual."""
    return _STEMMER.stem(palabra) if _STEMMER else palabra


def procesar(texto):
    """Pipeline completo: tokeniza, quita stopwords y saca la raíz."""
    return [raiz(t) for t in limpiar(tokenizar(texto))]


def cargar(ruta):
    """Carga .json, .yaml/.yml o .txt (una línea = un elemento)."""
    ext = os.path.splitext(ruta)[1].lower()
    with open(ruta, encoding="utf-8") as f:
        if ext == ".json":
            return json.load(f)
        if ext in (".yaml", ".yml"):
            if yaml is None:
                raise SystemExit("Falta PyYAML: pip install pyyaml")
            return yaml.safe_load(f)
        return [ln.strip() for ln in f if ln.strip()]


def guardar(ruta, datos):
    """Guarda en .json o .yaml/.yml según la extensión."""
    ext = os.path.splitext(ruta)[1].lower()
    with open(ruta, "w", encoding="utf-8") as f:
        if ext in (".yaml", ".yml"):
            if yaml is None:
                raise SystemExit("Falta PyYAML: pip install pyyaml")
            yaml.safe_dump(datos, f, allow_unicode=True, sort_keys=False)
        else:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"Archivo generado: {ruta}")


def mensajes_de(datos):
    """Acepta lista de strings o lista de dicts con clave 'mensaje'."""
    return [d["mensaje"] if isinstance(d, dict) else d for d in datos]


def obtener_mensajes(ruta=None, n=10):
    """El usuario da los n mensajes: desde un archivo (.txt, .json, .yaml)
    o escribiéndolos a mano si deja la ruta vacía."""
    if ruta is None:
        ruta = input(
            f"Archivo con los {n} mensajes (.txt, .json o .yaml)\n"
            "o Enter para escribirlos a mano: "
        ).strip().strip('"')
    if ruta:
        if os.path.exists(ruta):
            mensajes = mensajes_de(cargar(ruta))
            if len(mensajes) == n:
                return mensajes
            print(f"El archivo tiene {len(mensajes)} mensajes y se necesitan exactamente {n}.")
        else:
            print(f"No encontré '{ruta}'.")
        print("Escríbelos a mano.")
    mensajes = []
    while len(mensajes) < n:
        m = input(f"Mensaje {len(mensajes) + 1}/{n}: ").strip()
        if m:
            mensajes.append(m)
    return mensajes


def preguntar_etiqueta(texto):
    """El supervisor responde s (spam) o n (no spam)."""
    while True:
        r = input(f'\n"{texto}"\n¿Es spam? (s/n): ').strip().lower()
        if r in ("s", "n"):
            return "spam" if r == "s" else "no_spam"
        print("Responde 's' o 'n'.")
