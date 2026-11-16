N = 4

def es_seguro(tablero, fila, col):
    for f in range(fila):
        c = tablero[f]

        # Misma columna
        if c == col:
            return False

        # Misma diagonal
        if abs(c - col) == abs(f - fila):
            return False

    return True

def imprimir_tablero(tablero, titulo):
    print(f"\n{titulo}")

    print("    0  1  2  3")
    print("  +--------------")

    for f in range(N):
        linea = f"{f} |"

        for c in range(N):
            if tablero[f] == c:
                linea += " Q "
            else:
                linea += " . "

        print(linea)

    print()

def imprimir_recorrido(recorrido):
    print("\nRecorrido de colocación de las reinas:")

    for paso, (fila, col) in enumerate(recorrido, 1):
        print(f"Paso {paso}: colocar reina en fila {fila}, columna {col}")

def resolver(tablero, fila, recorrido):
    # Caso base: ya se colocaron todas las reinas
    if fila == N:
        imprimir_tablero(tablero, "SOLUCIÓN FINAL")
        imprimir_recorrido(recorrido)
        return True

    for col in range(N):
        if es_seguro(tablero, fila, col):
            # Colocar reina
            tablero[fila] = col
            recorrido.append((fila, col))

            imprimir_tablero(
                tablero,
                f"Paso {len(recorrido)}: reina colocada en ({fila}, {col})"
            )

            # Intentar colocar la siguiente reina
            if resolver(tablero, fila + 1, recorrido):
                return True

            # Backtracking
            tablero[fila] = -1
            ultima = recorrido.pop()

            imprimir_tablero(
                tablero,
                f"BACKTRACKING: se retira la reina de {ultima}"
            )

    return False

tablero = [-1] * N
recorrido = []

if resolver(tablero, 0, recorrido):
    print("\nEl problema de las 4 reinas fue resuelto correctamente.")
else:
    print("\nNo existe solución.")