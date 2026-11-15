"""Buscador A* sobre un tablero JSON de 10x10, compatible con ambos proyectos."""
import argparse
import heapq
import json
from pathlib import Path

MOVIMIENTOS = ((-1, 0), (1, 0), (0, -1), (0, 1))
LIBRES = {'.', '0'}
MUROS = {'#', 'X'}
VALIDOS = LIBRES | MUROS | {'R', 'B'}


def cargar_tablero(ruta):
    with open(ruta, encoding='utf-8') as archivo:
        datos = json.load(archivo)
    if not isinstance(datos, dict) or 'tablero' not in datos:
        raise ValueError('El JSON debe ser un objeto con la clave "tablero".')
    tablero = datos['tablero']
    if not isinstance(tablero, list) or len(tablero) != 10 or any(not isinstance(fila, list) or len(fila) != 10 for fila in tablero):
        raise ValueError('El tablero debe tener exactamente 10 filas y 10 columnas.')
    for i, fila in enumerate(tablero):
        for j, celda in enumerate(fila):
            if not isinstance(celda, str) or celda not in VALIDOS:
                raise ValueError(f'Celda inválida en fila {i+1}, columna {j+1}: {celda!r}.')
    robots = [(i, j) for i in range(10) for j in range(10) if tablero[i][j] == 'R']
    bombas = [(i, j) for i in range(10) for j in range(10) if tablero[i][j] == 'B']
    if len(robots) != 1 or len(bombas) != 1:
        raise ValueError('Debe existir exactamente un robot R y una bomba B.')
    return tablero, robots[0], bombas[0]


def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_estrella(tablero, inicio, destino):
    """Devuelve una ruta óptima con movimientos ortogonales de costo 1, o None."""
    pendientes = [(heuristica(inicio, destino), 0, inicio)]
    mejores_costos = {inicio: 0}
    padres = {}
    while pendientes:
        _, costo_actual, actual = heapq.heappop(pendientes)
        if costo_actual != mejores_costos.get(actual):
            continue
        if actual == destino:
            ruta = [actual]
            while ruta[-1] != inicio:
                ruta.append(padres[ruta[-1]])
            return ruta[::-1]
        for df, dc in MOVIMIENTOS:
            vecino = (actual[0] + df, actual[1] + dc)
            f, c = vecino
            if not (0 <= f < 10 and 0 <= c < 10) or tablero[f][c] in MUROS:
                continue
            nuevo = costo_actual + 1
            if nuevo < mejores_costos.get(vecino, float('inf')):
                mejores_costos[vecino] = nuevo
                padres[vecino] = actual
                heapq.heappush(pendientes, (nuevo + heuristica(vecino, destino), nuevo, vecino))
    return None


def coordenada(pos):
    return f'{chr(65 + pos[1])}{pos[0] + 1}'


def mostrar_tablero(tablero, ruta=None):
    copia = [fila[:] for fila in tablero]
    for f, c in ruta or []:
        if copia[f][c] not in ('R', 'B'):
            copia[f][c] = '*'
    print('    ' + ' '.join('ABCDEFGHIJ'))
    for i, fila in enumerate(copia, start=1):
        print(f'{i:>2}  ' + ' '.join(fila))


def resolver(ruta_archivo):
    tablero, inicio, destino = cargar_tablero(ruta_archivo)
    ruta = a_estrella(tablero, inicio, destino)
    print(f'Robot: {coordenada(inicio)} | Bomba: {coordenada(destino)}')
    if ruta is None:
        print('No existe un camino hacia la bomba.')
    else:
        print(f'Camino óptimo: {len(ruta)-1} pasos.')
        print('Ruta: ' + ' -> '.join(map(coordenada, ruta)))
    mostrar_tablero(tablero, ruta)
    return ruta


def main():
    parser = argparse.ArgumentParser(description='Pathfinding A* con tablero JSON de 10x10.')
    parser.add_argument('archivo', nargs='?', default=str(Path(__file__).with_name('tablero.json')), help='Ruta del tablero JSON')
    args = parser.parse_args()
    try:
        resolver(args.archivo)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
