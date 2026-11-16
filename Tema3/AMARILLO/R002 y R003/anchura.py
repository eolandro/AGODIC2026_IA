import json
import os

carpeta = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(carpeta, "rel.json")) as f:
    rel = json.load(f)


def hijos(nodo):
    lista = []
    for padre, hijo in rel:
        if padre == nodo:
            lista = lista + [hijo]
    return lista


def pa(raiz, meta):
    cola = [[raiz]]                    
    visitados = []
    while len(cola) > 0:
        camino = cola.pop(0)        
        raiz = camino[-1]             
        visitados = visitados + [raiz]
        if raiz == meta:              
            return visitados, camino
        for h in hijos(raiz):          
            cola = cola + [camino + [h]]
    return visitados, None          


nodos = []
for padre, hijo in rel:
    if padre not in nodos:
        nodos = nodos + [padre]
    if hijo not in nodos:
        nodos = nodos + [hijo]

print("===== PRIMERO EN ANCHURA =====")
while True:
    raiz = input("Ingresa la raiz (q para salir): ").strip().upper()
    if raiz == 'Q':
        break
    meta = input("Ingresa el objetivo: ").strip().upper()
    if raiz not in nodos:
        print("Esa raiz no existe en el arbol")
        continue
    recorrido, camino = pa(raiz, meta)
    print("Recorrido:", " -> ".join(recorrido))
    if camino is None:
        print("El objetivo no existe en el arbol")
    else:
        print("Camino solucion:", " -> ".join(camino))
    print("Nodos visitados:", len(recorrido))
    print()
