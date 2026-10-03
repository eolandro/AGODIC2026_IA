
import json
import sys
from pathlib import Path


def leer_grafo(ruta):
    try:
        with open(ruta, encoding="utf-8") as archivo:
            grafo = json.load(archivo)
    except (OSError, json.JSONDecodeError) as error:
        sys.exit(f"No se pudo leer {ruta}: {error}")

    nodos = grafo["nodos"]
    destinos = [opcion["ir_a"]
                for nodo in nodos.values()
                for opcion in nodo.get("opciones", {}).values()]
    faltantes = sorted(set(destinos + [grafo["inicio"]]) - set(nodos))
    if faltantes:
        sys.exit(f"El grafo apunta a nodos que no existen: {', '.join(faltantes)}")
    return grafo


def leer_opcion(opciones):
    alias = {"si": "s", "sí": "s", "no": "n"}
    while True:
        respuesta = input("Respuesta: ").strip().lower()
        respuesta = alias.get(respuesta, respuesta)
        if respuesta in opciones:
            return respuesta
        print("  Opciones válidas:", ", ".join(opciones))


def clasificar(grafo):
    nodos = grafo["nodos"]
    actual = grafo["inicio"]
    hechos = []

    while "opciones" in nodos[actual]:
        nodo = nodos[actual]
        print(f"\n{nodo['pregunta']}")
        for clave, opcion in nodo["opciones"].items():
            print(f"  [{clave}] {opcion['texto']}")
        elegida = nodo["opciones"][leer_opcion(nodo["opciones"])]
        hechos.append(elegida["hecho"])
        actual = elegida["ir_a"]

    hoja = nodos[actual]
    print(f"\nLa figura es: {hoja['figura'].upper()}")
    print(hoja["descripcion"])
    print("\nHechos acumulados:")
    for numero, hecho in enumerate(hechos, 1):
        print(f"  {numero}. {hecho}")


def main():
    carpeta = Path(__file__).parent
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else carpeta / "grafo.json"
    grafo = leer_grafo(ruta)

    nodos = grafo["nodos"]
    figuras = [nodo["figura"] for nodo in nodos.values() if "figura" in nodo]
    print("=" * 44)
    print(f"  {grafo['titulo']}")
    print("=" * 44)
    print(f"Grafo cargado: {len(nodos)} nodos, {len(figuras)} figuras.")
    print("Piensa en una figura y responde con la clave entre corchetes.")

    otra = "s"
    while otra == "s":
        clasificar(grafo)
        print("\n¿Clasificar otra figura? [s] Sí  [n] No")
        otra = leer_opcion({"s": "", "n": ""})
    print("Fin del programa.")


if __name__ == "__main__":
    main()
