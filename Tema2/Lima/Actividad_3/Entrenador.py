import json
import sys

ENTRADA = sys.argv[1] if len(sys.argv) > 1 else "mensajes_entrenamiento.txt"
SALIDA = sys.argv[2] if len(sys.argv) > 2 else "entrenamiento_etiquetado.json"
NUM_MENSAJES = 10


def leer_mensajes(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]


def preguntar_supervisor(numero, mensaje):
    respuestas = {"s": "spam", "si": "spam", "sí": "spam", "n": "no_spam", "no": "no_spam"}
    print(f"\n{numero}. \"{mensaje}\"")
    respuesta = input("   ¿Es spam? (s/n): ").strip().lower()
    while respuesta not in respuestas:
        respuesta = input("   Escribe s o n: ").strip().lower()
    return respuestas[respuesta]


def main():
    print("* * * ENTRENADOR (supervisor) * * *")
    try:
        mensajes = leer_mensajes(ENTRADA)
    except FileNotFoundError:
        sys.exit(f"No se encontró '{ENTRADA}'.")
    if len(mensajes) != NUM_MENSAJES:
        print(f"Aviso: se esperaban {NUM_MENSAJES} mensajes y hay {len(mensajes)}.")

    registros = [{"mensaje": m, "etiqueta": preguntar_supervisor(i, m)}
                 for i, m in enumerate(mensajes, 1)]

    with open(SALIDA, "w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2)

    spam = sum(r["etiqueta"] == "spam" for r in registros)
    print(f"\nSpam: {spam} | No spam: {len(registros) - spam} | Total: {len(registros)}")
    print(f"Archivo '{SALIDA}' generado.")


if __name__ == "__main__":
    main()
