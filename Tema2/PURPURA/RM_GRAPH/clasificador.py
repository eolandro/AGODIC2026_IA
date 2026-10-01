import json

ARCHIVO_GRAFO = "grafo.json"

def cargar_grafo(archivo):
    with open(archivo, "r", encoding="utf-8") as archivo_json:
        return json.load(archivo_json)

def normalizar_respuesta(respuesta):
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
    try:
        grafo = cargar_grafo(ARCHIVO_GRAFO)
        print("""
Estas son las figuras disponibles:

  • Círculo
  • Elipse
  • Triángulo equilátero
  • Triángulo rectángulo
  • Triángulo isósceles
  • Triángulo obtusángulo
  • Cuadrado
  • Rombo
  • Trapecio rectángulo
  • Trapecio
  • Rectángulo
  • Romboide
  • Pentágono
  • Hexágono
  • Heptágono
  • Octágono

Elige una figura, yo la adivinaré.
Contesta las siguientes preguntas.
""")
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
