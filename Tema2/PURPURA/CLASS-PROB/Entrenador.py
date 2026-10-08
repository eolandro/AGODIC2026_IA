
import json


ARCHIVO_MENSAJES = "mensajes_entrenamiento.txt"
ARCHIVO_CONOCIMIENTO = "conocimiento_entrenamiento.json"

def cargar_mensajes():

    try:
        with open(
            ARCHIVO_MENSAJES,
            "r",
            encoding="utf-8"
        ) as archivo:

            mensajes = [
                linea.strip()
                for linea in archivo
                if linea.strip()
            ]

        if len(mensajes) != 10:
            print()
            print("ERROR:")
            print(
                f"El archivo debe contener exactamente "
                f"10 mensajes."
            )
            print(
                f"Se encontraron {len(mensajes)}."
            )
            return None

        return mensajes

    except FileNotFoundError:
        print()
        print("ERROR:")
        print(
            f"No se encontró el archivo "
            f"'{ARCHIVO_MENSAJES}'."
        )
        return None


def solicitar_clasificacion():

    while True:

        clasificacion = input(
            "Clasificación [S = Spam / N = No Spam]: "
        ).strip().lower()

        if clasificacion == "s":
            return "Spam"

        elif clasificacion == "n":
            return "No Spam"

        else:
            print(
                "Opción no válida. "
                "Escribe S o N."
            )


def guardar_conocimiento(conocimiento):

    try:

        with open(
            ARCHIVO_CONOCIMIENTO,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                conocimiento,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        print()
        print("=" * 60)
        print("       ARCHIVO DE CONOCIMIENTO GENERADO")
        print("=" * 60)
        print()
        print(
            f"Archivo: {ARCHIVO_CONOCIMIENTO}"
        )
        print(
            f"Mensajes guardados: {len(conocimiento)}"
        )

    except Exception as error:

        print()
        print("ERROR al guardar el archivo.")
        print(f"Detalle: {error}")


def entrenar():

    mensajes = cargar_mensajes()

    if mensajes is None:
        return

    conocimiento = []

    print()
    print("=" * 60)
    print("             CLASS_PROB")
    print("             ENTRENADOR")
    print("=" * 60)
    print()
    print(
        f"Se cargaron {len(mensajes)} mensajes "
        f"desde '{ARCHIVO_MENSAJES}'."
    )
    print()

    for i, mensaje in enumerate(mensajes, start=1):

        print("-" * 60)
        print(f"MENSAJE {i} DE 10")
        print("-" * 60)

        print()
        print(f"Mensaje: {mensaje}")
        print()

        clasificacion = solicitar_clasificacion()

        registro = {
            "id": i,
            "mensaje": mensaje,
            "clasificacion": clasificacion
        }

        conocimiento.append(registro)

        print()
        print(
            f"Mensaje registrado como: "
            f"{clasificacion}"
        )
        print()

    guardar_conocimiento(conocimiento)


def main():

    entrenar()


if __name__ == "__main__":
    main()

