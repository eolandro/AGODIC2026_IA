import json
import re
import sys
from pathlib import Path

TABLA = Path("tabla_probabilidades.json")
ENTRADA = Path("mensajes_nuevos.txt")
SALIDA = Path("mensajes_clasificados.json")
CANTIDAD = 10

# Método de consenso: DEMOCRACIA
# Cada token activado vota "spam" si su probabilidad es >= UMBRAL.
# El mensaje es spam si más de la mitad de los votos dicen spam.
UMBRAL = 0.5

STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del",
    "a", "ante", "bajo", "con", "contra", "de", "desde", "en", "entre", "hacia",
    "hasta", "para", "por", "segun", "sin", "sobre", "tras",
    "y", "e", "o", "u", "ni", "pero", "sino", "que", "como", "porque", "pues",
    "si", "aunque", "cuando", "donde", "mientras", "entonces", "tambien",
    "me", "te", "se", "nos", "mi", "tu", "su", "yo", "tu", "el", "ella", "es",
    "esta", "este", "esto", "ese", "esa", "muy", "mas", "ya", "no",
}


def tokenizar(texto):
    palabras = re.findall(r"[a-záéíóúñü]+", texto.lower())
    return {p for p in palabras if p not in STOPWORDS and len(p) > 2}


def cargar_tabla():
    if not TABLA.exists():
        sys.exit(f"No existe {TABLA}. Ejecuta primero R007_detokenizador.py")
    try:
        tabla = json.loads(TABLA.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"{TABLA} no es un JSON válido: {e}")
    if not isinstance(tabla, dict) or not tabla:
        sys.exit(f"{TABLA} no tiene el formato esperado. Vuelve a ejecutar R007_detokenizador.py")
    return tabla


def cargar_mensajes():
    if not ENTRADA.exists():
        sys.exit(f"No existe {ENTRADA}. Crea el archivo con {CANTIDAD} mensajes NUEVOS, uno por línea.")
    lineas = ENTRADA.read_text(encoding="utf-8").splitlines()
    mensajes = [linea.strip() for linea in lineas if linea.strip()]
    if len(mensajes) != CANTIDAD:
        sys.exit(f"{ENTRADA} debe tener exactamente {CANTIDAD} mensajes (tiene {len(mensajes)}).")
    return mensajes


def clasificar(mensaje, tabla):
    activados = {t: tabla[t]["probabilidad"] for t in tokenizar(mensaje) if t in tabla}
    votos_spam = sum(1 for p in activados.values() if p >= UMBRAL)
    es_spam = len(activados) > 0 and votos_spam > len(activados) / 2
    return activados, votos_spam, es_spam


def main():
    tabla = cargar_tabla()
    mensajes = cargar_mensajes()
    resultados = []
    
    print(" =================    TABLA CON MENSAJES ETIQUETADOS    ================= \n")

    for i, mensaje in enumerate(mensajes, start=1):
        activados, votos_spam, es_spam = clasificar(mensaje, tabla)
        resultados.append({
            "mensaje": mensaje,
            "tokens_activados": activados,
            "votos_spam": votos_spam,
            "votos_totales": len(activados),
            "spam": es_spam,
        })
        etiqueta = "SPAM" if es_spam else "NO SPAM"
        print(f"{i:>2}. [{etiqueta:7}] votos spam {votos_spam}/{len(activados)} | {mensaje}")

    SALIDA.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nArchivo generado: {SALIDA}")
    print("Siguiente paso: R009_metricas.py")


if __name__ == "__main__":
    main()
