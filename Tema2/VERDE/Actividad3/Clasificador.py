import math
from pathlib import Path
import yaml
from Entrenador import ETIQUETA_SPAM, ETIQUETA_NO_SPAM
from Detokenizador import tokenizar, CLASES


CARPETA = Path(__file__).resolve().parent
ARCHIVO_MENSAJES = CARPETA / "newmsgs.yaml"
ARCHIVO_PROBS = CARPETA / "probs.yaml"
ARCHIVO_SALIDA = CARPETA / "newclasificados.yaml"
UMBRAL = 0.5


def palabras_conocidas(tokens, tabla):
    return [t for t in tokens if t in tabla["palabras"]]

def log_puntaje(tokens, tabla, clase):
    return (math.log(tabla["priori"][clase])
            + sum(math.log(tabla["palabras"][t][clase])
                  for t in palabras_conocidas(tokens, tabla)))

def sigmoide(x):
    match x >= 0:
        case True:
            return 1 / (1 + math.exp(-x))
        case False:
            e = math.exp(x)
            return e / (1 + e)

def probabilidad_spam(tokens, tabla):
    diferencia = (log_puntaje(tokens, tabla, ETIQUETA_SPAM)
                  - log_puntaje(tokens, tabla, ETIQUETA_NO_SPAM))
    return sigmoide(diferencia)


def etiqueta_de(probabilidad):
    match probabilidad > UMBRAL:
        case True:
            return ETIQUETA_SPAM
        case False:
            return ETIQUETA_NO_SPAM


def clasificar_mensaje(mensaje, tabla):
    p = probabilidad_spam(tokenizar(mensaje), tabla)
    return {"mensaje": mensaje,
            "etiqueta": etiqueta_de(p),
            "probabilidad_spam": round(p, 4)}


def clasificar(mensajes, tabla):
    return [clasificar_mensaje(m, tabla) for m in mensajes]

def cargar_yaml(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)

def guardar_clasificados(ruta, clasificados):
    with open(ruta, "w", encoding="utf-8") as archivo:
        yaml.safe_dump(clasificados, archivo, allow_unicode=True, sort_keys=False)

def mostrar_resultado(numero, registro):
    print(f"{numero:>2}. [{registro['etiqueta']:<7}] "
          f"P(spam)={registro['probabilidad_spam']:.4f}  {registro['mensaje']}")

def main():
    mensajes = cargar_yaml(ARCHIVO_MENSAJES)
    tabla = cargar_yaml(ARCHIVO_PROBS)
    clasificados = clasificar(mensajes, tabla)
    guardar_clasificados(ARCHIVO_SALIDA, clasificados)
    for numero, registro in enumerate(clasificados, start=1):
        mostrar_resultado(numero, registro)
    print(f"\nListo: {len(clasificados)} mensajes clasificados en {ARCHIVO_SALIDA.name}.")

if __name__ == "__main__":
    main()