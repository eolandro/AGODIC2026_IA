import json
import sys

ENTRADA = "mensajes_clasificados.json"
SUPERVISOR = "etiquetas_supervisor.json"
EVALUACION = "evaluacion.json"


def preguntar(numero, mensaje):
    respuestas = {"s": "spam", "si": "spam", "sí": "spam", "n": "no_spam", "no": "no_spam"}
    print(f"\n{numero}. \"{mensaje}\"")
    respuesta = input("   ¿Es spam? (s/n): ").strip().lower()
    while respuesta not in respuestas:
        respuesta = input("   Escribe s o n: ").strip().lower()
    return respuestas[respuesta]


def dividir(a, b):
    return a / b if b else None


def mostrar(nombre, formula, a, b, valor):
    texto = "N/A (división entre 0)" if valor is None else f"{valor:.4f}  ({valor:.0%})"
    print(f"{nombre:11}= {formula:22}= {a}/{b} = {texto}")


def matriz(predichas, reales):
    celdas = {(p, r): 0 for p in ("spam", "no_spam") for r in ("spam", "no_spam")}
    for p, r in zip(predichas, reales):
        celdas[(p, r)] += 1
    return (celdas[("spam", "spam")], celdas[("spam", "no_spam")],
            celdas[("no_spam", "spam")], celdas[("no_spam", "no_spam")])


def main():
    print("* * * MÉTRICAS * * *")
    try:
        with open(ENTRADA, encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        sys.exit(f"No se encontró '{ENTRADA}'. Ejecuta primero Clasificador.py")
    registros = datos["mensajes"]

    if "--reusar" in sys.argv:
        with open(SUPERVISOR, encoding="utf-8") as archivo:
            reales = json.load(archivo)
    else:
        print("El supervisor clasifica los mensajes nuevos:")
        reales = [preguntar(i, r["mensaje"]) for i, r in enumerate(registros, 1)]
        with open(SUPERVISOR, "w", encoding="utf-8") as archivo:
            json.dump(reales, archivo, ensure_ascii=False, indent=2)

    predichas = [r["etiqueta"] for r in registros]
    vp, fp, fn, vn = matriz(predichas, reales)
    total = vp + fp + fn + vn

    print("\nComparación (supervisor vs clasificador):")
    for i, (r, p) in enumerate(zip(registros, predichas), 1):
        marca = "ok " if p == reales[i - 1] else "ERR"
        print(f"  {marca} {i:>2}. real={reales[i - 1]:8} clasif={p:8} {r['mensaje'][:45]}")

    print(f"\nMATRIZ DE CONFUSIÓN (método: {datos['metodo']})")
    print(f"{'':24}{'Real spam':>11}{'Real no spam':>14}")
    print(f"{'Clasificó spam':24}{vp:>11}{fp:>14}    (VP, FP)")
    print(f"{'Clasificó no spam':24}{fn:>11}{vn:>14}    (FN, VN)")

    print("\nMÉTRICAS")
    mostrar("Accuracy", "(VP+VN)/total", vp + vn, total, dividir(vp + vn, total))
    mostrar("Precision", "VP/(VP+FP)", vp, vp + fp, dividir(vp, vp + fp))
    mostrar("Recall", "VP/(VP+FN)", vp, vp + fn, dividir(vp, vp + fn))
    mostrar("Prevalence", "(VP+FN)/total", vp + fn, total, dividir(vp + fn, total))
    mostrar("Bias", "(VP+FP)/(VP+FN)", vp + fp, vp + fn, dividir(vp + fp, vp + fn))

    evaluacion = {
        "metodo": datos["metodo"],
        "matriz_confusion": {"VP": vp, "FP": fp, "FN": fn, "VN": vn},
        "metricas": {
            "accuracy": dividir(vp + vn, total),
            "precision": dividir(vp, vp + fp),
            "recall": dividir(vp, vp + fn),
            "prevalence": dividir(vp + fn, total),
            "bias": dividir(vp + fp, vp + fn),
        },
        "resultados": [{"mensaje": r["mensaje"], "clasificador": p, "supervisor": real}
                       for r, p, real in zip(registros, predichas, reales)],
    }
    with open(EVALUACION, "w", encoding="utf-8") as archivo:
        json.dump(evaluacion, archivo, ensure_ascii=False, indent=2)

    print("\nComparación de métodos de consenso:")
    print(f"{'Método':12}{'Accuracy':>10}{'Precision':>11}{'Recall':>8}")
    for metodo in registros[0]["metodos"]:
        a, b, c, d = matriz([r["metodos"][metodo] for r in registros], reales)
        valores = [dividir(a + d, a + b + c + d), dividir(a, a + b), dividir(a, a + c)]
        celdas = "".join(f"{('N/A' if v is None else f'{v:.0%}'):>{w}}"
                         for v, w in zip(valores, (10, 11, 8)))
        print(f"{metodo:12}{celdas}")


if __name__ == "__main__":
    main()
    print(f"\nArchivo '{EVALUACION}' generado.")
