"""R008: buscar una bomba con A*, leyendo el tablero desde un archivo."""

import heapq
from pathlib import Path


def validar_tablero(tablero):
    if not tablero or not tablero[0]:
        raise ValueError("El tablero esta vacio.")

    ancho = len(tablero[0])
    inicios = []
    bombas = []
    for fila in range(len(tablero)):
        if len(tablero[fila]) != ancho:
            raise ValueError("Todas las filas deben tener el mismo largo.")
        for columna in range(ancho):
            simbolo = tablero[fila][columna]
            if simbolo not in "IB#.":
                raise ValueError("Solo se permiten I, B, # y . en el tablero.")
            if simbolo == "I":
                inicios.append((fila, columna))
            elif simbolo == "B":
                bombas.append((fila, columna))

    if len(inicios) != 1 or len(bombas) != 1:
        raise ValueError("Debe haber exactamente un inicio I y una bomba B.")
    return inicios[0], bombas[0]


def leer_tablero(archivo):
    tablero = Path(archivo).read_text(encoding="utf-8").splitlines()
    inicio, bomba = validar_tablero(tablero)
    return tablero, inicio, bomba


def distancia(casilla, meta):
    # Distancia de Manhattan: filas y columnas que faltan por recorrer.
    return abs(casilla[0] - meta[0]) + abs(casilla[1] - meta[1])


def a_estrella(tablero, inicio, meta):
    pendientes = [(distancia(inicio, meta), 0, inicio)]
    costo = {inicio: 0}
    anterior = {inicio: None}

    while pendientes:
        prioridad, pasos, actual = heapq.heappop(pendientes)
        if pasos != costo[actual]:
            continue

        if actual == meta:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = anterior[actual]
            return camino[::-1]

        fila, columna = actual
        for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            f, c = fila + df, columna + dc
            if not (0 <= f < len(tablero) and 0 <= c < len(tablero[0])):
                continue
            if tablero[f][c] == "#":
                continue

            vecino = (f, c)
            nuevo_costo = pasos + 1
            if vecino not in costo or nuevo_costo < costo[vecino]:
                costo[vecino] = nuevo_costo
                anterior[vecino] = actual
                prioridad = nuevo_costo + distancia(vecino, meta)
                heapq.heappush(pendientes, (prioridad, nuevo_costo, vecino))
    return None


def main():
    print("BUSQUEDA DE UNA BOMBA CON A*")
    print("I = inicio, B = bomba, # = pared, . = libre, * = camino")
    archivo = Path(__file__).with_name("tablero.txt")
    try:
        tablero, inicio, bomba = leer_tablero(archivo)
    except (OSError, UnicodeError, ValueError) as error:
        print("No se pudo leer el tablero:", error)
        return

    camino = a_estrella(tablero, inicio, bomba)
    if camino is None:
        for fila in tablero:
            print(fila)
        print("No hay un camino hasta la bomba.")
        return

    dibujo = [list(fila) for fila in tablero]
    for fila, columna in camino[1:-1]:
        dibujo[fila][columna] = "*"
    for fila in dibujo:
        print("".join(fila))
    print("Bomba encontrada en", len(camino) - 1, "pasos.")


if __name__ == "__main__":
    main()
