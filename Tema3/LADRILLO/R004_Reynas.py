paso = 0  
tablero = [-1, -1, -1, -1]  
soluciones = []  


def pos_ajedrez(fila, col):
    letras = ['a', 'b', 'c', 'd']
    return letras[col] + str(fila + 1)


def casillas_bloqueadas(limite_fila):
    bloqueadas = []
    letras = ['a', 'b', 'c', 'd']

    for r_fila in range(limite_fila):
        r_col = tablero[r_fila]
        for f in range(4):
            for c in range(4):
                fila_igual = (f == r_fila)
                col_igual = (c == r_col)
                diag_igual = (abs(f - r_fila) == abs(c - r_col))

                if fila_igual or col_igual or diag_igual:
                    casilla = letras[c] + str(f + 1)
                    if casilla not in bloqueadas:
                        bloqueadas.append(casilla)
    return bloqueadas


def imprimir_tablero(filas_activas=4, margen="    "):
    bloqueadas = casillas_bloqueadas(filas_activas)
    print(margen + "    a   b   c   d")
    print(margen + "  +---+---+---+---+")

    for i in range(4):
        casillas = []
        for c in range(4):
            coord = pos_ajedrez(i, c)
            if tablero[i] == c:
                casillas.append(" R" + str(i + 1))
            elif coord in bloqueadas:
                casillas.append(" x ")
            else:
                casillas.append("   ")

        print(margen + str(i + 1) + " |" + "|".join(casillas) + "|")
        print(margen + "  +---+---+---+---+")


def imprimir_soluciones():
    print("\n" + "=" * 54)
    print("         RESUMEN FINAL: 2 SOLUCIONES ENCONTRADAS")
    print("=" * 54)
    print(f"  Solucion 1: {', '.join(soluciones[0])}      Solucion 2: {', '.join(soluciones[1])}")
    print("      a   b   c   d                a   b   c   d")
    print("    +---+---+---+---+          +---+---+---+---+")

    letras = ['a', 'b', 'c', 'd']
    cols_s1 = [letras.index(pos[0]) for pos in soluciones[0]]
    cols_s2 = [letras.index(pos[0]) for pos in soluciones[1]]

    for f in range(4):
        fila_s1 = [" R" + str(f + 1) if c == cols_s1[f] else "   " for c in range(4)]
        fila_s2 = [" R" + str(f + 1) if c == cols_s2[f] else "   " for c in range(4)]
        print(f"  {f + 1} |{'|'.join(fila_s1)}|        {f + 1} |{'|'.join(fila_s2)}|")
        print("    +---+---+---+---+          +---+---+---+---+")
    print("=" * 54)


def backtracking(fila):
    global paso

    if fila == 4:
        sol_actual = [pos_ajedrez(f, tablero[f]) for f in range(4)]
        soluciones.append(sol_actual)
        print("\n    **********************************************")
        print(f"    *  ¡SOLUCION #{len(soluciones)} ENCONTRADA EN EL PASO {paso}!  *")
        print("    **********************************************")
        imprimir_tablero(4, "        ")
        print("")
        return

    num_fila = str(fila + 1)
    reina = "R" + num_fila
    bloqueadas = casillas_bloqueadas(fila)
    intentos_fallidos = []

    for col in range(4):
        paso += 1
        casilla = pos_ajedrez(fila, col)

        if fila == 0:
            print("\n" + "-" * 54)
            print(f"  RAMA {col + 1}/4: INICIANDO CON R1 EN {casilla.upper()}")
            print("-" * 54)

        if casilla in bloqueadas:
            intentos_fallidos.append(f"{casilla}(x)")
        else:
            if len(intentos_fallidos) > 0:
                print(f"  [Fila {num_fila}] Bloqueadas: {', '.join(intentos_fallidos)}")
                intentos_fallidos = []

            tablero[fila] = col
            print(f"  [Paso {paso:02d}] Fila {num_fila} -> {reina} colocada en {casilla}")
            imprimir_tablero(fila + 1, "    ")

            backtracking(fila + 1)

            tablero[fila] = -1
            print(f"  [Retroceso] Fila {num_fila} -> Se retira {reina} de {casilla}")

    if len(intentos_fallidos) > 0:
        print(f"  [Fila {num_fila}] Sin lugar libre -> {', '.join(intentos_fallidos)}")


print("=" * 54)
print("                        4-REINAS (4x4)            ")
print("    R1..R4 = Reinas  |  x = Abarca  |  ' ' = Libre")
print("=" * 54)

backtracking(0)
imprimir_soluciones()