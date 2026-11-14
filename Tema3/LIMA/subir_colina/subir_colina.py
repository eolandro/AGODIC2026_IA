import json

TAM_CACHE = 3     

with open("colina_datos.json", encoding="utf-8") as archivo:
    datos = json.load(archivo)

coordenadas = datos["nodos"]     

grafo = {}
for nodo in coordenadas:
    grafo[nodo] = []
for a, b, peso in datos["caminos"]:
    grafo[a].append([b, peso])
    grafo[b].append([a, peso])

def validar(raiz, buscado):
    if raiz not in grafo:
        print("\nLa raiz", raiz, "no existe en el grafo")
        return False
    if buscado not in grafo:
        print("\nEl nodo buscado", buscado, "no existe en el grafo")
        return False
    return True

def distancia(nodo, meta):
    x1, y1 = coordenadas[nodo]
    x2, y2 = coordenadas[meta]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def subir_colina(raiz, buscado, estrategia, limite):
    if not validar(raiz, buscado):
        return False

    print()
    print("\nSubir la colina, estrategia", estrategia, "de", raiz, "a", buscado,
          "(limite", limite, "pasos)")
    print()
    print("\nPaso".ljust(6) + "Actual".ljust(8) + "Vecinos (peso)".ljust(26)
          + "Elige".ljust(10) + "Cache")
    print("-" * 74)

    actual = raiz
    cache = []
    recorrido = [raiz]
    costo = 0
    paso = 0

    while actual != buscado:
        if paso == limite:
            print("-" * 74)
            print("\nRecorrido:", " -> ".join(recorrido))
            print("\nSe alcanzo el limite de", limite, "pasos sin llegar a", buscado)
            return False
        paso = paso + 1

        opciones = []
        texto = ""
        for vecino, peso in grafo[actual]:
            if vecino in cache:
                texto = texto + vecino + "(" + str(peso) + ")* "
            else:
                texto = texto + vecino + "(" + str(peso) + ") "
                opciones.append([vecino, peso])

        if len(opciones) == 0:
            print(str(paso).ljust(6) + actual.ljust(8) + texto.ljust(26)
                  + "Atorado".ljust(10) + ", ".join(cache))
            print("-" * 74)
            print("\nRecorrido:", " -> ".join(recorrido))
            print("\nTodos los vecinos estan en el cache, el algoritmo se atoro en", actual)
            return False

        mejor = opciones[0]
        for opcion in opciones:
            if estrategia == "corta" and opcion[1] < mejor[1]:
                mejor = opcion
            if estrategia == "larga" and opcion[1] > mejor[1]:
                mejor = opcion

        cache.append(actual)
        descartado = None
        if len(cache) > TAM_CACHE:
            descartado = cache.pop(0)

        print(str(paso).ljust(6) + actual.ljust(8) + texto.ljust(26)
              + (mejor[0] + "(" + str(mejor[1]) + ")").ljust(10) + ", ".join(cache))
        if descartado is not None:
            print("      (", descartado, "sale del cache )")

        actual = mejor[0]
        recorrido.append(actual)
        costo = costo + mejor[1]

    print(str(paso + 1).ljust(6) + actual.ljust(8) + "-".ljust(26)
          + "Llegue".ljust(10) + ", ".join(cache))
    print("-" * 74)
    print("\nRecorrido:", " -> ".join(recorrido))
    print("Costo total:", costo)
    return True

def corta(raiz, buscado, limite=20):
    return subir_colina(raiz, buscado, "corta", limite)

def larga(raiz, buscado, limite=20):
    return subir_colina(raiz, buscado, "larga", limite)

