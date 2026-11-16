"""R006: recorrer las 64 casillas de un tablero 8x8 sin repetir."""


SALTOS = ((2, 1), (1, 2), (-1, 2), (-2, 1),
          (-2, -1), (-1, -2), (1, -2), (2, -1))


def disponibles(tablero, fila, columna):
    opciones = []
    for df, dc in SALTOS:
        f, c = fila + df, columna + dc
        if 0 <= f < 8 and 0 <= c < 8 and tablero[f][c] == 0:
            opciones.append((f, c))
    return opciones


def recorrer(tablero, fila, columna, paso):
    tablero[fila][columna] = paso
    if paso == 64:
        return True

    # Primero se intenta la casilla que tiene menos salidas libres.
    opciones = []
    for f, c in disponibles(tablero, fila, columna):
        salidas = len(disponibles(tablero, f, c))
        opciones.append((salidas, f, c))
    opciones.sort()

    for salidas, f, c in opciones:
        if recorrer(tablero, f, c, paso + 1):
            return True

    # Si no se puede continuar, se regresa para probar otra opcion.
    tablero[fila][columna] = 0
    return False


def main():
    print("RECORRIDO DEL CABALLO EN TABLERO 8x8")
    tablero = [[0] * 8 for _ in range(8)]
    if recorrer(tablero, 0, 0, 1):
        for fila in tablero:
            print(" ".join(f"{paso:2}" for paso in fila))
        print("Los numeros indican el orden de las 64 visitas.")
        print("El recorrido empieza en la esquina superior izquierda (1).")
    else:
        print("No se encontro un recorrido.")


if __name__ == "__main__":
    main()
