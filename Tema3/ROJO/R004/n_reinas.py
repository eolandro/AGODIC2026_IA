N = 4  # número de reinas (tablero de 4x4)


def es_segura(estado, fila, columna):
    """Revisa si una reina en (fila, columna) no es atacada por las
    reinas ya colocadas en las filas anteriores."""
    for f in range(fila):
        c = estado[f]
        if c == columna:                          # misma columna
            return False
        if abs(c - columna) == abs(f - fila):     # misma diagonal
            return False
    return True


def dibujar_tablero(estado, n):
    """Dibuja el tablero. Q = reina, . = casilla vacía."""
    print("    " + " ".join(str(c) for c in range(n)))
    print("   +" + "--" * n)
    for f in range(n):
        fila = ""
        for c in range(n):
            fila += "Q " if f < len(estado) and estado[f] == c else ". "
        print(f" {f} | {fila}")


def resolver(n, mostrar_pasos, todas):
    """Busca soluciones con backtracking.
    mostrar_pasos -> imprime cada intento de colocar una reina.
    todas         -> si es False, se detiene en la primera solución."""
    soluciones = []
    contador = {"pasos": 0, "retrocesos": 0}

    def colocar(estado, fila):
        if fila == n:                     # se colocaron todas las reinas
            soluciones.append(estado[:])
            if mostrar_pasos:
                print(f"\n  *** ¡Solución {len(soluciones)} encontrada! ***")
                if todas:
                    print("  Se sigue buscando más soluciones...")
            return not todas              # True = detener la búsqueda

        for columna in range(n):
            contador["pasos"] += 1
            if es_segura(estado, fila, columna):
                estado.append(columna)
                if mostrar_pasos:
                    print(f"\nPaso {contador['pasos']}: reina en fila {fila}, columna {columna} -> OK")
                    dibujar_tablero(estado, n)
                if colocar(estado, fila + 1):
                    return True
                estado.pop()              # se quita la reina (retroceso)
                contador["retrocesos"] += 1
                if mostrar_pasos:
                    print(f"  Retroceso: se quita la reina de la fila {fila}")
            elif mostrar_pasos:
                print(f"Paso {contador['pasos']}: fila {fila}, columna {columna} -> atacada")
        return False

    colocar([], 0)
    return soluciones, contador


def main():
    n = N
    print("=" * 50)
    print(f"  PROBLEMA DE LAS {n} REINAS")
    print("=" * 50)
    print(f"Tablero de {n}x{n}. Se coloca una reina por fila.")
    soluciones, cont = resolver(n, mostrar_pasos=True, todas=True)

    print("\n" + "=" * 50)
    print("  RESULTADO")
    print("=" * 50)
    if soluciones:
        print(f"Se encontraron {len(soluciones)} soluciones para {n} reinas.")
        for i, sol in enumerate(soluciones, 1):
            print(f"\nSolución {i}:")
            posiciones = ", ".join(f"(fila {f}, col {c})" for f, c in enumerate(sol))
            print(f"  Reinas en: {posiciones}")
            dibujar_tablero(sol, n)
    else:
        print(f"No existe solución para {n} reinas.")
    print(f"\nIntentos: {cont['pasos']} | Retrocesos: {cont['retrocesos']}")


if __name__ == "__main__":
    main()
