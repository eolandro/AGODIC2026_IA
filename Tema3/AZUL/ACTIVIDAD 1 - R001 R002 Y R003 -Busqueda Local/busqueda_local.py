
import json
from pathlib import Path
from collections import deque


# CARGAR GRAFO PARA R001 Y R002

def cargar_grafo():
    ruta = Path(__file__).parent / "gra.json"

    with open(ruta, "r", encoding="utf-8") as archivo:
        conexiones = json.load(archivo)

    grafo = {}

    for padre, hijo in conexiones:
        grafo.setdefault(padre, [])
        grafo.setdefault(hijo, [])
        grafo[padre].append(hijo)

    return grafo


# CARGAR GRAFO PARA R003

def cargar_colina():
    ruta = Path(__file__).parent / "colina.json"

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


# R001: PRIMERO EN PROFUNDIDAD

def primero_profundidad(grafo, inicio, objetivo):
    pila = [inicio]
    visitados = []
    recorrido = []

    print("\n--- PRIMERO EN PROFUNDIDAD ---")

    while pila:
        actual = pila.pop()

        if actual in visitados:
            continue

        visitados.append(actual)
        recorrido.append(actual)

        print("Explorando:", actual)

        if actual == objetivo:
            print("Recorrido:", " -> ".join(recorrido))
            print("Encontrado:", True)
            return True

        for hijo in grafo.get(actual, []):
            if hijo not in visitados:
                pila.append(hijo)

    print("Recorrido:", " -> ".join(recorrido))
    print("Encontrado:", False)
    return False


# R002: PRIMERO EN ANCHURA

def primero_anchura(grafo, inicio, objetivo):
    cola = deque([inicio])
    visitados = []
    recorrido = []

    print("\n--- PRIMERO EN ANCHURA ---")

    while cola:
        actual = cola.popleft()

        if actual in visitados:
            continue

        visitados.append(actual)
        recorrido.append(actual)

        print("Explorando:", actual)

        if actual == objetivo:
            print("Recorrido:", " -> ".join(recorrido))
            print("Encontrado:", True)
            return True

        for hijo in grafo.get(actual, []):
            if hijo not in visitados and hijo not in cola:
                cola.append(hijo)

    print("Recorrido:", " -> ".join(recorrido))
    print("Encontrado:", False)
    return False


# R003: SUBIR LA COLINA

def subir_colina(grafo, inicio, meta, estrategia="corto",
                  tam_cache=3, max_pasos=50):

    cache = deque(maxlen=tam_cache)
    actual = inicio
    camino = [inicio]
    costo_total = 0
    pasos = 0

    print(f"\n--- SUBIR LA COLINA: {estrategia.upper()} ---")
    print(f"Inicio: {inicio} -> Meta: {meta}")

    while actual != meta:

        if pasos >= max_pasos:
            print("Se alcanzo el limite de pasos.")
            return None, costo_total

        candidatos = {
            vecino: peso
            for vecino, peso in grafo.get(actual, {}).items()
            if vecino not in cache
        }

        if not candidatos:
            print("Atorado en:", actual)
            print("Cache:", list(cache))
            return None, costo_total

        if estrategia == "corto":
            siguiente = min(candidatos, key=candidatos.get)
        else:
            siguiente = max(candidatos, key=candidatos.get)

        peso = candidatos[siguiente]

        print(
            f"Paso {pasos + 1}: en {actual}, "
            f"opciones {candidatos} -> voy a {siguiente} "
            f"(costo {peso})"
        )

        cache.append(actual)

        print("Cache:", list(cache))

        costo_total += peso
        actual = siguiente
        camino.append(actual)
        pasos += 1

    print("Camino encontrado:", " -> ".join(camino))
    print("Costo total:", costo_total)

    return camino, costo_total


# FUNCIONES AUXILIARES

def mostrar_arbol(grafo):
    print("\n--- NODOS DISPONIBLES ---")

    for nodo, hijos in grafo.items():
        if hijos:
            print(f"{nodo} -> {', '.join(hijos)}")
        else:
            print(f"{nodo} -> Sin hijos")


def solicitar_nodo(grafo, mensaje):
    nodo = input(mensaje).strip().upper()

    if nodo not in grafo:
        print("Error: el nodo no existe.")
        return None

    return nodo


# MENU PRINCIPAL

def menu():

    while True:

        print("\n========================================")
        print("          BUSQUEDA LOCAL")
        print("========================================")
        print("1. Primero en Profundidad (R001)")
        print("2. Primero en Anchura (R002)")
        print("3. Subir la Colina (R003)")
        print("4. Ejecutar los tres algoritmos")
        print("5. Mostrar arbol R001 y R002")
        print("6. Mostrar grafo R003")
        print("7. Salir")
        print("========================================")

        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            grafo = cargar_grafo()

            inicio = solicitar_nodo(grafo, "Nodo inicial: ")
            objetivo = solicitar_nodo(grafo, "Nodo objetivo: ")

            if inicio is not None and objetivo is not None:
                primero_profundidad(grafo, inicio, objetivo)

        elif opcion == "2":
            grafo = cargar_grafo()

            inicio = solicitar_nodo(grafo, "Nodo inicial: ")
            objetivo = solicitar_nodo(grafo, "Nodo objetivo: ")

            if inicio is not None and objetivo is not None:
                primero_anchura(grafo, inicio, objetivo)

        elif opcion == "3":
            grafo = cargar_colina()

            print("\nNodos disponibles:", ", ".join(grafo.keys()))

            inicio = input("Nodo inicial (Ñ): ").strip().upper() or "Ñ"
            objetivo = input("Nodo meta (A): ").strip().upper() or "A"

            if inicio not in grafo or objetivo not in grafo:
                print("Nodo no valido.")
                continue

            print("\n1. Camino corto")
            print("2. Camino largo")
            print("3. Ambos")

            estrategia = input("Elige estrategia: ").strip() or "3"

            if estrategia in ("1", "3"):
                subir_colina(grafo, inicio, objetivo, "corto")

            if estrategia in ("2", "3"):
                subir_colina(grafo, inicio, objetivo, "largo")

        elif opcion == "4":
            grafo = cargar_grafo()

            inicio = solicitar_nodo(grafo, "Nodo inicial para R001 y R002: ")
            objetivo = solicitar_nodo(grafo, "Nodo objetivo para R001 y R002: ")

            if inicio is not None and objetivo is not None:
                primero_profundidad(grafo, inicio, objetivo)
                primero_anchura(grafo, inicio, objetivo)

                grafo_colina = cargar_colina()

                print("\n--- R003: SUBIR LA COLINA ---")
                print("Inicio: Ñ | Meta: A")

                subir_colina(grafo_colina, "Ñ", "A", "corto")
                subir_colina(grafo_colina, "Ñ", "A", "largo")

        elif opcion == "5":
            mostrar_arbol(cargar_grafo())

        elif opcion == "6":
            mostrar_arbol(cargar_colina())

        elif opcion == "7":
            print("Programa finalizado.")
            break

        else:
            print("Opcion no valida. Intenta nuevamente.")


if __name__ == "__main__":
    menu()
