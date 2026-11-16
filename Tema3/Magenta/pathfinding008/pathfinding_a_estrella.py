import json
import heapq

MOVIMIENTOS = [
    (-1, 0),  # arriba
    (1, 0),   # abajo
    (0, -1),  # izquierda
    (0, 1)    # derecha
]


def cargar_tablero(ruta="tablero.json"):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        tablero = datos["tablero"]

        inicio = None
        bomba = None

        for fila in range(len(tablero)):
            for columna in range(len(tablero[0])):
                if tablero[fila][columna] == "R":
                    inicio = (fila, columna)
                elif tablero[fila][columna] == "B":
                    bomba = (fila, columna)

        if inicio is None or bomba is None:
            print("Error: el tablero debe contener una 'R' y una 'B'.")
            return None, None, None

        return tablero, inicio, bomba

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{ruta}'.")
        return None, None, None

    except KeyError:
        print("Error: el JSON debe tener la clave 'tablero'.")
        return None, None, None

    except json.JSONDecodeError as error:
        print("Error: el archivo JSON tiene un formato inválido.")
        print(error)
        return None, None, None


def heuristica_manhattan(pos_actual, pos_bomba):
    fila_actual, columna_actual = pos_actual
    fila_bomba, columna_bomba = pos_bomba

    return abs(fila_actual - fila_bomba) + abs(columna_actual - columna_bomba)


def a_estrella(tablero, inicio, bomba):
    filas = len(tablero)
    columnas = len(tablero[0])

    lista_abierta = []
    viene_de = {}
    costo_g = {inicio: 0}
    visitados = set()

    h_inicial = heuristica_manhattan(inicio, bomba)
    f_inicial = costo_g[inicio] + h_inicial

    heapq.heappush(lista_abierta, (f_inicial, h_inicial, inicio))

    while lista_abierta:
        f_actual, h_actual, actual = heapq.heappop(lista_abierta)

        if actual in visitados:
            continue

        visitados.add(actual)

        if actual == bomba:
            camino = []
            nodo = actual

            while nodo in viene_de:
                camino.append(nodo)
                nodo = viene_de[nodo]

            camino.append(inicio)
            camino.reverse()

            return camino, costo_g[bomba]

        fila_actual, columna_actual = actual

        for movimiento_fila, movimiento_columna in MOVIMIENTOS:
            fila_vecina = fila_actual + movimiento_fila
            columna_vecina = columna_actual + movimiento_columna
            vecino = (fila_vecina, columna_vecina)

            dentro_del_tablero = (
                0 <= fila_vecina < filas
                and 0 <= columna_vecina < columnas
            )

            if not dentro_del_tablero:
                continue

            if tablero[fila_vecina][columna_vecina] == "X":
                continue

            if vecino in visitados:
                continue

            nuevo_costo_g = costo_g[actual] + 1

            if vecino not in costo_g or nuevo_costo_g < costo_g[vecino]:
                costo_g[vecino] = nuevo_costo_g
                h_vecino = heuristica_manhattan(vecino, bomba)
                f_vecino = nuevo_costo_g + h_vecino

                viene_de[vecino] = actual
                heapq.heappush(
                    lista_abierta,
                    (f_vecino, h_vecino, vecino)
                )

    return None, None


def imprimir_tablero(tablero, camino):
    print("\n========== TABLERO CON CAMINO ==========")

    camino_sin_inicio = set(camino[1:-1])

    for fila in range(len(tablero)):
        linea = ""

        for columna in range(len(tablero[0])):
            valor = tablero[fila][columna]
            posicion = (fila, columna)

            if posicion in camino_sin_inicio:
                linea += " * "
            else:
                linea += f" {valor} "

        print(linea)

    print("=========================================")


def main():
    print("==========================================")
    print("       PATHFINDING A* - BOOME")
    print("==========================================")

    tablero, inicio, bomba = cargar_tablero("tablero.json")

    if tablero is None:
        return

    print(f"\nBoome (R) está en: {inicio}")
    print(f"La bomba (B) está en: {bomba}")

    camino, costo_total = a_estrella(tablero, inicio, bomba)

    if camino is None:
        print("\nNo existe un camino posible hacia la bomba.")
        return

    print("\n¡Camino encontrado!")
    print(f"Total de movimientos: {costo_total}")
    print(f"Ruta de Boome: {camino}")

    imprimir_tablero(tablero, camino)


if __name__ == "__main__":
    main()