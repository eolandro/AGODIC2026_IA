import json
from pathlib import Path
def cargar_grafo():
    ruta = Path(__file__).parent / "gra.json"
    with open(ruta, "r", encoding="utf-8") as archivo:
        conexiones = json.load(archivo)
    grafo = {}
    for padre, hijo in conexiones:
        if padre not in grafo:
            grafo[padre] = []
        if hijo not in grafo:
            grafo[hijo] = []
        grafo[padre].append(hijo)
    return grafo
grafo = cargar_grafo()
# Primero en Profundidad: utiliza una pila
def profundidad(raiz, objetivo):
    pila = [raiz]
    visitados = []
    recorrido = []
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
print("Busqueda local lista.")
print('Ejemplo ---> profundidad("...", "...")')
print("Escribe q para salir.")

while True:
    try:
        command = input(">")
        if command=='q':
            print("Programa terminado.")
            break
        T=eval(command)
        #print("Resultado:", T)
    except Exception as error:
        print("Error:", error)
        print("Revisa el comando y los nombres de los nodos.")

