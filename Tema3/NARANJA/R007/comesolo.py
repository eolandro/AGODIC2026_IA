FILAS = 5

NOMBRES = ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

tablero = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

LINEAS = [
    [1, 2, 4], [2, 4, 7], [4, 7, 11], [3, 5, 8], [5, 8, 12], [6, 9, 13],
    [1, 3, 6], [3, 6, 10], [6, 10, 15], [2, 5, 9], [5, 9, 14], [4, 8, 13],
    [4, 5, 6], [7, 8, 9], [8, 9, 10], [11, 12, 13], [12, 13, 14], [13, 14, 15]
]

def imprimir_triangulo(textos):
    casilla = 1
    for fila in range(1, FILAS + 1):
        linea = "  " * (FILAS - fila)
        for i in range(fila):
            linea = linea + textos[casilla] + "   "
            casilla = casilla + 1
        print(linea)
        if fila < FILAS:
            linea = " " * (2 * (FILAS - fila) - 1)
            for i in range(fila):
                linea = linea + "/ \\ "
            print(linea)


def imprimir_tablero(tablero):
    textos = [""]
    for casilla in range(1, 16):
        if tablero[casilla] == 1:
            textos.append("O")
        else:
            textos.append(".")
    imprimir_triangulo(textos)

def pedir_casilla():
    while True:
        texto = input("Escribe la casilla que iniciara vacia (1-9 o A-F): ")
        texto = texto.upper()
        for casilla in range(1, 16):
            if NOMBRES[casilla] == texto:
                return casilla
        print("Esa casilla no existe, intenta de nuevo.")

def saltos_posibles(tablero):
    saltos = []
    for linea in LINEAS:
        a = linea[0]
        b = linea[1]
        c = linea[2]
        if tablero[a] == 1 and tablero[b] == 1 and tablero[c] == 0:
            saltos.append([a, b, c])
        if tablero[c] == 1 and tablero[b] == 1 and tablero[a] == 0:
            saltos.append([c, b, a])
    return saltos

def contar_fichas(tablero):
    total = 0
    for casilla in range(1, 16):
        if tablero[casilla] == 1:
            total = total + 1
    return total

def buscar_camino(inicio):
    pila = [[inicio, []]]

    while len(pila) > 0:
        elemento = pila.pop()
        tablero = elemento[0]
        camino = elemento[1]

        if contar_fichas(tablero) == 1:
            return camino

        for salto in saltos_posibles(tablero):
            nuevo = []
            for x in tablero:
                nuevo.append(x)
            nuevo[salto[0]] = 0
            nuevo[salto[1]] = 0
            nuevo[salto[2]] = 1

            nuevo_camino = []
            for s in camino:
                nuevo_camino.append(s)
            nuevo_camino.append(salto)

            pila.append([nuevo, nuevo_camino])

    return None

def imprimir_camino(tablero, camino):
    paso = 1
    for salto in camino:
        tablero[salto[0]] = 0
        tablero[salto[1]] = 0
        tablero[salto[2]] = 1
        print("----------------------------------------------")
        print("Paso " + str(paso) + ": ficha " + NOMBRES[salto[0]] + " salta sobre " + NOMBRES[salto[1]] + " y cae en " + NOMBRES[salto[2]])
        print("----------------------------------------------")
        imprimir_tablero(tablero)
        paso = paso + 1

def ficha_final(tablero):
    for casilla in range(1, 16):
        if tablero[casilla] == 1:
            return casilla
    return -1

print("==============================================")
print("        PROBLEMA DEL COME SOLO  EQUIPO NARANJA")
print("==============================================")
print("O = ficha   . = casilla vacia")
print()
print("Posiciones del tablero:")
print()
imprimir_triangulo(NOMBRES)
print()
vacia = pedir_casilla()
tablero[vacia] = 0
print()
print("Tablero inicial (casilla", NOMBRES[vacia], "vacia):")
print()
imprimir_tablero(tablero)

camino = buscar_camino(tablero)

if camino is None:
    print("No se encontro solucion")
else:
    print("==============================================")
    print("Camino correcto:")
    imprimir_camino(tablero, camino)
    print("==============================================")
    print("Solucion encontrada")
    print("Saltos realizados:", len(camino))
    print("Fichas restantes:", contar_fichas(tablero))
    print("La ultima ficha quedo en la casilla", NOMBRES[ficha_final(tablero)])
    print("==============================================")