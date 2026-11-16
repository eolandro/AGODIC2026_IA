import json
import os

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


def primero_en_profundidad(arbol, inicio, meta):
    """Recorre el árbol con DFS hasta encontrar la meta.
    Regresa (camino, orden_de_visita)."""
    # Cada elemento de la pila guarda el nodo y el camino para llegar a él
    pila = [(inicio, [inicio])]
    visitados = set()
    orden_visita = []
    paso = 1

    while pila:
        print(f"\nPaso {paso}")
        print(f"  Pila: {[n for n, _ in pila]}")

        nodo, camino = pila.pop()  # sacamos el de arriba (el último)

        if nodo in visitados:
            continue
        visitados.add(nodo)
        orden_visita.append(nodo)
        print(f"  Visitando: {nodo}")

        if nodo == meta:
            print(f"  ¡Meta '{meta}' encontrada!")
            return camino, orden_visita

        # Se meten los hijos en orden inverso para que el primero de la
        # lista (el de más a la izquierda) sea el que se explore primero
        hijos = arbol.get(nodo, [])
        for hijo in reversed(hijos):
            if hijo not in visitados:
                pila.append((hijo, camino + [hijo]))
        if hijos:
            print(f"  Hijos agregados a la pila: {hijos}")
        else:
            print("  Es una hoja, no tiene hijos. Se regresa (backtracking).")
        paso += 1

    return None, orden_visita


def mostrar_arbol(arbol, nodo, nivel=0):
    """Imprime el árbol con sangría para verlo gráficamente."""
    print("    " * nivel + ("└── " if nivel else "") + nodo)
    for hijo in arbol.get(nodo, []):
        mostrar_arbol(arbol, hijo, nivel + 1)


def main():
    arbol = cargar_arbol("arbol.json")
    raiz = encontrar_raiz(arbol)

    print("=" * 50)
    print("  BÚSQUEDA PRIMERO EN PROFUNDIDAD (DFS)")
    print("=" * 50)
    print("\nÁrbol cargado desde arbol.json:\n")
    mostrar_arbol(arbol, raiz)

    print(f"\nNodos disponibles: {', '.join(arbol.keys())}")
    meta = input("\n¿Qué nodo quieres buscar? ").strip().upper()

    if meta not in arbol:
        print(f"El nodo '{meta}' no existe en el árbol.")
        return

    camino, orden = primero_en_profundidad(arbol, raiz, meta)

    print("\n" + "=" * 50)
    print("  RESULTADO")
    print("=" * 50)
    print(f"Orden en que se visitaron los nodos: {' -> '.join(orden)}")
    print(f"Nodos visitados: {len(orden)}")
    if camino:
        print(f"Camino de '{raiz}' a '{meta}': {' -> '.join(camino)}")
    else:
        print("No se encontró la meta.")


if __name__ == "__main__":
    main()
