# R006 - Problema de los caballos 1
# . = casilla vacía

borde = [(0, 0), (1, 2), (2, 0), (0, 1), (2, 2), (1, 0), (0, 2), (2, 1)]

tablero = [["N", ".", "N"],
           [".", ".", "."],
           ["B", ".", "B"]]


def mostrar(tablero):
    for fila in tablero:
        print("  ".join(fila))
    print()

def mover(tablero, paso):
    nuevo = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    for i in range(len(borde)):
        fila, col = borde[i]
        if tablero[fila][col] != ".":
            nueva_fila, nueva_col = borde[(i + paso) % len(borde)]
            nuevo[nueva_fila][nueva_col] = tablero[fila][col]
    return nuevo


def resuelto(tablero):
    arriba = tablero[0][0] == "B" and tablero[0][2] == "B"
    abajo = tablero[2][0] == "N" and tablero[2][2] == "N"
    return arriba and abajo


print("PROBLEMA DE LOS CABALLOS 1")
print("N = caballo negro, B = caballo blanco\n")
print("Estado inicial")
mostrar(tablero)

print("¿En qué dirección quieres mover los caballos?")
print("1. En el sentido de las manecillas del reloj")
print("2. En contra de las manecillas del reloj")
opcion = input("Opción: ")
while opcion != "1" and opcion != "2":
    opcion = input("Opción no válida, escribe 1 o 2: ")
print()

if opcion == "1":
    paso = 1
else:
    paso = -1

estado = 0
while not resuelto(tablero):
    tablero = mover(tablero, paso)
    estado = estado + 1
    if resuelto(tablero):
        print("Estado final")
    else:
        print("Estado", estado)
    mostrar(tablero)
