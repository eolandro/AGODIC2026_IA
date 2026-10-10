# r006_entrenador.py

import csv
import os

ARCHIVO_SALIDA = "datos/mensajes_entrenamiento.csv"


def es_spam(respuesta):
    respuesta = respuesta.strip().lower()

    while respuesta not in ["spam", "no spam"]:
        print("Respuesta inválida. Escribe: Spam o No Spam")
        respuesta = input("Clasificación: ").strip().lower()

    return "Spam" if respuesta == "spam" else "No Spam"


def entrenar():
    os.makedirs("datos", exist_ok=True)

    mensajes = []

    print("=== R006: ENTRENADOR ===")
    cantidad = 10

    for i in range(1, cantidad + 1):
        print(f"\nMensaje {i}")
        texto = input("Escribe el mensaje: ")
        clasificacion = es_spam(input("¿Es Spam o No Spam?: "))

        mensajes.append({
            "id": i,
            "mensaje": texto,
            "clase": clasificacion
        })

    with open(ARCHIVO_SALIDA, "w", newline="", encoding="utf-8") as archivo:
        campos = ["id", "mensaje", "clase"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(mensajes)

    print(f"\nArchivo generado correctamente: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    entrenar()
