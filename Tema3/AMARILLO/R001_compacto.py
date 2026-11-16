import json

with open("arbol.json", "r", encoding="utf-8") as f:
    arbol = json.load(f)


def primero_anchura(raiz, buscado):
    cola = []
    while True:
        print("Raiz:", raiz)
        if raiz == buscado:
            return True
        for hijo in arbol.get(raiz, []):
            cola.append(hijo)
        if not cola:
            return False
        raiz = cola.pop(0)


def primero_profundidad(raiz, buscado, pila=None):
    if pila is None:
        pila = []
    print("Raiz:", raiz)
    if raiz == buscado:
        return True
    for hijo in arbol.get(raiz, []):
        pila.append(hijo)
    if not pila:
        return False
    nueva_raiz = pila.pop()
    return primero_profundidad(nueva_raiz, buscado, pila)


def altura(nodo, buscado):
    n = 0
    while n < len(nodo) and n < len(buscado) and nodo[n] == buscado[n]:
        n = n + 1
    return n


def subir_colina(raiz, buscado):
    while True:
        print("Raiz:", raiz, "| altura:", altura(raiz, buscado))
        if raiz == buscado:
            return True
        mejor = None
        for hijo in arbol.get(raiz, []):
            if altura(hijo, buscado) > altura(raiz, buscado):
                if mejor is None or altura(hijo, buscado) > altura(mejor, buscado):
                    mejor = hijo
        if mejor is None:
            return False
        raiz = mejor


print("Funciones: primero_anchura(raiz, buscado)  primero_profundidad(raiz, buscado)  subir_colina(raiz, buscado)")
print("Escribe q para salir")

while True:
    comando = input(">>> ")
    if comando == "q":
        break
    try:
        resultado = eval(comando)
        print(resultado)
    except Exception as e:
        print("Error:", e)
