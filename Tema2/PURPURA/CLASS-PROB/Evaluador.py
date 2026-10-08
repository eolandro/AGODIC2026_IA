
import json
ARCHIVO_RESULTADOS = "resultados_clasificador.json"
ARCHIVO_EVALUACION = "evaluacion.json"

def cargar_resultados():
    try:
        with open(
            ARCHIVO_RESULTADOS,
            "r",
            encoding="utf-8"
        ) as archivo:
            datos = json.load(archivo)
        print(
            "Resultados del clasificador "
            "cargados correctamente."
        )
        return datos
    except FileNotFoundError:
        print()
        print("ERROR:")
        print(
            f"No se encontró el archivo "
            f"'{ARCHIVO_RESULTADOS}'."
        )
        print()
        print(
            "Primero debes ejecutar "
            "Clasificador.py."
        )
        return None
    except json.JSONDecodeError:
        print()
        print("ERROR:")
        print(
            "El archivo JSON tiene un formato incorrecto."
        )
        return None

def solicitar_clasificacion():
    while True:
        respuesta = input(
            "Clasificación real "
            "[S = Spam / N = No Spam]: "
        ).strip().lower()
        if respuesta == "s":
            return "Spam"
        elif respuesta == "n":
            return "No Spam"
        else:
            print(
                "Opción no válida."
            )
            print(
                "Escribe S para Spam o N para No Spam."
            )

def obtener_clasificaciones_reales(resultados):
    evaluaciones = []
    print()
    print("=" * 60)
    print("       CLASIFICACIÓN DEL SUPERVISOR")
    print("=" * 60)
    print()
    print(
        "Ahora el supervisor debe indicar "
        "la clasificación REAL de cada mensaje."
    )
    print()
    print(
        "IMPORTANTE: no se modifica la clasificación "
        "realizada por el sistema."
    )
    print()
    for resultado in resultados:
        print("-" * 60)
        print(
            f"MENSAJE {resultado['id']}"
        )
        print()
        print(
            f"Mensaje: "
            f"{resultado['mensaje']}"
        )
        print()
        print(
            f"Clasificación del sistema: "
            f"{resultado['clasificacion']}"
        )
        print()
        clasificacion_real = solicitar_clasificacion()
        evaluaciones.append({
            "id": resultado["id"],
            "mensaje":
                resultado["mensaje"],
            "prediccion":
                resultado["clasificacion"],
            "clasificacion_real":
                clasificacion_real
        })
        print()
    return evaluaciones

def calcular_matriz_confusion(evaluaciones):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for evaluacion in evaluaciones:
        real = evaluacion[
            "clasificacion_real"
        ]
        prediccion = evaluacion[
            "prediccion"
        ]
        if (
            real == "Spam"
            and prediccion == "Spam"
        ):
            TP += 1
        elif (
            real == "No Spam"
            and prediccion == "No Spam"
        ):
            TN += 1
        elif (
            real == "No Spam"
            and prediccion == "Spam"
        ):

            FP += 1
        elif (
            real == "Spam"
            and prediccion == "No Spam"
        ):
            FN += 1

    return TP, TN, FP, FN

def calcular_metricas(
    TP,
    TN,
    FP,
    FN
):
    total = TP + TN + FP + FN

    if total > 0:
        accuracy = ((TP + TN)/ total)
    else:
        accuracy = 0

    if (TP + FP) > 0:
        precision = (TP / (TP + FP))
    else:
        precision = 0

    if (TP + FN) > 0:
        recall = (TP/ (TP + FN))
    else:
        recall = 0
    
    if total > 0:
        prevalence = ((TP + FN) / total)
    else:
        prevalence = 0

    return {
        "Accuracy": round(
            accuracy,
            4
        ),

        "Precision": round(
            precision,
            4
        ),

        "Recall": round(
            recall,
            4
        ),

        "Prevalence": round(
            prevalence,
            4
        )
    }

