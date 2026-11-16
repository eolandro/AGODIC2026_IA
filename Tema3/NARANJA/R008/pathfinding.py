import json

TAM = 10

MOVIMIENTOS = [[-1, 0], [1, 0], [0, -1], [0, 1]]

LETRAS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

def leer_archivo(nombre_archivo):
    archivo = open(nombre_archivo, "r")
    datos = json.load(archivo)
    archivo.close()
    return datos

def armar_tablero(datos):
    tablero = []
    for renglon in datos["tablero"]:
        tablero.append(renglon.split())
    return tablero

def buscar_simbolo(tablero, simbolo):
    for fila in range(TAM):
        for col in range(TAM):
            if tablero[fila][col] == simbolo:
                return [fila, col]
    return None

def imprimir_tablero(tablero):
    linea = "     "
    for col in range(TAM):
        linea = linea + " " + LETRAS[col] + " "
    print(linea)
    for fila in range(TAM):
        linea = str(fila + 1).rjust(2) + " | "
        for col in range(TAM):
            linea = linea + " " + tablero[fila][col] + " "
        print(linea)

def texto_posicion(posicion):
    return LETRAS[posicion[1]] + str(posicion[0] + 1)

def distancia_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def casillas_vecinas(tablero, posicion, obstaculo):
    vecinas = []
    for mov in MOVIMIENTOS:
        fila = posicion[0] + mov[0]
        col = posicion[1] + mov[1]
        if fila >= 0 and fila < TAM and col >= 0 and col < TAM:
            if tablero[fila][col] != obstaculo:
                vecinas.append([fila, col])
    return vecinas

def crear_matriz(valor):
    matriz = []
    for fila in range(TAM):
        renglon = []
        for col in range(TAM):
            renglon.append(valor)
        matriz.append(renglon)
    return matriz

def a_estrella(tablero, robot, bomba, obstaculo):
    G = crear_matriz(-1)
    padre = crear_matriz(None)
    cerrada = crear_matriz(False)

    G[robot[0]][robot[1]] = 0
    abiertas = [robot]

    while len(abiertas) > 0:
        mejor = 0
        for i in range(len(abiertas)):
            casilla = abiertas[i]
            F = G[casilla[0]][casilla[1]] + distancia_manhattan(casilla, bomba)
            casilla_mejor = abiertas[mejor]
            F_mejor = G[casilla_mejor[0]][casilla_mejor[1]] + distancia_manhattan(casilla_mejor, bomba)
            if F < F_mejor:
                mejor = i

        actual = abiertas.pop(mejor)

        if actual == bomba:
            return padre

        cerrada[actual[0]][actual[1]] = True

        for vecina in casillas_vecinas(tablero, actual, obstaculo):
            if cerrada[vecina[0]][vecina[1]]:
                continue
            nuevo_G = G[actual[0]][actual[1]] + 1
            if G[vecina[0]][vecina[1]] == -1 or nuevo_G < G[vecina[0]][vecina[1]]:
                G[vecina[0]][vecina[1]] = nuevo_G
                padre[vecina[0]][vecina[1]] = actual
                if vecina not in abiertas:
                    abiertas.append(vecina)

    return None

def reconstruir_camino(padre, robot, bomba):
    camino = []
    actual = bomba
    while actual != robot:
        camino.append(actual)
        actual = padre[actual[0]][actual[1]]
    camino.append(robot)
    camino.reverse()
    return camino

def marcar_camino(tablero, camino, simbolo_camino):
    for casilla in camino[1:-1]:
        tablero[casilla[0]][casilla[1]] = simbolo_camino

def direccion(desde, hasta):
    if hasta[0] < desde[0]:
        return "arriba"
    if hasta[0] > desde[0]:
        return "abajo"
    if hasta[1] < desde[1]:
        return "izquierda"
    return "derecha"

datos = leer_archivo("tablero.json")
simbolos = datos["simbolos"]
tablero = armar_tablero(datos)
robot = buscar_simbolo(tablero, simbolos["robot"])
bomba = buscar_simbolo(tablero, simbolos["bomba"])

print("==============================================")
print("      PATHFINDING A*  BOOME   EQUIPO NARANJA")
print("==============================================")
print("Simbolos:")
print("  " + simbolos["robot"] + " = robot")
print("  " + simbolos["bomba"] + " = bomba")
print("  " + simbolos["obstaculo"] + " = obstaculo")
print("  " + simbolos["libre"] + " = casilla libre")
print("  " + simbolos["camino"] + " = camino")
print()
print("Tablero inicial:")
print()
imprimir_tablero(tablero)
print()
print("Robot en la casilla", texto_posicion(robot))
print("Bomba en la casilla", texto_posicion(bomba))

padre = a_estrella(tablero, robot, bomba, simbolos["obstaculo"])

print("==============================================")
if padre is None:
    print("No hay camino del robot a la bomba")
else:
    camino = reconstruir_camino(padre, robot, bomba)
    marcar_camino(tablero, camino, simbolos["camino"])
    print("Camino final:")
    print()
    imprimir_tablero(tablero)
    print()
    for i in range(1, len(camino)):
        print("Paso " + str(i).rjust(2) + ": " + texto_posicion(camino[i - 1]) + " -> " + texto_posicion(camino[i]) + "   (" + direccion(camino[i - 1], camino[i]) + ")")
    print("==============================================")
    print("Bomba encontrada")
    print("Pasos del robot a la bomba:", len(camino) - 1)
print("==============================================")