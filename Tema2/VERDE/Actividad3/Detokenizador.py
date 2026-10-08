from collections import Counter
from pathlib import Path
import re
import yaml
from Entrenador import ETIQUETA_SPAM, ETIQUETA_NO_SPAM, hay_ambas_clases


CARPETA = Path(__file__).resolve().parent
ARCHIVO_ENTRADA = CARPETA / "msg_etiquetados.yaml"
ARCHIVO_SALIDA = CARPETA / "probs.yaml"
CLASES = (ETIQUETA_SPAM, ETIQUETA_NO_SPAM)


def tokenizar(texto):
    return re.findall(r"\w+", texto.lower())

def tokens_de_clase(etiquetados, clase):
    return [t
            for r in etiquetados if r["etiqueta"] == clase
            for t in tokenizar(r["mensaje"])]

def vocabulario(etiquetados):
    return sorted({t for r in etiquetados for t in tokenizar(r["mensaje"])})

def probabilidad_a_priori(etiquetados, clase):
    return sum(1 for r in etiquetados if r["etiqueta"] == clase) / len(etiquetados)


def probabilidad_palabra(conteo, total_tokens, tam_vocabulario):
    return (conteo + 1) / (total_tokens + tam_vocabulario)


def tabla_probabilidades(etiquetados):
    vocab = vocabulario(etiquetados)
    tokens = {c: tokens_de_clase(etiquetados, c) for c in CLASES}
    conteos = {c: Counter(tokens[c]) for c in CLASES}
    return {
        "priori": {c: probabilidad_a_priori(etiquetados, c) for c in CLASES},
        "palabras": {
            p: {c: probabilidad_palabra(conteos[c][p], len(tokens[c]), len(vocab))
                for c in CLASES}
            for p in vocab
        },
    }


def cargar_etiquetados(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)

def guardar_probs(ruta, tabla):
    with open(ruta, "w", encoding="utf-8") as archivo:
        yaml.safe_dump(tabla, archivo, allow_unicode=True, sort_keys=False)

def main():
    etiquetados = cargar_etiquetados(ARCHIVO_ENTRADA)
    if not hay_ambas_clases(etiquetados):
        print("Error: msg_etiquetados.yaml debe tener al menos un spam y un no spam. "
              "Ejecuta entrenador.py primero.")
        return
    tabla = tabla_probabilidades(etiquetados)
    guardar_probs(ARCHIVO_SALIDA, tabla)
    print(f"Se procesaron {len(etiquetados)} mensajes de {ARCHIVO_ENTRADA.name}.")
    print(f"Vocabulario: {len(tabla['palabras'])} palabras distintas.")
    print(f"Probabilidades a priori: {tabla['priori']}")
    print(f"Tabla guardada en {ARCHIVO_SALIDA.name}.")


if __name__ == "__main__":
    main()