def colina(raiz, buscado):
    if not validar(raiz, buscado):
        return False

    print()
    print("\nSubir la colina con funcion de evaluacion, de", raiz, "a", buscado)
    print("h(n) = distancia en linea recta de n a", buscado, "(subir = que h baje)")
    print()
    print("Paso".ljust(6) + "Actual".ljust(14) + "Vecinos h(n)".ljust(30) + "Elige")
    print("-" * 74)

    actual = raiz
    recorrido = [raiz]
    costo = 0
    paso = 0

    while actual != buscado:
        paso = paso + 1
        h_actual = distancia(actual, buscado)

        mejor = None
        mejor_h = h_actual
        texto = ""
        for vecino, peso in grafo[actual]:
            h = distancia(vecino, buscado)
            texto = texto + vecino + "(" + format(h, ".1f") + ") "
            if h < mejor_h:
                mejor = [vecino, peso]
                mejor_h = h

        columna_actual = actual + " h=" + format(h_actual, ".1f")

        if mejor is None:
            print(str(paso).ljust(6) + columna_actual.ljust(14) + texto.ljust(30) + "Atorado")
            print("-" * 74)
            print("\nRecorrido:", " -> ".join(recorrido))
            print("Ningun vecino esta mas cerca de la meta: optimo local en", actual)
            return False

        print(str(paso).ljust(6) + columna_actual.ljust(14) + texto.ljust(30)
              + mejor[0] + " (h=" + format(mejor_h, ".1f") + ")")
        actual = mejor[0]
        recorrido.append(actual)
        costo = costo + mejor[1]

    print(str(paso + 1).ljust(6) + (actual + " h=0.0").ljust(14) + "-".ljust(30) + "Llegue")
    print("-" * 74)
    print("\nRecorrido:", " -> ".join(recorrido))
    print("\nCosto total:", costo)
    return True

def pedir_nodo(mensaje):
    while True:
        dato = input(mensaje).strip().upper()
        if dato in grafo:
            return dato
        print("  Ese nodo no existe. Nodos validos:", ", ".join(grafo))

def pedir_limite():
    while True:
        dato = input("\nLimite de pasos (Enter para 20): ").strip()
        if dato == "":
            return 20
        if dato.isdigit() and int(dato) > 0:
            return int(dato)
        print("  Escribe un numero entero mayor que 0")

def mostrar_grafo():
    print("\nCaminos (nodo - nodo : peso):")
    for a, b, peso in datos["caminos"]:
        print("  ", a, "-", b, ":", peso)
    print("Nodos:", ", ".join(grafo))

def consola():
    print()
    print("\nModo consola: escribe la funcion con la raiz y el nodo a buscar")
    print('Ejemplos:  corta("A","J")   larga("A","J")   colina("C","J")')
    print('Para cambiar el limite de pasos:  corta("A","J",5)')
    print("Escribe S para volver al menu")

    funciones = {"corta": corta, "larga": larga, "colina": colina}
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
            print("\nError:", error)

def menu():
    print("\n" + "=" * 62)
    print("                 SUBIR LA COLINA")
    print("=" * 62)
    mostrar_grafo()
    while True:
        print()
        print("\n1. Estrategia corta (camino de menor peso)")
        print("2. Estrategia larga (camino de mayor peso)")
        print("3. Con funcion de evaluacion (distancia a la meta)")
        print("4. Ver el grafo")
        print("5. Modo consola (escribir la funcion)")
        print("0. Salir")
        opcion = input("\nOpcion: ").strip()
        if opcion == "1" or opcion == "2":
            raiz = pedir_nodo("\nNodo inicial: ")
            buscado = pedir_nodo("\nNodo a buscar: ")
            limite = pedir_limite()
            if opcion == "1":
                corta(raiz, buscado, limite)
            else:
                larga(raiz, buscado, limite)
        elif opcion == "3":
            raiz = pedir_nodo("\nNodo inicial: ")
            buscado = pedir_nodo("\nNodo a buscar: ")
            colina(raiz, buscado)
        elif opcion == "4":
            mostrar_grafo()
        elif opcion == "5":
            consola()
        elif opcion == "0":
            break
        else:
            print("\nOpcion no valida")

if __name__ == "__main__":
    menu()