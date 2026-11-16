import json
import os

carpeta = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(carpeta, "grafo.json"), encoding="utf-8") as f:
    grafo = json.load(f)


def vecinos(nodo):
    lista = []
    for a, b, peso in grafo:
        if a == nodo:
            lista = lista + [[b, peso]]
        if b == nodo:
            lista = lista + [[a, peso]]
    return lista



def sc(raiz, meta, estrategia):
    actual = raiz
    camino = [actual]
    cache = []                            
    total = 0
    pasos = 0
    while pasos < 50:                     
        if actual == meta:                
            return camino, total, True
        cache = cache + [actual]         
        mejor = None
        for nodo, peso in vecinos(actual):
            if nodo not in cache:
                if mejor is None:
                    mejor = [nodo, peso]
                elif estrategia == 'corta' and peso < mejor[1]:
                    mejor = [nodo, peso]
                elif estrategia == 'larga' and peso > mejor[1]:
                    mejor = [nodo, peso]
        if mejor is None:                 # no hay a donde ir
            break
        actual = mejor[0]
        camino = camino + [actual]
        total = total + mejor[1]
        pasos = pasos + 1
    return camino, total, actual == meta


# Nodos que existen en el grafo
nodos = []
for a, b, peso in grafo:
    if a not in nodos:
        nodos = nodos + [a]
    if b not in nodos:
        nodos = nodos + [b]

print("===== SUBIR LA COLINA =====")
print("Lugares disponibles:", ", ".join(nodos))
while True:
    raiz = input("Lugar de inicio (q para salir): ").strip().upper()
    if raiz == 'Q':
        break
    meta = input("Lugar de meta: ").strip().upper()
    estrategia = input("Estrategia (corta/larga): ").strip().lower()
    if raiz not in nodos or meta not in nodos:
        print("Ese lugar no existe en el grafo")
        continue
    if estrategia != 'corta' and estrategia != 'larga':
        print("Estrategia no valida")
        continue
    camino, total, llego = sc(raiz, meta, estrategia)
    print("Recorrido:", " -> ".join(camino))
    print("Costo total:", total)
    if llego:
        print("Llego a la meta", meta)
    else:
        print("No se llego a la meta", meta)
    print()
