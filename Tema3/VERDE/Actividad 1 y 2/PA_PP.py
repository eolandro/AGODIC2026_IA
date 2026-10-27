import json

with open("arbol.json", "r", encoding="utf-8") as f:
    arbol = json.load(f)

def PA(raiz, buscado):
    cola = []
    visitados = {raiz}
    while True:
        print("Raiz:", raiz)
        if raiz == buscado:
            return True
        for hijo in arbol.get(raiz, []):
            if hijo not in visitados:
                visitados.add(hijo)
                cola.append(hijo)
        if not cola:
            return False
        raiz = cola.pop(0)


def PP(raiz, buscado, pila=None):
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
    return PP(nueva_raiz, buscado, pila)

print("Nodos del arbol:", list(arbol.keys()))
print("Ejemplos:  PA('O','OKEN')   PP('O','OKEN')   q = salir")

while True:
    command = input(">")
    if command == "q":
        break
    try:
        T = eval(command)
        print(T)
    except Exception as e:
        print("Error:", e)