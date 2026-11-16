# R005 - Problema de los caballos 1
negros = [[0, 0], [2, 0]]
rojos = [[0, 2], [2, 2]]
recorrido = [[0, 0], [2, 1], [0, 2], [1, 0], [2, 2], [0, 1], [2, 0], [1, 2]]
def siguiente(pos):
    for i in range(8):
        if recorrido[i] == pos:
            if i == 7:
                return recorrido[0]
            return recorrido[i + 1]
def armar_tablero(negros, rojos):
    tablero = [[".", ".", "."],
               [".", ".", "."],
               [".", ".", "."]]
    for p in negros:
        tablero[p[1]][p[0]] = "N"
    for p in rojos:
        tablero[p[1]][p[0]] = "R"
    return tablero
def imprimir_horizontal(tableros, titulos):
    linea = ""
    for t in titulos:
        linea = linea + t.ljust(12)
    print(linea)

    for y in range(3):
        linea = ""
        for i in range(len(tableros)):
            fila = tableros[i][y]
            linea = linea + fila[0] + " " + fila[1] + " " + fila[2] + " "
            if y == 1 and i < len(tableros) - 1:
                linea = linea + " ->   "
            else:
                linea = linea + "      "
        print(linea)

# ---------------- Programa principal ----------------
print("==============================================")
print("     PROBLEMA DE LOS CABALLOS 1  EQUIPO NARANJA")
print("==============================================")
print("N = caballo negro   R = caballo rojo   . = casilla vacia")

tablero = armar_tablero(negros, rojos)
final = armar_tablero(rojos, negros)     

imprimir_horizontal([tablero, final], ["Inicio", "Resultado"])

estados = [tablero]
titulos = ["Estado 0"]

estado = 0
while tablero != final:
    nuevos_negros = []
    for p in negros:
        nuevos_negros.append(siguiente(p))

    nuevos_rojos = []
    for p in rojos:
        nuevos_rojos.append(siguiente(p))

    negros = nuevos_negros
    rojos = nuevos_rojos

    tablero = armar_tablero(negros, rojos)
    estado = estado + 1

    estados.append(tablero)
    titulos.append("Estado " + str(estado))

print("Procedimiento:")
imprimir_horizontal(estados, titulos)

print("==============================================")
print("Intercambio logrado en", estado, "estados")
print("Movimientos de caballos:", estado * 4)
print("==============================================")
