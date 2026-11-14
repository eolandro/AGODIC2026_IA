N = 4  # Tablero de 4x4 con 4 reinas
def crear_tablero():
    """Crea el tablero vacío de N x N."""
    return [["." for _ in range(N)] for _ in range(N)]


def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))
    print()

def es_segura(posiciones, fila, col):
    """Revisa que una reina en (fila, col) no sea atacada por las ya colocadas."""
    for f, c in posiciones:
        if c == col:                      # misma columna
            return False
        if abs(f - fila) == abs(c - col): # misma diagonal
            return False
    return True

def resolver(posiciones, soluciones):
    """Backtracking: coloca una reina por fila. Guarda el recorrido de cada solución."""
    fila = len(posiciones)
    if fila == N:
        soluciones.append(list(posiciones))
        return
    for col in range(N):
        if es_segura(posiciones, fila, col):
            posiciones.append((fila, col))
            resolver(posiciones, soluciones)
            posiciones.pop()  # retroceso (backtracking)

print("Tablero inicial (4x4):")
imprimir_tablero(crear_tablero())

soluciones = []
resolver([], soluciones)

print(f"Soluciones encontradas: {len(soluciones)}\n")
for i, solucion in enumerate(soluciones, start=1):
    print(f"=== Solución {i} ===")
    print("Recorrido:")
    tablero = crear_tablero()
    for paso, (fila, col) in enumerate(solucion, start=1):
        tablero[fila][col] = "Q"
        print(f"Paso {paso}: reina en fila {fila + 1}, columna {col + 1}")
        imprimir_tablero(tablero)