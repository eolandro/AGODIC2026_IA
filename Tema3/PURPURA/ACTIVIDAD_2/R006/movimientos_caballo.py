import json

COLUMNAS = "abcdefgh"
FILAS = "12345678"

# Los 8 saltos posibles del caballo en forma de "L" (dx = columna, dy = fila)
SALTOS = [(1, 2), (2, 1), (2, -1), (1, -2),
          (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def movimientos_caballo(casilla):
    """Regresa la lista de casillas a las que puede saltar un caballo desde 'casilla'."""
    x = COLUMNAS.index(casilla[0])
    y = FILAS.index(casilla[1])
    destinos = []
    for dx, dy in SALTOS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8:  # que no se salga del tablero
            destinos.append(COLUMNAS[nx] + FILAS[ny])
    return sorted(destinos)


def generar_tablero():
    tablero = {}
    for fila in FILAS:
        for col in COLUMNAS:
            casilla = col + fila
            tablero[casilla] = movimientos_caballo(casilla)
    return tablero


if __name__ == "__main__":
    datos = generar_tablero()
    with open("movimientos_caballo.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print(f"JSON generado con {len(datos)} casillas.")
    print("Ejemplo a1:", datos["a1"])
    print("Ejemplo d4:", datos["d4"])
