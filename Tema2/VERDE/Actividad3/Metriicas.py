from pathlib import Path
import yaml
from Entrenador import ETIQUETA_SPAM


CARPETA = Path(__file__).resolve().parent
ARCHIVO_ENTRADA = CARPETA / "newclasificados.yaml"

def respuesta_a_booleano(respuesta):
    match respuesta.strip().upper():
        case "S":
            return True
        case "N":
            return False
        case _:
            return None 

def es_spam_predicho(registro):
    return registro["etiqueta"] == ETIQUETA_SPAM

def matriz_confusion(clasificados, verdades):
    pares = [(real, es_spam_predicho(r)) for r, real in zip(clasificados, verdades)]
    return {
        "TP": sum(1 for real, pred in pares if real and pred),
        "FP": sum(1 for real, pred in pares if not real and pred),
        "FN": sum(1 for real, pred in pares if real and not pred),
        "TN": sum(1 for real, pred in pares if not real and not pred),
    }


def dividir(numerador, denominador):
    match denominador:
        case 0:
            return None
        case _:
            return numerador / denominador


def metricas(m):
    total = m["TP"] + m["FP"] + m["FN"] + m["TN"]
    return {
        "Accuracy": dividir(m["TP"] + m["TN"], total),
        "Precision": dividir(m["TP"], m["TP"] + m["FP"]),
        "Recall": dividir(m["TP"], m["TP"] + m["FN"]),
        "Prevalence": dividir(m["TP"] + m["FN"], total),
    }


def formatear_metrica(valor):
    match valor:
        case None:
            return "indefinido"
        case _:
            return f"{valor:.4f}  ({valor * 100:.1f}%)"


def cargar_clasificados(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)

def preguntar_verdad(mensaje, numero, total):
    respuesta = input(f"\nMensaje {numero}/{total}:\n  \"{mensaje}\"\n¿Es spam? (S/N): ")
    verdad = respuesta_a_booleano(respuesta)
    if verdad is None:
        print("Respuesta inválida: escribe únicamente S o N.")
        return preguntar_verdad(mensaje, numero, total)
    return verdad


def obtener_verdades(clasificados):
    total = len(clasificados)
    return [preguntar_verdad(r["mensaje"], i, total)
            for i, r in enumerate(clasificados, start=1)]

def mostrar_resultados(m, resultado):
    print("\n=== Matriz de confusión (positivo = spam) ===")
    print(f"TP (spam detectado):     {m['TP']}")
    print(f"FP (falsa alarma):       {m['FP']}")
    print(f"FN (spam no detectado):  {m['FN']}")
    print(f"TN (no spam correcto):   {m['TN']}")
    print("\n=== Métricas ===")
    for nombre, valor in resultado.items():
        print(f"{nombre:<11}: {formatear_metrica(valor)}")

def main():
    clasificados = cargar_clasificados(ARCHIVO_ENTRADA)
    print(f"Se cargaron {len(clasificados)} mensajes de {ARCHIVO_ENTRADA.name}.")
    verdades = obtener_verdades(clasificados)
    m = matriz_confusion(clasificados, verdades)
    mostrar_resultados(m, metricas(m))

if __name__ == "__main__":
    main()
