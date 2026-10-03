"""RM_Graph: la clasificación se define completamente en grafo.json."""
import json
from pathlib import Path


def leer_opcion(opciones):
    """Valida la entrada sin programar las ramas de cada figura."""
    equivalencias = {"si": "s", "sí": "s", "no": "n"}
    respuesta = input("Tu respuesta: ").strip().lower()
    respuesta = equivalencias.get(respuesta, respuesta)
    while respuesta not in opciones and respuesta != "salir":
        print("Elige una de estas claves:", ", ".join(opciones))
        respuesta = input("Tu respuesta: ").strip().lower()
        respuesta = equivalencias.get(respuesta, respuesta)
    return respuesta


def clasificar(grafo):
    nodos = grafo["nodos"]
    actual = grafo["inicio"]
    hechos = []  # Cada respuesta agrega información; no se elimina la anterior.

    while "opciones" in nodos[actual]:
        nodo = nodos[actual]
        print(f"\nPregunta {len(hechos) + 1}: {nodo['pregunta']}")
        for clave, opcion in nodo["opciones"].items():
            print(f"  {clave}. {opcion['texto']}")
        respuesta = leer_opcion(nodo["opciones"])
        if respuesta == "salir":
            return False
        transicion = nodo["opciones"][respuesta]
        hechos.append(transicion["hecho"])
        actual = transicion["destino"]  # Consulta key-value, sin if por figura.

    print(f"\n¡Tu figura es: {nodos[actual]['resultado']}!")
    print(nodos[actual]["descripcion"])
    print("\nRazonamiento seguido:")
    for numero, hecho in enumerate(hechos, 1):
        print(f"  {numero}. {hecho}")
    print(f"Total: {len(hechos)} preguntas.")
    return True


def jugar(grafo):
    repetir = "s"
    while repetir == "s":
        if not clasificar(grafo):
            return
        print("\n¿Otra figura? s = jugar otra vez; n = menú")
        repetir = leer_opcion({"s": "Sí", "n": "No"})


def catalogo(grafo):
    figuras = sorted(nodo["resultado"] for nodo in grafo["nodos"].values()
                     if "resultado" in nodo)
    print("\nFiguras disponibles:")
    for figura in figuras:
        print(" -", figura)


def main():
    ruta = Path(__file__).with_name("grafo.json")
    try:
        with ruta.open(encoding="utf-8") as archivo:
            grafo = json.load(archivo)
    except (OSError, json.JSONDecodeError) as error:
        print("No se pudo leer grafo.json. Colócalo junto al programa.")
        print(error)
        return

    acciones = {
        "1": lambda: jugar(grafo),
        "2": lambda: catalogo(grafo),
        "3": lambda: print("\n" + "\n".join(grafo["instrucciones"])),
    }
    while True:
        print(f"\n{grafo['titulo']}")
        print("1. Jugar\n2. Ver figuras\n3. Cómo jugar\n4. Salir")
        opcion = leer_opcion({"1": "", "2": "", "3": "", "4": ""})
        if opcion in ("4", "salir"):
            print("¡Hasta la próxima!")
            break
        acciones[opcion]()


if __name__ == "__main__":
    main()
