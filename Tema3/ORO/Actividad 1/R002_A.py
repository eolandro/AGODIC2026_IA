import json
import os
import sys
from collections import deque

try:
    sys.stdout.reconfigure(encoding="utf-8")   # para la consola de Windows
except AttributeError:
    pass


def cargar_arbol(ruta):
    """Lee los pares [padre, hijo] y regresa {nodo: [hijos]} y la raíz."""
    with open(ruta, encoding="utf-8") as archivo:
        relaciones = json.load(archivo)

    arbol = {}
    hijos_de_alguien = set()
    for par in relaciones:
        padre, hijo = str(par[0]), str(par[1])
        arbol.setdefault(padre, []).append(hijo)   # se respeta el orden del archivo
        arbol.setdefault(hijo, [])
        hijos_de_alguien.add(hijo)

    # La raíz es el nodo que no es hijo de nadie
    raices = [n for n in arbol if n not in hijos_de_alguien]
    return arbol, (raices[0] if raices else next(iter(arbol)))


def dibujar_arbol(arbol, nodo, nivel=0):
    print("    " + "   " * nivel + ("└─ " if nivel else "") + nodo)
    for hijo in arbol[nodo]:
        dibujar_arbol(arbol, hijo, nivel + 1)


def primero_anchura(arbol, inicio, meta):
    cola = deque([[inicio]])   # cada elemento es un camino completo
    visitados = []
    paso = 0

    print(f"\nBuscando {meta} desde {inicio} con Primero en Anchura\n")
    while cola:
        paso += 1
        print(f"Paso {paso:2d} | Cola: {['-'.join(c) for c in cola]}")
        camino = cola.popleft()  # FIFO: sale el primero que entró
        nodo = camino[-1]
        visitados.append(nodo)
        print(f"        | Expando {nodo} (nivel {len(camino) - 1})")

        if nodo == meta:
            return camino, visitados

        for hijo in arbol[nodo]:
            cola.append(camino + [hijo])
    return None, visitados


def pedir_nodo(arbol, mensaje, por_defecto):
    por_nombre = {n.lower(): n for n in arbol}
    while True:
        valor = input(f"{mensaje} [{por_defecto}]: ").strip()
        if not valor:
            return por_defecto
        if valor.lower() in por_nombre:
            return por_nombre[valor.lower()]
        print(f"  Nodo no válido. Opciones: {', '.join(arbol)}")


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "arbol.json")
    try:
        arbol, raiz = cargar_arbol(ruta)
    except (OSError, ValueError, IndexError, TypeError) as error:
        print(f"Error al leer {ruta}: {error}")
        sys.exit(1)

    print(f"Árbol leído de {ruta} ({len(arbol)} nodos):")
    dibujar_arbol(arbol, raiz)

    hojas = [n for n in arbol if not arbol[n]]
    inicio = pedir_nodo(arbol, "\nNodo inicial", raiz)
    meta = pedir_nodo(arbol, "Nodo a buscar", hojas[-1])

    camino, visitados = primero_anchura(arbol, inicio, meta)
    print(f"\nOrden de visita: {' -> '.join(visitados)}")
    print(f"Nodos visitados: {len(visitados)}")
    if camino:
        print(f"Camino encontrado: {' -> '.join(camino)}")
        print(f"Saltos: {len(camino) - 1}")
    else:
        print(f"{meta} no está debajo de {inicio} en el árbol.")
