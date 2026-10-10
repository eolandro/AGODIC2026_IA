import json
import re
import sys
from pathlib import Path

ENTRADA = Path("mensajes_etiquetados.json")
SALIDA = Path("tabla_probabilidades.json")

# Artículos, preposiciones y conectores que se eliminan
STOPWORDS = {
    # artículos
    "el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del",
    # preposiciones
    "a", "ante", "bajo", "con", "contra", "de", "desde", "en", "entre", "hacia",
    "hasta", "para", "por", "segun", "sin", "sobre", "tras",
    # conectores
    "y", "e", "o", "u", "ni", "pero", "sino", "que", "como", "porque", "pues",
    "si", "aunque", "cuando", "donde", "mientras", "entonces", "tambien",
    # pronombres y palabras muy comunes
    "me", "te", "se", "nos", "mi", "tu", "su", "yo", "tu", "el", "ella", "es",
    "esta", "este", "esto", "ese", "esa", "muy", "mas", "ya", "no",
}


def tokenizar(texto):
    palabras = re.findall(r"[a-záéíóúñü]+", texto.lower())
    return {p for p in palabras if p not in STOPWORDS and len(p) > 2}


def cargar_etiquetados():
    if not ENTRADA.exists():
        sys.exit(f"No existe {ENTRADA}. Ejecuta primero R006_entrenador.py")
    try:
        mensajes = json.loads(ENTRADA.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"{ENTRADA} no es un JSON válido: {e}")
    valido = isinstance(mensajes, list) and mensajes and all(
        isinstance(m, dict) and isinstance(m.get("mensaje"), str) and isinstance(m.get("spam"), bool)
        for m in mensajes
    )
    if not valido:
        sys.exit(f"{ENTRADA} no tiene el formato esperado. Vuelve a ejecutar R006_entrenador.py")
    return mensajes


def main():
    mensajes = cargar_etiquetados()

    total = {}  
    spam = {}   
    for m in mensajes:
        for token in tokenizar(m["mensaje"]):
            total[token] = total.get(token, 0) + 1
            if m["spam"]:
                spam[token] = spam.get(token, 0) + 1


    tabla = {
        token: {
            "spam": spam[token],
            "total": total[token],
            "probabilidad": round(spam[token] / total[token], 4),
        }
        for token in spam
    }
    tabla = dict(sorted(tabla.items(), key=lambda x: (-x[1]["probabilidad"], x[0])))

    SALIDA.write_text(json.dumps(tabla, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{'Token':20}{'Spam':>6}{'Total':>7}{'P(spam|token)':>16}")
    for token, d in tabla.items():
        print(f"{token:20}{d['spam']:>6}{d['total']:>7}{d['probabilidad']:>16.4f}")

    print(f"\nTokens en la tabla: {len(tabla)}")
    print(f"\n Archivo generado: {SALIDA}")
    print(" Siguiente paso: R008_clasificador.py")


if __name__ == "__main__":
    main()