def mostrar_matriz(TP,TN,FP,FN):

    print()
    print("=" * 60)
    print("             MATRIZ DE CONFUSIÓN")
    print("=" * 60)
    print()
    print(
        "                         REAL"
    )

    print(
        "                  Spam       No Spam"
    )

    print(
        "Predicción Spam    "
        f"{TP:^8}     "
        f"{FP:^8}"
    )

    print(
        "Predicción NoSpam  "
        f"{FN:^8}     "
        f"{TN:^8}"
    )
    print()
    print(f"TP (Verdadero Positivo):  {TP}")
    print(f"TN (Verdadero Negativo):  {TN}")
    print(f"FP (Falso Positivo):      {FP}")
    print(f"FN (Falso Negativo):      {FN}")

def mostrar_metricas(metricas):

    print()
    print("=" * 60)
    print("                 MÉTRICAS")
    print("=" * 60)
    print()
    print(f"Accuracy:    {metricas['Accuracy']:.4f}")
    print(f"Precision:   {metricas['Precision']:.4f}")
    print(f"Recall:      {metricas['Recall']:.4f}")
    print(f"Prevalence:  {metricas['Prevalence']:.4f}")
    print()
    print(
        f"Accuracy:    "
        f"{metricas['Accuracy'] * 100:.2f}%"
    )

    print(
        f"Precision:   "
        f"{metricas['Precision'] * 100:.2f}%"
    )

    print(
        f"Recall:      "
        f"{metricas['Recall'] * 100:.2f}%"
    )

    print(
        f"Prevalence:  "
        f"{metricas['Prevalence'] * 100:.2f}%"
    )

def guardar_evaluacion(evaluaciones,TP,TN,FP,FN,metricas):
    contenido = {

        "descripcion":
            "Evaluación del sistema Class_Prob",

        "matriz_confusion": {

            "TP": TP,
            "TN": TN,
            "FP": FP,
            "FN": FN
        },

        "metricas": metricas,

        "resultados":
            evaluaciones
    }

    try:
        with open(ARCHIVO_EVALUACION,"w",encoding="utf-8") as archivo:
            json.dump(
                contenido,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        print()
        print("=" * 60)
        print("          EVALUACIÓN GUARDADA")
        print("=" * 60)
        print()

        print(
            f"Archivo generado: "
            f"{ARCHIVO_EVALUACION}"
        )

    except Exception as error:

        print()
        print("ERROR al guardar la evaluación.")
        print(f"Detalle: {error}")
def mostrar_comparacion(evaluaciones):

    print()
    print("=" * 60)
    print("             COMPARACIÓN FINAL")
    print("=" * 60)
    print()

    print(
        f"{'ID':<5}"
        f"{'Predicción':<15}"
        f"{'Real':<15}"
        f"{'Resultado':<15}"
    )

    print("-" * 60)

    for evaluacion in evaluaciones:

        prediccion = evaluacion[
            "prediccion"
        ]

        real = evaluacion[
            "clasificacion_real"
        ]

        if prediccion == real:

            resultado = "Correcto"

        else:

            resultado = "Incorrecto"

        print(
            f"{evaluacion['id']:<5}"
            f"{prediccion:<15}"
            f"{real:<15}"
            f"{resultado:<15}"
        )

def main():

    print()
    print("=" * 60)
    print("               CLASS_PROB")
    print("               EVALUADOR")
    print("=" * 60)
    print()
    datos = cargar_resultados()
    if datos is None:
        return
    resultados = datos.get(
        "resultados",
        []
    )
    if len(resultados) != 10:
        print()
        print(
            "ADVERTENCIA:"
        )
        print(
            f"Se esperaban 10 mensajes, "
            f"pero se encontraron {len(resultados)}."
        )
        print()
    evaluaciones = obtener_clasificaciones_reales(resultados)
    (
        TP,
        TN,
        FP,
        FN
    ) = calcular_matriz_confusion(
        evaluaciones
    )
    metricas = calcular_metricas(
        TP,
        TN,
        FP,
        FN
    )
    mostrar_comparacion(
        evaluaciones
    )

    mostrar_matriz(
        TP,
        TN,
        FP,
        FN
    )
    mostrar_metricas(
        metricas
    )
    guardar_evaluacion(
        evaluaciones,
        TP,
        TN,
        FP,
        FN,
        metricas
    )
    print()
    print(
        "Proceso de evaluación terminado."
    )
    print()
if __name__ == "__main__":
    main()
