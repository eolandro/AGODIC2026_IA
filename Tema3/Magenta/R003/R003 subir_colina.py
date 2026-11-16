import json
from pathlib import Path

def cargar_grafo():
    archivo = Path(__file__).parent / "mapa_colina.json"
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            grafo = json.load(f)
        print("Mapa de colina cargado correctamente.\n")
        return grafo
    except FileNotFoundError:
        print("Error: No se encontró el archivo mapa_colina.json")
        return None
    except json.JSONDecodeError:
        print("Error: El archivo JSON tiene un formato incorrecto.")
        return None

def subir_colina(grafo, inicio, objetivo):
    actual = inicio
    visitados = [actual]
    costo_total = 0

    print(f"\n--- INICIANDO SUBIR LA COLINA (Inicio: {inicio} | Meta: {objetivo}) ---")

    while actual != objetivo:
        vecinos = grafo.get(actual, {})


        opciones = {nodo: costo for nodo, costo in vecinos.items() if nodo not in visitados}

        if not opciones:
            print(f"\nAtascado en '{actual}': No hay caminos nuevos disponibles (Óptimo local).")
            print("Camino recorrido:", " -> ".join(visitados))
            print(f"Costo acumulado: {costo_total}")
            return False

        mejor_vecino = min(opciones, key=opciones.get)
        menor_costo = opciones[mejor_vecino]

        print(f"Desde {actual} evalúa {opciones} -> Elige: {mejor_vecino} (Costo: {menor_costo})")

        # Avanzar al mejor vecino
        actual = mejor_vecino
        visitados.append(actual)
        costo_total += menor_costo

    print(f"\n¡Objetivo '{objetivo}' alcanzado!")
    print("Camino seguido:", " -> ".join(visitados))
    print(f"Costo total del recorrido: {costo_total}")
    return True


if __name__ == "__main__":
    grafo = cargar_grafo()

    if grafo is None:
        exit()

    while True:
        print("\n========== SUBIR LA COLINA (R003) ==========")
        print("1. Buscar ruta")
        print("2. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "2":
            print("Programa finalizado.")
            break

        if opcion != "1":
            print("Opción no válida.")
            continue

        inicio = input("Ingresa el nodo inicial (ej. O): ").strip().upper()
        objetivo = input("Ingresa el nodo objetivo (ej. G): ").strip().upper()

        if inicio not in grafo:
            print(f"Error: El nodo inicial '{inicio}' no existe en el mapa.")
            continue

        if objetivo not in grafo:
            print(f"Error: El nodo objetivo '{objetivo}' no existe en el mapa.")
            continue

        subir_colina(grafo, inicio, objetivo)