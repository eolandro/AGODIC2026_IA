import json
from pathlib import Path
from collections import deque

def cargar_grafo():
    archivo = Path(__file__).parent / "mapa.json"
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            grafo = json.load(f)
        print("Mapa cargado correctamente.\n")
        return grafo
    except FileNotFoundError:
        print("Error: No se encontró el archivo mapa.json")
        return None
    except json.JSONDecodeError:
        print("Error: El archivo JSON tiene un formato incorrecto.")
        return None

def PA(grafo, inicio, objetivo):
    cola = deque([inicio])
    visitados = []

    print(f"\n--- INICIANDO BÚSQUEDA PRIMERO EN ANCHURA (Meta: {objetivo}) ---")

    while cola:

        raiz = cola.popleft()

        if raiz not in visitados:
            visitados.append(raiz)
            print(f"Explorando raíz: {raiz:6} | Cola restante: {list(cola)}")

            if raiz == objetivo:
                print(f"\n¡Objetivo '{objetivo}' encontrado!")
                print("Orden de raíces visitadas:", " -> ".join(visitados))
                return True

            hijos = grafo.get(raiz, [])
            for hijo in hijos:
                if hijo not in visitados:
                    cola.append(hijo)

    print(f"\nObjetivo '{objetivo}' no encontrado.")
    print("Orden de raíces visitadas:", " -> ".join(visitados))
    return False

if __name__ == "__main__":
    grafo = cargar_grafo()

    if grafo is None:
        exit()

    while True:
        print("\n========== PRIMERO EN ANCHURA (R002) ==========")1
        print("1. Buscar nodo")
        print("2. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "2":
            print("Programa finalizado.")
            break

        if opcion != "1":
            print("Opción no válida.")
            continue

        inicio = input("Ingresa el nodo inicial (ej. O): ").strip().upper()
        objetivo = input("Ingresa el nodo objetivo (ej. OKEN): ").strip().upper()

        if inicio not in grafo:
            print(f"Error: El nodo inicial '{inicio}' no existe en el mapa.")
            continue

        if objetivo not in grafo:
            print(f"Error: El nodo objetivo '{objetivo}' no existe en el mapa.")
            continue

        PA(grafo, inicio, objetivo)