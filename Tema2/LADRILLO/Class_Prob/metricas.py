import json

def ejecutar_metricas():
    print("\n ********************* METRICAS ***********************")

    archivo = open("msg1_sistema.json", "r", encoding="utf-8")
    predicciones = json.load(archivo)
    archivo.close()

    realidad = []
    print("\n Supervisor, clasifique los mensajes nuevos (Spam = 1, No Spam = 0)")
    for msg in predicciones:
        print("\nMensaje", msg["id"], ":", msg["msg1"])
        etiqueta = input("¿Es Spam (1) o No Spam (0)?: ")

        realidad.append({
            "id": msg["id"],
            "msg1": msg["msg1"],
            "es_noes": int(etiqueta)
        })

    archivo_guardar = open("msg1_realidad.json", "w", encoding="utf-8")
    json.dump(realidad, archivo_guardar, ensure_ascii=False, indent=4)
    archivo_guardar.close()

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for i in range(len(predicciones)):
        pred = predicciones[i]["es_noes"]
        real = realidad[i]["es_noes"]

        if pred == 1 and real == 1:
            tp = tp + 1
        elif pred == 0 and real == 0:
            tn = tn + 1
        elif pred == 1 and real == 0:
            fp = fp + 1
        else:
            fn = fn + 1

    total = tp + tn + fp + fn

    exactitud = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    if (precision + recall) > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0.0
        
    prevalencia = (tp + fn) / total if total > 0 else 0.0

    print("\n Matriz de confusión")
    print("                  Real Spam   Real No Spam")
    print("Predicho Spam    ", tp, "(TP)    ", fp, "(FP)")
    print("Predicho No Spam ", fn, "(FN)    ", tn, "(TN)")
    
    print("\n Exactitud (accuracy): {:.2f}\n Precisión: {:.2f}\n Recall (sensibilidad): {:.2f}\n F1-score: {:.2f}\n Prevalencia: {:.2f}".format(exactitud, precision, recall, f1, prevalencia))

    metricas = {
        "TP": tp, "TN": tn, "FP": fp, "FN": fn,
        "exactitud": round(exactitud, 2),
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1": round(f1, 2),
        "prevalencia": round(prevalencia, 2)
    }
    archivo_metricas = open("metricas.json", "w", encoding="utf-8")
    json.dump(metricas, archivo_metricas, ensure_ascii=False, indent=4)
    archivo_metricas.close()

    print("\n ¡Listo! Se generaron 'msg1_realidad.json' y 'metricas.json' con éxito")

if __name__ == "__main__":
    ejecutar_metricas()