import json
import os
from collections import deque


def cargar_arbol(nombre_archivo):
    """Lee el archivo JSON (lista de pares [padre, hijo]) y arma un
    diccionario donde cada nodo tiene la lista de sus hijos."""
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        aristas = json.load(f)

    arbol = {}
    for padre, hijo in aristas:
        arbol.setdefault(padre, []).append(hijo)
        arbol.setdefault(hijo, [])  # para que las hojas también existan
    return arbol


def encontrar_raiz(arbol):
    """La raíz es el único nodo que no es hijo de nadie."""
    hijos = {h for lista in arbol.values() for h in lista}
    for nodo in arbol:
        if nodo not in hijos:
            return nodo
    return None


def primero_en_anchura(arbol, inicio, meta):
    """Recorre el árbol con BFS hasta encontrar la meta.
    Regresa (camino, orden_de_visita, nivel_de_cada_nodo)."""
    # Cada elemento de la cola guarda el nodo, el camino y su nivel
    cola = deque([(inicio, [inicio], 0)])
    visitados = {inicio}
    orden_visita = []
    niveles = {}
    paso = 1

    while cola:
        print(f"\nPaso {paso}")
        print(f"  Cola: {[n for n, _, _ in cola]}")

        nodo, camino, nivel = cola.popleft()  # sacamos el del frente
        orden_visita.append(nodo)
        niveles[nodo] = nivel
        print(f"  Visitando: {nodo} (nivel {nivel})")

        if nodo == meta:
            print(f"  ¡Meta '{meta}' encontrada!")
            return camino, orden_visita, niveles

        # Los hijos se forman al FINAL de la cola, en orden normal
        hijos = [h for h in arbol.get(nodo, []) if h not in visitados]
        for hijo in hijos:
            visitados.add(hijo)
            cola.append((hijo, camino + [hijo], nivel + 1))
        if hijos:
            print(f"  Hijos formados al final de la cola: {hijos}")
        else:
            print("  Es una hoja, no tiene hijos.")
        paso += 1

    return None, orden_visita, niveles


def mostrar_arbol(arbol, nodo, nivel=0):
    """Imprime el árbol con sangría para verlo gráficamente."""
    print("    " * nivel + ("└── " if nivel else "") + nodo)
    for hijo in arbol.get(nodo, []):
        mostrar_arbol(arbol, hijo, nivel + 1)


def main():
    arbol = cargar_arbol("arbol.json")
    raiz = encontrar_raiz(arbol)

    print("=" * 50)
    print("  BÚSQUEDA PRIMERO EN ANCHURA (BFS)")
    print("=" * 50)
    print("\nÁrbol cargado desde arbol.json:\n")
    mostrar_arbol(arbol, raiz)

    print(f"\nNodos disponibles: {', '.join(arbol.keys())}")
    meta = input("\n¿Qué nodo quieres buscar? ").strip().upper()

    if meta not in arbol:
        print(f"El nodo '{meta}' no existe en el árbol.")
        return

    camino, orden, niveles = primero_en_anchura(arbol, raiz, meta)

    print("\n" + "=" * 50)
    print("  RESULTADO")
    print("=" * 50)

    # Se muestra el recorrido agrupado por niveles
    print("Recorrido por niveles:")
    for n in range(max(niveles.values()) + 1):
        nodos_nivel = [x for x in orden if niveles[x] == n]
        print(f"  Nivel {n}: {', '.join(nodos_nivel)}")

    print(f"\nOrden en que se visitaron los nodos: {' -> '.join(orden)}")
    print(f"Nodos visitados: {len(orden)}")
    if camino:
        print(f"Camino de '{raiz}' a '{meta}': {' -> '.join(camino)}")
        print(f"Profundidad de la meta: nivel {len(camino) - 1}")
    else:
        print("No se encontró la meta.")


if __name__ == "__main__":
    main()
