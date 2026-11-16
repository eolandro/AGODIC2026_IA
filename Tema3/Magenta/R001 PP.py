import json
from pathlib import Path

# ==========================================
# CARGAR EL GRAFO DESDE UN ARCHIVO JSON
# ==========================================
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

# ==========================================
# R001: PRIMERO EN PROFUNDIDAD (P.P. / DFS)
# ==========================================
def PP(grafo, inicio, objetivo):
    # Usamos una Pila (LIFO: el último que entra es el primero que sale)
    pila = [inicio]
    visitados = []

    print(f"\n--- INICIANDO BÚSQUEDA PRIMERO EN PROFUNDIDAD (Meta: {objetivo}) ---")

    while pila:
        # 1. Extraer un elemento de la pila y convertirlo en raíz
        raiz = pila.pop()

        if raiz not in visitados:
            visitados.append(raiz)
            print(f"Explorando raíz: {raiz:6} | Pila restante: {pila}")

            # 2. Revisar si la raíz es el elemento buscado
            if raiz == objetivo:
                print(f"\n¡Objetivo '{objetivo}' encontrado!")
                print("Orden de raíces visitadas:", " -> ".join(visitados))
                return True

            # 3. Listar sus hijos y agregarlos a la pila (en orden normal, tal como en el pizarrón)
            hijos = grafo.get(raiz, [])
            for hijo in hijos:
                if hijo not in visitados:
                    pila.append(hijo)

    print(f"\nObjetivo '{objetivo}' no encontrado.")
    print("Orden de raíces visitadas:", " -> ".join(visitados))
    return False

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================
if __name__ == "__main__":
    grafo = cargar_grafo()

    if grafo is None:
        exit()

    while True:
        print("\n========== PRIMERO EN PROFUNDIDAD (R001) ==========")
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

        PP(grafo, inicio, objetivo)l