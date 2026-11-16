import argparse
import heapq
import json

MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izq, der


def leer_tablero(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


def crear_mapa(datos):
    """Mapa de caracteres: '.' libre, 'X' obstáculo, 'R' robot, 'B' bomba."""
    mapa = [["."] * datos["columnas"] for _ in range(datos["filas"])]
    for fila, columna in datos["obstaculos"]:
        mapa[fila][columna] = "X"
    rf, rc = datos["robot"]
    bf, bc = datos["bomba"]
    mapa[rf][rc] = "R"
    mapa[bf][bc] = "B"
    return mapa


def heuristica(casilla, meta):
    """Distancia Manhattan."""
    return abs(casilla[0] - meta[0]) + abs(casilla[1] - meta[1])


def vecinos(mapa, casilla):
    filas, columnas = len(mapa), len(mapa[0])
    for df, dc in MOVIMIENTOS:
        f, c = casilla[0] + df, casilla[1] + dc
        if 0 <= f < filas and 0 <= c < columnas and mapa[f][c] != "X":
            yield (f, c)


def a_estrella(mapa, inicio, meta):
    """Regresa (camino, casillas_expandidas)."""
    # Cada elemento de la lista abierta: (f, h, contador, casilla)
    # el contador desempata para que heapq no compare tuplas de casillas
    contador = 0
    abierta = [(heuristica(inicio, meta), heuristica(inicio, meta), contador, inicio)]
    g = {inicio: 0}
    padre = {inicio: None}
    cerrada = set()
    paso = 1

    while abierta:
        f_actual, h_actual, _, actual = heapq.heappop(abierta)
        if actual in cerrada:
            continue
        cerrada.add(actual)

        print(f"\nPaso {paso}: se expande {actual} -> g={g[actual]}, h={h_actual}, f={f_actual}")

        if actual == meta:
            print("   ¡Se llegó a la bomba!")
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            return camino[::-1], len(cerrada)

        for vecino in vecinos(mapa, actual):
            if vecino in cerrada:
                continue
            nuevo_g = g[actual] + 1
            if nuevo_g < g.get(vecino, float("inf")):
                g[vecino] = nuevo_g
                padre[vecino] = actual
                h = heuristica(vecino, meta)
                contador += 1
                heapq.heappush(abierta, (nuevo_g + h, h, contador, vecino))
                print(f"   Vecino {vecino}: g={nuevo_g}, h={h}, f={nuevo_g + h}")

        pendientes = sorted({(f, c) for f, _, _, c in abierta if c not in cerrada})
        print(f"   Lista abierta: {[(c, f) for f, c in pendientes]}")
        paso += 1

    return None, len(cerrada)


def imprimir_tablero(mapa, titulo, camino=None):
    print(f"\n================ {titulo} ================")
    print("    " + " ".join(str(c) for c in range(len(mapa[0]))))
    for i, fila in enumerate(mapa):
        celdas = []
        for j, celda in enumerate(fila):
            if camino and (i, j) in camino and celda == ".":
                celdas.append("*")
            else:
                celdas.append(celda)
        print(f" {i}  " + " ".join(celdas))
    print("=" * (34 + len(titulo)))


def imprimir_heuristica(mapa, meta):
    """Tabla con h(n) en cada casilla libre, como en el pizarrón."""
    print("\n======== HEURÍSTICA h(n): saltos para llegar a B ========")
    print("     " + "".join(f"{c:>3}" for c in range(len(mapa[0]))))
    for i, fila in enumerate(mapa):
        celdas = []
        for j, celda in enumerate(fila):
            if celda in ("X", "B", "R"):
                celdas.append(f"{celda:>3}")
            else:
                celdas.append(f"{heuristica((i, j), meta):>3}")
        print(f" {i:>2}  " + "".join(celdas))


def validar(datos):
    filas, columnas = datos["filas"], datos["columnas"]
    obstaculos = {tuple(o) for o in datos["obstaculos"]}
    for nombre in ("robot", "bomba"):
        f, c = datos[nombre]
        if not (0 <= f < filas and 0 <= c < columnas):
            return f"La posición de '{nombre}' está fuera del tablero."
        if (f, c) in obstaculos:
            return f"La posición de '{nombre}' está sobre un obstáculo."
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("Tablero", nargs="?", default="tablero.json")
    args = parser.parse_args()

    datos = leer_tablero(args.Tablero)
    error = validar(datos)
    if error:
        print(error)
        return

    mapa = crear_mapa(datos)
    inicio = tuple(datos["robot"])
    meta = tuple(datos["bomba"])

    print("**************************************************")
    print("              INICIANDO BOOM  -  A*               ")
    print("**************************************************")
    print(f"Robot (R) en {inicio} | Bomba (B) en {meta} | Obstáculos (X): {len(datos['obstaculos'])}")
    imprimir_tablero(mapa, "TABLERO INICIAL")
    imprimir_heuristica(mapa, meta)

    print("\n================ BÚSQUEDA A* ================")
    camino, expandidas = a_estrella(mapa, inicio, meta)

    print("\n=== FIN DE LA BÚSQUEDA ===")
    if camino is None:
        print("El robot no puede llegar a la bomba: está bloqueada por obstáculos.")
        return

    print(f"Camino encontrado ({len(camino) - 1} movimientos):")
    print("  " + " -> ".join(str(c) for c in camino))
    print(f"Casillas expandidas: {expandidas}")
    imprimir_tablero(mapa, "CAMINO DEL ROBOT (*)", set(camino))
    print("Bomba desactivada.")


if __name__ == "__main__":
    main()
