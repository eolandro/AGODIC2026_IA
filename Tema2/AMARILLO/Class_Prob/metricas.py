"""
Descripción: Carga archivo de conocimiento y Calcula "Recoll, Accuracy, Presicion ,Prevalence".
Restricciones:
= El supervisor clasifica los 10 nuevos mensaje y se comparan los resultados con "Clasificador"
= Se calcula Recoll, Accuracy, Presicion ,Prevalence.
"""
import sys

from common import cargar, guardar, preguntar_etiqueta


def div(a, b):
    return round(a / b, 4) if b else None


def calcular(predichas, reales):
    vp = sum(p == "spam" and r == "spam" for p, r in zip(predichas, reales))
    fp = sum(p == "spam" and r == "no_spam" for p, r in zip(predichas, reales))
    fn = sum(p == "no_spam" and r == "spam" for p, r in zip(predichas, reales))
    vn = sum(p == "no_spam" and r == "no_spam" for p, r in zip(predichas, reales))
    total = vp + fp + fn + vn
    prec, rec = div(vp, vp + fp), div(vp, vp + fn)
    return {
        "matriz_confusion": {"VP": vp, "FP": fp, "FN": fn, "VN": vn},
        "accuracy": div(vp + vn, total),
        "precision": prec,
        "recall": rec,
        "prevalence": div(vp + fn, total),
        "bias": div(vp + fp, vp + fn),
        "specificity": div(vn, vn + fp),
        "f1": div(2 * prec * rec, prec + rec) if prec and rec else None,
    }


def mostrar(m):
    c = m["matriz_confusion"]
    vp, fp, fn, vn = c["VP"], c["FP"], c["FN"], c["VN"]
    print("\n            Real: spam   Real: no spam")
    print(f"Pred spam   {vp:>9}   {fp:>12}   | {vp + fp}")
    print(f"Pred no     {fn:>9}   {vn:>12}   | {fn + vn}")
    print(f"            {vp + fn:>9}   {fp + vn:>12}   | {vp + fp + fn + vn}\n")
    for k in ("accuracy", "precision", "recall", "prevalence", "bias", "specificity", "f1"):
        v = m[k]
        print(f"{k.capitalize():12}: {'N/A' if v is None else v}")


def main(entrada="clasificados.json", salida="metricas.json", etiq_ruta=None):
    datos = cargar(entrada)
    if etiq_ruta:
        reales = cargar(etiq_ruta)
        if len(reales) != len(datos):
            raise SystemExit(f"Hay {len(reales)} etiquetas y {len(datos)} mensajes.")
    else:                                                  
        reales = [preguntar_etiqueta(d["mensaje"]) for d in datos]
    for d, r in zip(datos, reales):
        d["etiqueta_supervisor"] = r
    m = calcular([d["etiqueta"] for d in datos], reales)
    mostrar(m)
    guardar(salida, {"metricas": m, "mensajes": datos})


if __name__ == "__main__":
    a = sys.argv
    main(a[1] if len(a) > 1 else "clasificados.json",
         a[2] if len(a) > 2 else "metricas.json",
         a[3] if len(a) > 3 else None)
