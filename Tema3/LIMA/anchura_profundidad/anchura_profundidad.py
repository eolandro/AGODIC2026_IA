import json
from collections import deque

with open("arbol_busqueda.json", encoding="utf-8") as archivo:
    relaciones = json.load(archivo)

arbol = {}
for padre, hijo in relaciones:
    if padre not in arbol:
        arbol[padre] = []
    if hijo not in arbol:
        arbol[hijo] = []
    arbol[padre].append(hijo)

def reconstruir_camino(padres, nodo):
    camino = []
    while nodo is not None:
        camino.append(nodo)
        nodo = padres[nodo]
    camino.reverse()
    return camino

def validar(raiz, buscado):
    if raiz not in arbol:
        print("\nLa raiz", raiz, "no existe en el arbol")
        return False
    if buscado not in arbol:
        print("\nEl nodo buscado", buscado, "no existe en el arbol")
        return False
    return True

def imprimir_encabezado(estructura):
    print()
    print("Paso".ljust(6) + "Nodo".ljust(8) + "Hijos agregados".ljust(20) + estructura)
    print("-" * 70)

def imprimir_resultado(recorrido, padres, nodo_final, encontrado):
    print("-" * 70)
    print("\nRecorrido:", " -> ".join(recorrido))
    if encontrado:
        print("\nCamino de la raiz al nodo:", " -> ".join(reconstruir_camino(padres, nodo_final)))
    else:
        print("\nEl nodo buscado no esta en el arbol")

def profundidad(raiz, buscado):
    if not validar(raiz, buscado):
        return False
    imprimir_encabezado("Pila")

    pila = [raiz]
    padres = {raiz: None}
    visitados = set()         
    recorrido = []
    paso = 0

    while len(pila) > 0:
        nodo = pila.pop()
        if nodo in visitados:
            continue
        visitados.add(nodo)
        recorrido.append(nodo)
        paso = paso + 1

        if nodo == buscado:
            print(str(paso).ljust(6) + nodo.ljust(8) + "Encontrado!")
            imprimir_resultado(recorrido, padres, nodo, True)
            return True

        hijos = arbol[nodo]

        for hijo in reversed(hijos):
            if hijo not in visitados:
                pila.append(hijo)
                padres[hijo] = nodo

        print(str(paso).ljust(6) + nodo.ljust(8) + str(hijos).ljust(20) + str(pila))

    imprimir_resultado(recorrido, padres, None, False)
    return False

def anchura(raiz, buscado):
    if not validar(raiz, buscado):
        return False
    imprimir_encabezado("Cola")

    cola = deque([raiz])
    padres = {raiz: None}   
    recorrido = []
    paso = 0

    while len(cola) > 0:
        nodo = cola.popleft()
        recorrido.append(nodo)
        paso = paso + 1

        if nodo == buscado:
            print(str(paso).ljust(6) + nodo.ljust(8) + "Encontrado!")
            imprimir_resultado(recorrido, padres, nodo, True)
            return True

        hijos = arbol[nodo]
        for hijo in hijos:
            if hijo not in padres:    
                cola.append(hijo)
                padres[hijo] = nodo

        print(str(paso).ljust(6) + nodo.ljust(8) + str(hijos).ljust(20) + str(list(cola)))

    imprimir_resultado(recorrido, padres, None, False)
    return False

def pedir_nodo(mensaje):
    while True:
        dato = input(mensaje).strip().upper()
        if dato in arbol:
            return dato
        print("  Ese nodo no existe. Nodos validos:", ", ".join(arbol))

def mostrar_arbol():
    print("\nArbol (padre -> hijos):")
    for nodo in arbol:
        if len(arbol[nodo]) > 0:
            print("  ", nodo, "->", ", ".join(arbol[nodo]))
    print("Nodos:", ", ".join(arbol))

def consola():
    print()
    print("\nModo consola: escribe la funcion con la raiz y el nodo a buscar")
    print('Ejemplo:  profundidad("A","O")   o   anchura("A","O")')
    print("\nEscribe S para volver al menu")

    funciones = {"profundidad": profundidad, "anchura": anchura}
    while True:
        comando = input(">").strip()
        if comando == "":
            continue
        if comando.upper() == "S":
            break
        try:
            resultado = eval(comando, {"__builtins__": {}}, funciones)
            print(resultado)
        except Exception as error:
            print("Error:", error)

def menu():
    print("\n","=" * 62)
    print("   BUSQUEDA LOCAL: PRIMERO EN PROFUNDIDAD Y EN ANCHURA")
    print("=" * 62)
    mostrar_arbol()
    while True:
        print()
        print("\n1. Primero en profundidad (R001)")
        print("2. Primero en anchura (R002)")
        print("3. Ver el arbol")
        print("4. Modo consola (escribir la funcion)")
        print("0. Salir")
        opcion = input("\nOpcion: ").strip()
        if opcion == "1":
            raiz = pedir_nodo("\nNodo inicial: ")
            buscado = pedir_nodo("\nNodo a buscar: ")
            profundidad(raiz, buscado)
        elif opcion == "2":
            raiz = pedir_nodo("\nNodo inicial: ")
            buscado = pedir_nodo("\nNodo a buscar: ")
            anchura(raiz, buscado)
        elif opcion == "3":
            mostrar_arbol()
        elif opcion == "4":
            consola()
        elif opcion == "0":
            break
        else:
            print("\nOpción no válida")

if __name__ == "__main__":
    menu()