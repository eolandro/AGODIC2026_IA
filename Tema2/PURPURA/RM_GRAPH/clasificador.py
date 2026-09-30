import json


ARCHIVO_GRAFO = "grafo.json"


def cargar_grafo(archivo):
    """Carga el grafo desde el archivo externo."""
    with open(archivo, "r", encoding="utf-8") as archivo_json:
        return json.load(archivo_json)


def normalizar_respuesta(respuesta):
    """Normaliza la respuesta escrita por el usuario."""

    respuesta = respuesta.strip().lower()

    equivalencias = {
        "sí": "si",
        "s": "si",
        "si": "si",
        "no": "no",
        "n": "no"
    }

    return equivalencias.get(respuesta, respuesta)


def ejecutar_grafo(grafo):
    """Recorre el grafo hasta encontrar un nodo resultado."""

    nodo_actual = grafo["inicio"]

    while True:

        nodo = grafo["nodos"][nodo_actual]

        if nodo["tipo"] == "resultado":
            return nodo["figura"]

        print("\n" + nodo["texto"])

        opciones = nodo["transiciones"]

        print("\nOpciones:")

        for opcion in opciones:
            print(" -", opcion)

        respuesta = input("\nRespuesta: ")

        respuesta = normalizar_respuesta(respuesta)

        if respuesta in opciones:
            nodo_actual = opciones[respuesta]

        else:
            print("\nRespuesta no válida.")
            print("Por favor, selecciona una de las opciones mostradas.")


def main():
    """Función principal."""

    try:

        grafo = cargar_grafo(ARCHIVO_GRAFO)

        figura = ejecutar_grafo(grafo)

        print("\n======================================")
        print("       FIGURA IDENTIFICADA")
        print("======================================")
        print(f"Figura: {figura}")
        print("======================================")

    except FileNotFoundError:
        print("ERROR: No se encontró el archivo grafo.json.")

    except json.JSONDecodeError:
        print("ERROR: El archivo grafo.json tiene un formato incorrecto.")


if __name__ == "__main__":
    main()