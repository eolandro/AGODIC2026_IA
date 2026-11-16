from collections import deque

N = 6  # tamaño del tablero

# Los 8 movimientos en "L" del caballo
MOVIMIENTOS = [(2, 1), (1, 2), (-1, 2), (-2, 1),
               (-2, -1), (-1, -2), (1, -2), (2, -1)]

INICIO = (frozenset({(0, 0), (0, 5)}), frozenset({(5, 0), (5, 5)}))
META = (frozenset({(5, 0), (5, 5)}), frozenset({(0, 0), (0, 5)}))


def nombre_casilla(casilla):
    """Convierte (fila, col) en notación de ajedrez: (0,0) -> a6."""
    fila, col = casilla
    return f"{'abcdef'[col]}{N - fila}"


def dibujar(estado):
    blancos, negros = estado
    print("     a b c d e f")
    print("    +------------")
    for f in range(N):
        fila = ""
        for c in range(N):
            if (f, c) in blancos:
                fila += "B "
            elif (f, c) in negros:
                fila += "N "
            else:
                fila += ". "
        print(f"  {N - f} | {fila}")


def sucesores(estado):
    """Genera todos los estados a los que se llega con un movimiento.
    Regresa tuplas (nuevo_estado, descripción_del_movimiento)."""
    blancos, negros = estado
    ocupadas = blancos | negros
    resultado = []
    for color, grupo, otro in (("Blanco", blancos, negros), ("Negro", negros, blancos)):
        for (f, c) in grupo:
            for df, dc in MOVIMIENTOS:
                nf, nc = f + df, c + dc
                if 0 <= nf < N and 0 <= nc < N and (nf, nc) not in ocupadas:
                    nuevo_grupo = (grupo - {(f, c)}) | {(nf, nc)}
                    if color == "Blanco":
                        nuevo = (nuevo_grupo, otro)
                    else:
                        nuevo = (otro, nuevo_grupo)
                    desc = f"Caballo {color}: {nombre_casilla((f, c))} -> {nombre_casilla((nf, nc))}"
                    resultado.append((nuevo, desc))
    return resultado


def bfs(inicio, meta):
    """Búsqueda Primero en Anchura. Regresa la lista de movimientos y el
    número de estados explorados."""
    cola = deque([inicio])
    padre = {inicio: None}   # padre[estado] = (estado_anterior, movimiento)
    explorados = 0

    while cola:
        estado = cola.popleft()
        explorados += 1
        if estado == meta:
            # Reconstruir el camino de la meta hacia atrás
            camino = []
            while padre[estado] is not None:
                anterior, mov = padre[estado]
                camino.append((mov, estado))
                estado = anterior
            camino.reverse()
            return camino, explorados

        for nuevo, mov in sucesores(estado):
            if nuevo not in padre:
                padre[nuevo] = (estado, mov)
                cola.append(nuevo)

    return None, explorados


def main():
    print("=" * 50)
    print("  PROBLEMA DE LOS CABALLOS 1 (tablero 6x6)")
    print("=" * 50)
    print("B = caballo blanco, N = caballo negro\n")
    print("Estado inicial:")
    dibujar(INICIO)
    print("\nEstado meta (los caballos intercambian lugares):")
    dibujar(META)

    print("\nBuscando solución con BFS (puede tardar unos segundos)...")
    camino, explorados = bfs(INICIO, META)

    if camino is None:
        print("No se encontró solución.")
        return

    print(f"Solución encontrada. Estados explorados: {explorados}")
    for i, (mov, estado) in enumerate(camino, 1):
        print(f"\nMovimiento {i}: {mov}")
        dibujar(estado)

    print("\n" + "=" * 50)
    print("  RESULTADO")
    print("=" * 50)
    print(f"Los caballos intercambiaron lugares en {len(camino)} movimientos:")
    for i, (mov, _) in enumerate(camino, 1):
        print(f"  {i:2}. {mov}")


if __name__ == "__main__":
    main()
