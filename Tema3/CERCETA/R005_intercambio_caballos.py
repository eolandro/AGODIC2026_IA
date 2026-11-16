"""R005: intercambiar dos caballos blancos y dos negros en un tablero 6x6.

Se mueve una pieza por turno, sin capturas ni casillas compartidas.
Los caballos del mismo color son equivalentes. No se alternan los colores.
"""

from collections import deque


SALTOS = ((2, 1), (2, -1), (-2, 1), (-2, -1),
          (1, 2), (1, -2), (-1, 2), (-1, -2))


def destinos_caballo(casilla):
    fila, columna = divmod(casilla, 6)
    destinos = []
    for df, dc in SALTOS:
        nueva_fila, nueva_columna = fila + df, columna + dc
        if 0 <= nueva_fila < 6 and 0 <= nueva_columna < 6:
            destinos.append(nueva_fila * 6 + nueva_columna)
    return destinos


def resolver(inicio, meta):
    # Un estado contiene las dos casillas blancas y las dos negras.
    movimientos = [destinos_caballo(c) for c in range(36)]
    pendientes = deque([inicio])
    anterior = {inicio: None}

    while pendientes:
        estado = pendientes.popleft()
        if estado == meta:
            camino = []
            while estado is not None:
                camino.append(estado)
                estado = anterior[estado]
            return camino[::-1]

        ocupadas = estado[0] + estado[1]
        for color in range(2):
            for origen in estado[color]:
                for destino in movimientos[origen]:
                    if destino in ocupadas:
                        continue
                    piezas = list(estado[color])
                    piezas.remove(origen)
                    piezas.append(destino)
                    nuevo = list(estado)
                    nuevo[color] = tuple(sorted(piezas))
                    nuevo = tuple(nuevo)
                    if nuevo not in anterior:
                        anterior[nuevo] = estado
                        pendientes.append(nuevo)
    return None


def mostrar(estado):
    for fila in range(6):
        linea = []
        for columna in range(6):
            casilla = fila * 6 + columna
            simbolo = "."
            if casilla in estado[0]:
                simbolo = "B"
            elif casilla in estado[1]:
                simbolo = "N"
            linea.append(simbolo)
        print(" ".join(linea))


def main():
    inicio = ((0, 5), (30, 35))
    meta = (inicio[1], inicio[0])
    print("INTERCAMBIO DE CABALLOS: B = blanco, N = negro")
    print("Inicio: blancos arriba y negros abajo, en las esquinas.")
    print("Buscando por anchura...")
    camino = resolver(inicio, meta)
    if camino is None:
        print("No se encontro una solucion.")
        return
    for paso, estado in enumerate(camino):
        print(f"\nPaso {paso}:")
        mostrar(estado)
    print(f"\nIntercambio terminado en {len(camino) - 1} movimientos.")


if __name__ == "__main__":
    main()
