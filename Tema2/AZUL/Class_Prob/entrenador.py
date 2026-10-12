import json


def leer_mensajes(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        mensajes = [linea.strip() for linea in archivo if linea.strip()]
    if len(mensajes) != 10:
        raise ValueError("El archivo debe contener exactamente 10 mensajes.")
    return mensajes


def pedir_etiqueta(mensaje, numero):
    while True:
        print(f"\nMensaje {numero}: {mensaje}")
        respuesta = input("¿Es spam? [s/n]: ").strip().lower()
        if respuesta in ("s", "n"):
            return "spam" if respuesta == "s" else "no_spam"
        print("Respuesta inválida. Escribe s o n.")


def main():
    mensajes = leer_mensajes("base_supervisada.txt")
    etiquetados = []

    print("ENTRENADOR")
    print("El supervisor clasificará los 10 mensajes.")

    for numero, mensaje in enumerate(mensajes, 1):
        etiquetados.append({
            "id": numero,
            "mensaje": mensaje,
            "etiqueta": pedir_etiqueta(mensaje, numero)
        })

    with open("corpus_etiquetado.json", "w", encoding="utf-8") as archivo:
        json.dump(etiquetados, archivo, ensure_ascii=False, indent=4)

    print("\nArchivo corpus_etiquetado.json generado correctamente.")


if __name__ == "__main__":
    main()
