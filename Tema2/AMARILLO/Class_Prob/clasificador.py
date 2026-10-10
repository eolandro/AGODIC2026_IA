import statistics
import sys

from common import cargar, guardar, obtener_mensajes, procesar

METODOS = ("democracia", "media", "mediana", "moda")


def clasificar(mensaje, tabla, metodo="democracia"):
    tokens = tabla["tokens"]
    palabras = [p for p in procesar(mensaje) if p in tokens]
    probs = [tokens[p]["p_spam_dado_palabra"] for p in palabras]
    if not probs:
        etiqueta = "spam" if tabla["p_spam"] > 0.5 else "no_spam"
        return etiqueta, {"palabras": [], "nota": "sin palabras conocidas, se usa P(spam)"}

    media = statistics.mean(probs)
    mediana = statistics.median(probs)
    moda = statistics.mean(statistics.multimode([round(p, 1) for p in probs]))
    votos = {"media": media > 0.5, "mediana": mediana > 0.5, "moda": moda > 0.5}

    if metodo == "democracia":
        es_spam = sum(votos.values()) >= 2
    else:
        es_spam = votos[metodo]
    detalle = {
        "palabras": palabras,
        "media": round(media, 4),
        "mediana": round(mediana, 4),
        "moda": round(moda, 4),
        "votos": {k: ("spam" if v else "no_spam") for k, v in votos.items()},
    }
    return ("spam" if es_spam else "no_spam"), detalle


def clasificar_todos(mensajes, tabla, metodo="democracia"):
    resultados = []
    for m in mensajes:
        etiqueta, detalle = clasificar(m, tabla, metodo)
        resultados.append({"mensaje": m, "etiqueta": etiqueta, "detalle": detalle})
    return resultados


def main(entrada=None, tabla_ruta="tabla_probabilidades.json",
         salida="clasificados.json", metodo="democracia"):
    if metodo not in METODOS:
        raise SystemExit(f"Método inválido. Usa: {', '.join(METODOS)}")
    mensajes = obtener_mensajes(entrada)                                            
    resultados = clasificar_todos(mensajes, cargar(tabla_ruta), metodo)
    for r in resultados:
        print(f"[{r['etiqueta']:8}] {r['mensaje']}")
    guardar(salida, resultados)


if __name__ == "__main__":
    a = sys.argv
    main(a[1] if len(a) > 1 else None,
         a[2] if len(a) > 2 else "tabla_probabilidades.json",
         a[3] if len(a) > 3 else "clasificados.json",
         a[4] if len(a) > 4 else "democracia")
