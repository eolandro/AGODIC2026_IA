N = 4  # número de reinas y tamaño del tablero (N x N)

def posición_valida(posiciones, fila, columna):
    for f, c in enumerate(posiciones):
        misma_columna = (c == columna)
        misma_diagonal = abs(c - columna) == abs(f - fila)
        if misma_columna or misma_diagonal:
            return False
    return True

def resolver(posiciones, soluciones):
    fila = len(posiciones)
    if fila == N:
        soluciones.append(posiciones[:])
        return
    for columna in range(N):
        if posición_valida(posiciones, fila, columna):
            posiciones.append(columna)
            resolver(posiciones, soluciones)
            posiciones.pop()

def casilla_atacada(posiciones, fila, columna):
    for f, c in enumerate(posiciones):
        if f == fila or c == columna or abs(f - fila) == abs(c - columna):
            return True
    return False

def imprimir_tablero(posiciones):
    reinas = {(f, c): f"R{f + 1}" for f, c in enumerate(posiciones)}
    linea = "+" + "----+" * N
    print(linea)
    for f in range(N):
        celdas = []
        for c in range(N):
            if (f, c) in reinas:
                celdas.append(reinas[(f, c)])
            elif casilla_atacada(posiciones, f, c):
                celdas.append("X")
            else:
                celdas.append(" ")
        print("| " + " | ".join(f"{x:<2}" for x in celdas) + " |")
        print(linea)

# ---------------- MAIN ----------------
soluciones = []
resolver([], soluciones)
print(f"* * * PROBLEMA DE LAS {N} REINAS * * *")
print(f"Soluciones encontradas: {len(soluciones)}\n")

for i, solución in enumerate(soluciones, start=1):
    print(f"Solución {i}:")
    ubicación_reinas = ", ".join(f"R{f + 1}=({f + 1},{c + 1})" for f, c in enumerate(solución))
    print(ubicación_reinas)
    imprimir_tablero(solución)
    print()