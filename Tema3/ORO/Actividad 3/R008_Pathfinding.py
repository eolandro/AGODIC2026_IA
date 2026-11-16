import heapq
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")   # para la consola de Windows
except AttributeError:
    pass

LIBRE, MURO, ROBOT, BOMBA, CAMINO = ".", "X", "R", "B", "*"
MOVIMIENTOS = [(-1, 0, "arriba"), (1, 0, "abajo"), (0, -1, "izquierda"), (0, 1, "derecha")]


def leer_tablero(ruta):
    """Lee el tablero desde un JSON y regresa la matriz, el inicio y la meta."""
    with open(ruta, encoding="utf-8") as archivo:
        datos = json.load(archivo)

    filas, columnas = datos["filas"], datos["columnas"]

    def a_indice(par, que):
        r, c = par[0] - 1, par[1] - 1          # el JSON cuenta desde 1
        if not (0 <= r < filas and 0 <= c < columnas):
            raise ValueError(f"{que} {par} está fuera del tablero de {filas}x{columnas}.")
        return r, c

    tablero = [[LIBRE] * columnas for _ in range(filas)]
    for par in datos.get("obstaculos", []):
        r, c = a_indice(par, "El obstáculo")
        tablero[r][c] = MURO

    inicio = a_indice(datos["robot"], "El robot")
    meta = a_indice(datos["bomba"], "La bomba")
    for pos, que in ((inicio, "robot"), (meta, "bomba")):
        if tablero[pos[0]][pos[1]] == MURO:
            raise ValueError(f"El {que} está encima de un obstáculo.")
    tablero[inicio[0]][inicio[1]] = ROBOT
    tablero[meta[0]][meta[1]] = BOMBA
    return tablero, inicio, meta


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def nombre(pos):
    """(fila, columna) -> 'F6C1' contando desde 1, como en el cuaderno."""
    return f"F{pos[0] + 1}C{pos[1] + 1}"


def vecinos(tablero, pos):
    filas, columnas = len(tablero), len(tablero[0])
    for df, dc, _ in MOVIMIENTOS:
        r, c = pos[0] + df, pos[1] + dc
        if 0 <= r < filas and 0 <= c < columnas and tablero[r][c] != MURO:
            yield r, c


def a_estrella(tablero, inicio, meta, mostrar_pasos=True):
    h0 = manhattan(inicio, meta)
    # Elementos de la lista abierta: (f, h, orden, posición)
    # En empate de f se prefiere la de menor h (más cerca de la bomba)
    abierta = [(h0, h0, 0, inicio)]
    g = {inicio: 0}
    padre = {inicio: None}
    cerrada = set()
    orden = 1
    paso = 0

    while abierta:
        f, h, _, actual = heapq.heappop(abierta)
        if actual in cerrada:
            continue                      # entrada vieja con peor g, se ignora
        cerrada.add(actual)
        paso += 1

        if mostrar_pasos:
            print(f"Paso {paso:2d}: expando {nombre(actual)}  "
                  f"g={g[actual]} h={h} f={f}")

        if actual == meta:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            return camino[::-1], paso

        for vecino in vecinos(tablero, actual):
            if vecino in cerrada:
                continue
            nuevo_g = g[actual] + 1       # cada salto cuesta 1
            if nuevo_g < g.get(vecino, float("inf")):
                g[vecino] = nuevo_g
                padre[vecino] = actual
                hv = manhattan(vecino, meta)
                heapq.heappush(abierta, (nuevo_g + hv, hv, orden, vecino))
                orden += 1

        if mostrar_pasos:
            # Solo la entrada vigente de cada casilla (la de su mejor g)
            pendientes = sorted({(fa, ha, p) for fa, ha, _, p in abierta
                                 if p not in cerrada and fa == g[p] + ha})
            print("         abierta: " +
                  ", ".join(f"{nombre(p)}(f={fa})" for fa, ha, p in pendientes))
    return None, paso


def dibujar(tablero, camino=()):
    en_camino = set(camino[1:-1]) if camino else set()
    print("     " + " ".join(f"{c + 1:>2}" for c in range(len(tablero[0]))))
    for r, fila in enumerate(tablero):
        celdas = [f"{CAMINO if (r, c) in en_camino else celda:>2}" for c, celda in enumerate(fila)]
        print(f"  {r + 1:>2} " + " ".join(celdas))


def dibujar_heuristica(tablero, meta):
    print("     " + " ".join(f"{c + 1:>2}" for c in range(len(tablero[0]))))
    for r, fila in enumerate(tablero):
        celdas = [" X" if celda == MURO else f"{manhattan((r, c), meta):>2}"
                  for c, celda in enumerate(fila)]
        print(f"  {r + 1:>2} " + " ".join(celdas))


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "tablero.json")

    try:
        tablero, inicio, meta = leer_tablero(ruta)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"Error al leer el tablero: {error}")
        sys.exit(1)

    print(f"Tablero leído de {ruta}")
    print(f"Robot (R) en {nombre(inicio)}   Bomba (B) en {nombre(meta)}\n")
    dibujar(tablero)

    print("\nHeurística h(n): saltos a la bomba (distancia Manhattan)")
    dibujar_heuristica(tablero, meta)

    print("\nBúsqueda A* (f = g + h):\n")
    camino, expandidos = a_estrella(tablero, inicio, meta)

    if camino is None:
        print("\nNo hay camino: la bomba está encerrada.")
    else:
        print(f"\n¡Bomba encontrada! Casillas expandidas: {expandidos}")
        print(f"Camino ({len(camino) - 1} saltos):")
        print("  " + " -> ".join(nombre(p) for p in camino))
        print("\nRecorrido en el tablero (*):")
        dibujar(tablero, camino)
