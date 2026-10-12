import json


def pedir_etiqueta(mensaje, numero):
    while True:
        print(f"\nMensaje {numero}: {mensaje}")
        respuesta = input("Clasificación real del supervisor [s=spam/n=no spam]: ").strip().lower()
        if respuesta in ("s", "n"):
            return "spam" if respuesta == "s" else "no_spam"
        print("Respuesta inválida. Escribe s o n.")


def division(numerador, denominador):
    return numerador / denominador if denominador else 0.0


def main():
    with open("predicciones_spam.json", "r", encoding="utf-8") as archivo:
        mensajes = json.load(archivo)

    if len(mensajes) != 10:
        raise ValueError("Se requieren exactamente 10 mensajes clasificados.")

    vp = fp = fn = vn = 0
    comparacion = []

    print("MÉTRICAS Y MATRIZ DE CONFUSIÓN")
    print("El supervisor clasificará los 10 mensajes nuevos.")

    for numero, item in enumerate(mensajes, 1):
        real = pedir_etiqueta(item["mensaje"], numero)
        predicha = item["clasificacion"]

        if real == "spam" and predicha == "spam":
            vp += 1
        elif real == "no_spam" and predicha == "spam":
            fp += 1
        elif real == "spam" and predicha == "no_spam":
            fn += 1
        else:
            vn += 1

        comparacion.append({
            "id": numero,
            "supervisor": real,
            "clasificador": predicha,
            "acierto": real == predicha
        })

    total = vp + fp + fn + vn
    recall = division(vp, vp + fn)
    accuracy = division(vp + vn, total)
    precision = division(vp, vp + fp)
    prevalence = division(vp + fn, total)
    error = division(fp + fn, total)
    f1 = division(2 * precision * recall, precision + recall)
    proporcion_predicha_spam = division(vp + fp, total)
    bias = proporcion_predicha_spam - prevalence

    resultado = {
        "matriz_confusion": {
            "verdaderos_positivos": vp,
            "falsos_positivos": fp,
            "falsos_negativos": fn,
            "verdaderos_negativos": vn
        },
        "metricas": {
            "recall": round(recall, 4),
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "prevalence": round(prevalence, 4),
            "tasa_error": round(error, 4),
            "f1_score": round(f1, 4),
            "bias_prediccion": round(bias, 4)
        },
        "comparacion": comparacion
    }

    with open("evaluacion_clasificador.json", "w", encoding="utf-8") as archivo:
        json.dump(resultado, archivo, ensure_ascii=False, indent=4)

    print("\nMatriz de confusión")
    print(f"VP: {vp} | FP: {fp} | FN: {fn} | VN: {vn}")
    print(f"Recall: {recall:.2%}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Prevalence: {prevalence:.2%}")
    print(f"Tasa de error: {error:.2%}")
    print(f"F1-score: {f1:.2%}")
    print(f"Bias de predicción: {bias:.2%}")
    print("Archivo evaluacion_clasificador.json generado correctamente.")


if __name__ == "__main__":
    main()
