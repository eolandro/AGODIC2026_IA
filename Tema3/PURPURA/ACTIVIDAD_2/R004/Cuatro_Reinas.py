N = 4  # tamaño del tablero y número de reinas

REINA = "♛"
BLOQUEADA = "✗"
LIBRE = " "


def tablero_vacio():
    return [[LIBRE for _ in range(N)] for _ in range(N)]


def bloquear(tablero, f, c):
    for i in range(N):
        for j in range(N):
            ataca = (i == f) or (j == c) or abs(i - f) == abs(j - c)
            if ataca and tablero[i][j] == LIBRE:
                tablero[i][j] = BLOQUEADA
    tablero[f][c] = REINA


def dibujar(tablero, sangria="    "):
    borde_sup = "┌" + "───┬" * (N - 1) + "───┐"
    separador = "├" + "───┼" * (N - 1) + "───┤"
    borde_inf = "└" + "───┴" * (N - 1) + "───┘"

    print(sangria + borde_sup)
    for i, fila in enumerate(tablero):
        print(sangria + "│" + "│".join(f" {x} " for x in fila) + "│")
        print(sangria + (separador if i < N - 1 else borde_inf))


def casillas_libres(tablero, desde):
    return [p for p in range(desde, N * N) if tablero[p // N][p % N] == LIBRE]


def main():
    soluciones = []

    print("=" * 50)
    print(f"  PROBLEMA DE LAS {N} REINAS - RECORRIDO COMPLETO")
    print("=" * 50)

    # Solo la reina 1 se mueve por todo el tablero
    for pos1 in range(N * N):
        f1, c1 = divmod(pos1, N)
        print(f"\n{'━' * 50}")
        print(f" INTENTO {pos1 + 1}: Reina 1 en fila {f1 + 1}, columna {c1 + 1}")
        print(f"{'━' * 50}")

        tablero = tablero_vacio()
        bloquear(tablero, f1, c1)
        reinas = [(f1, c1)]
        print("\n  Reina 1 colocada:")
        dibujar(tablero)

        ultima = pos1
        completo = True

        for n in range(2, N + 1):
            libres = casillas_libres(tablero, ultima + 1)
            if not libres:
                print(f"\n  Reina {n}: no hay casillas libres ✗ -> SE DESCARTA, "
                      f"la reina 1 avanza una casilla")
                completo = False
                break

            pos = libres[0]
            f, c = divmod(pos, N)
            bloquear(tablero, f, c)
            reinas.append((f, c))
            ultima = pos
            print(f"\n  Reina {n} colocada en fila {f + 1}, columna {c + 1}:")
            dibujar(tablero)

        if completo:
            print(f"\n  ★★★ ¡SOLUCIÓN ENCONTRADA! ★★★")
            soluciones.append(reinas)

    # Resumen
    print("\n" + "=" * 50)
    print(f"  RESUMEN: {len(soluciones)} soluciones encontradas")
    print("=" * 50)
    for k, reinas in enumerate(soluciones, 1):
        print(f"\n  Solución {k}: " +
              ", ".join(f"R{i + 1}({f + 1},{c + 1})" for i, (f, c) in enumerate(reinas)))
        limpio = [[LIBRE for _ in range(N)] for _ in range(N)]
        for f, c in reinas:
            limpio[f][c] = REINA
        dibujar(limpio)


if __name__ == "__main__":
    main()
