import json
from pathlib import Path

def moverfinal(L):
    F, *R = L
    return R + [F]


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


def anchura(raiz, objetivo):
    cola = [raiz]
    visitados = []
    recorrido = []
    while cola:
        actual = cola[0]
        cola = cola[1:]
        if actual in visitados:
            continue
        visitados.append(actual)
        recorrido.append(actual)
        print("Explorando:", actual)
        if actual == objetivo:
            print("Recorrido:", " -> ".join(recorrido))
            return True
        for hijo in grafo.get(actual, []):
            if hijo not in visitados and hijo not in cola:
                cola.append(hijo)
    print("Recorrido:", " -> ".join(recorrido))
    return False


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
            return True
        for hijo in grafo.get(actual, []):
            if hijo not in visitados:
                pila.append(hijo)
    print("Recorrido:", " -> ".join(recorrido))
    return False



print("Busqueda lista.")
print("Comandos disponibles:")
print('anchura("..", "...")')
print('profundidad("...", "...")')
print("Escribe q para salir.")
while True:
    try:
        command = input("> ")
        if command == "q":
            print("Programa terminado.")
            break
        T = eval(
            command,
            {
                "__builtins__": {},
                "anchura": anchura,
                "profundidad": profundidad,
                "moverfinal": moverfinal
            },
            {}
        )
        print("Resultado:", T)
    except Exception as error:
        print("Error:", error)
        print("Revisa el comando y los nombres de los nodos.")
