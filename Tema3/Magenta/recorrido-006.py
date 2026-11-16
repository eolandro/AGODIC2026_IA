N = 8

movimientos = [
    (2, 1), (1, 2),
    (-1, 2), (-2, 1),
    (-2, -1), (-1, -2),
    (1, -2), (2, -1)
]

def dentro(f, c):
    return 0 <= f < N and 0 <= c < N

def imprimir(tablero):
    print("\nRecorrido del caballo:\n")

    for fila in tablero:
        print(" ".join(f"{valor:2d}" for valor in fila))

    print()

def resolver(tablero, f, c, paso):
    if paso == N * N:
        return True

    for df, dc in movimientos:
        nf = f + df
        nc = c + dc

        if dentro(nf, nc) and tablero[nf][nc] == -1:
            tablero[nf][nc] = paso

            if resolver(tablero, nf, nc, paso + 1):
                return True

            # Backtracking
            tablero[nf][nc] = -1

    return False

tablero = [[-1 for _ in range(N)] for _ in range(N)]

tablero[0][0] = 0

if resolver(tablero, 0, 0, 1):
    imprimir(tablero)
    print("El caballo visitó todas las casillas exactamente una vez.")
else:
    print("No se encontró un recorrido completo desde la casilla inicial.")