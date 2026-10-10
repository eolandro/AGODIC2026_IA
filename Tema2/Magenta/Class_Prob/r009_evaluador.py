# r009_evaluador.py

import csv

ARCHIVO_RESULTADOS = "datos/resultados_clasificacion.csv"


def division_segura(numerador, denominador):
    if denominador == 0:
        return 0

    return numerador / denominador


def evaluar():
    with open(ARCHIVO_RESULTADOS, "r", encoding="utf-8") as archivo:
        resultados = list(csv.DictReader(archivo))

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for registro in resultados:
        real = registro["clase_real"]
        predicha = registro["clase_predicha"]

        if real == "Spam" and predicha == "Spam":
            tp += 1
        elif real == "No Spam" and predicha == "No Spam":
            tn += 1
        elif real == "No Spam" and predicha == "Spam":
            fp += 1
        elif real == "Spam" and predicha == "No Spam":
            fn += 1

    total = tp + tn + fp + fn

    accuracy = division_segura(tp + tn, total)
    precision = division_segura(tp, tp + fp)
    recall = division_segura(tp, tp + fn)
    prevalence = division_segura(tp + fn, total)

    print("=== R009: EVALUADOR ===")
    print("\nMatriz de confusión")
    print("+----------------+--------+----------+")
    print("| Real / Pred.   | Spam   | No Spam  |")
    print("+----------------+--------+----------+")
    print(f"| Spam           | {tp:^6} | {fn:^8} |")
    print(f"| No Spam        | {fp:^6} | {tn:^8} |")
    print("+----------------+--------+----------+")

    print("\nResultados:")
    print(f"TP: {tp}")
    print(f"TN: {tn}")
    print(f"FP: {fp}")
    print(f"FN: {fn}")
    print(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Precision: {precision:.4f} ({precision * 100:.2f}%)")
    print(f"Recall: {recall:.4f} ({recall * 100:.2f}%)")
    print(f"Prevalence: {prevalence:.4f} ({prevalence * 100:.2f}%)")


if __name__ == "__main__":
    evaluar()
