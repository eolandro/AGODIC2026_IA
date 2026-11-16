FILAS = 5

# Se asigna a cada casilla (fila, columna) su número del 1 al 15
NUMERO = {}
POSICION = {}
n = 1
for fila in range(FILAS):
    for col in range(fila + 1):
        NUMERO[(fila, col)] = n
        POSICION[n] = (fila, col)
        n += 1

# Las 6 direcciones en que se puede saltar dentro del triángulo
DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]


def generar_saltos():
    """Genera todos los saltos posibles (origen, comida, destino)."""
    saltos = []
    for (f, c), origen in NUMERO.items():
        for df, dc in DIRECCIONES:
            medio = (f + df, c + dc)
            destino = (f + 2 * df, c + 2 * dc)
            if medio in NUMERO and destino in NUMERO:
                saltos.append((origen, NUMERO[medio], NUMERO[destino]))
    return saltos


SALTOS = generar_saltos()


def dibujar(piezas, resaltar=None):
    """Dibuja el triángulo. ● = pieza, ○ = vacío.
    resaltar = casilla donde cayó la última pieza (se marca con ◉)."""
    for fila in range(FILAS):
        espacio = "  " * (FILAS - fila - 1)
        linea = []
        for col in range(fila + 1):
            num = NUMERO[(fila, col)]
            if num == resaltar:
                linea.append("◉")
            elif num in piezas:
                linea.append("●")
            else:
                linea.append("○")
        print("    " + espacio + "   ".join(linea))


def resolver(piezas, camino, fracasos):
    """Búsqueda en profundidad con backtracking.
    piezas   -> conjunto de casillas con pieza.
    camino   -> lista de saltos hechos hasta ahora.
    fracasos -> estados que ya se sabe que no tienen solución."""
    if len(piezas) == 1:
        return True

    estado = frozenset(piezas)
    if estado in fracasos:
        return False

    for origen, comida, destino in SALTOS:
        if origen in piezas and comida in piezas and destino not in piezas:
            # Hacer el salto
            piezas -= {origen, comida}
            piezas.add(destino)
            camino.append((origen, comida, destino))

            if resolver(piezas, camino, fracasos):
                return True

            # Deshacer el salto (backtracking)
            camino.pop()
            piezas.discard(destino)
            piezas |= {origen, comida}

    fracasos.add(estado)
    return False


def main():
    print("=" * 50)
    print("  COME SOLO (tablero triangular)")
    print("=" * 50)
    print("Numeración de las casillas:\n")
    for fila in range(FILAS):
        espacio = "  " * (FILAS - fila - 1)
        nums = [f"{NUMERO[(fila, c)]:>2}" for c in range(fila + 1)]
        print("   " + espacio + "  ".join(nums))

    vacia = None
    while vacia is None:
        texto = input("\n¿Qué casilla está vacía? (1-15): ").strip()
        if texto.isdigit() and 1 <= int(texto) <= 15:
            vacia = int(texto)
        else:
            print("Escribe un número del 1 al 15.")

    piezas = set(range(1, 16)) - {vacia}
    print("\nTablero inicial (● = pieza, ○ = vacío):")
    dibujar(piezas)

    camino = []
    if not resolver(set(piezas), camino, set()):
        print("\nNo existe solución que deje una sola pieza desde esa casilla.")
        return

    print("\n" + "-" * 50)
    print("  SOLUCIÓN PASO A PASO (◉ = donde cayó la pieza)")
    print("-" * 50)
    for i, (origen, comida, destino) in enumerate(camino, 1):
        piezas -= {origen, comida}
        piezas.add(destino)
        print(f"\nSalto {i}: la pieza en {origen} salta sobre {comida} y cae en {destino}")
        print(f"Quedan {len(piezas)} piezas")
        dibujar(piezas, resaltar=destino)

    print("\n" + "=" * 50)
    print("  RESULTADO")
    print("=" * 50)
    print(f"Se resolvió en {len(camino)} saltos. Queda una sola pieza en la casilla {piezas.pop()}.")
    print("Resumen de saltos:")
    for i, (o, c, d) in enumerate(camino, 1):
        print(f"  {i:2}. {o} -> {d} (come {c})")


if __name__ == "__main__":
    main()
