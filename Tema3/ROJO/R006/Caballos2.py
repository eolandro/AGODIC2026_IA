N = 8  # tamaño del tablero (8x8 como el ajedrez)

MOVIMIENTOS = [(2, 1), (1, 2), (-1, 2), (-2, 1),
               (-2, -1), (-1, -2), (1, -2), (2, -1)]


def nombre_casilla(f, c):
    """(fila, col) -> notación de ajedrez. (7,0) -> a1"""
    return f"{'abcdefgh'[c]}{N - f}"


def leer_casilla(texto):
    """Notación de ajedrez -> (fila, col). 'a1' -> (7, 0)"""
    texto = texto.strip().lower()
    if len(texto) != 2 or texto[0] not in "abcdefgh"[:N] or not texto[1].isdigit():
        return None
    c = "abcdefgh".index(texto[0])
    f = N - int(texto[1])
    if 0 <= f < N:
        return f, c
    return None


def movimientos_validos(tablero, f, c):
    """Casillas a las que el caballo puede saltar sin repetir."""
    lista = []
    for df, dc in MOVIMIENTOS:
        nf, nc = f + df, c + dc
        if 0 <= nf < N and 0 <= nc < N and tablero[nf][nc] == 0:
            lista.append((nf, nc))
    return lista


def recorrido(tablero, f, c, paso, contador):
    """Coloca el caballo en (f, c) con el número de paso y sigue buscando.
    Regresa True cuando se recorrió todo el tablero."""
    tablero[f][c] = paso
    if paso == N * N:
        return True

    # Warnsdorff: ordenar los siguientes saltos por cuántas salidas tienen
    siguientes = movimientos_validos(tablero, f, c)
    siguientes.sort(key=lambda casilla: len(movimientos_validos(tablero, *casilla)))

    for nf, nc in siguientes:
        if recorrido(tablero, nf, nc, paso + 1, contador):
            return True

    # Ningún movimiento funcionó: se quita el caballo (backtracking)
    tablero[f][c] = 0
    contador["retrocesos"] += 1
    return False


def dibujar(tablero):
    """Dibuja el tablero con el número de paso en que se visitó cada casilla."""
    letras = "".join(f"{l:>4}" for l in "abcdefgh"[:N])
    print("    " + letras)
    print("    +" + "----" * N)
    for f in range(N):
        fila = "".join(f"{tablero[f][c]:>4}" for c in range(N))
        print(f" {N - f}  |{fila}")


def main():
    print("=" * 50)
    print(f"  RECORRIDO DEL CABALLO (tablero {N}x{N})")
    print("=" * 50)

    inicio = None
    while inicio is None:
        texto = input("¿En qué casilla entra el caballo? (ej. a1, e4, etc): ")
        inicio = leer_casilla(texto)
        if inicio is None:
            print("Casilla no válida. Usa una letra a-h y un número 1-8.")

    tablero = [[0] * N for _ in range(N)]
    contador = {"retrocesos": 0}
    exito = recorrido(tablero, inicio[0], inicio[1], 1, contador)

    if not exito:
        print("No se encontró un recorrido desde esa casilla.")
        return

    # Reconstruir el orden de las casillas a partir de los números
    orden = [None] * (N * N)
    for f in range(N):
        for c in range(N):
            orden[tablero[f][c] - 1] = nombre_casilla(f, c)

    print(f"\nEl caballo entra en {orden[0]}.")
    print("\nRecorrido paso a paso:")
    for i in range(1, len(orden)):
        print(f"  Paso {i:2}: {orden[i - 1]} -> {orden[i]}")

    print("\n" + "=" * 50)
    print("  TABLERO RECORRIDO")
    print("=" * 50)
    print("(cada número indica en qué paso visitó el caballo esa casilla)\n")
    dibujar(tablero)
    print(f"\nCasillas visitadas: {N * N} de {N * N}")
    print(f"Retrocesos necesarios: {contador['retrocesos']}")


if __name__ == "__main__":
    main()
