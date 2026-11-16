import json

def cargar_tablero(name_file="Tablero.json"):
    try:
        with open(name_file, "r", encoding="utf-8") as archivo:
            tablero = json.load(archivo)
            
        

        pos_inicio = None
        pos_bomba = None

        for fila in range(len(tablero)):
            for col in range(len(tablero[0])):
                sim = str(tablero[fila][col])
                if sim == "R":
                    pos_inicio = (fila, col)
                elif sim == "B":
                    pos_bomba = (fila, col)
                    
        return tablero, pos_inicio, pos_bomba
    except Exception as error:
        print("Error al cargar el archivo JSON:", error)
        return None, None, None


def distancia_bomba(pos_actual, pos_bomba):

    fila_actual, col_actual = pos_actual
    fila_bomba, col_bomba = pos_bomba
    distancia_fila = abs(fila_actual - fila_bomba)
    distancia_columna = abs(col_actual - col_bomba)
    return distancia_fila + distancia_columna


def a_path(tablero, inicio, bomba):

    filas = len(tablero)
    columnas = len(tablero[0])

    h_inicial = distancia_bomba(inicio, bomba)

    open_set = [(h_inicial, inicio)] # Lista de casillas pendientes: [(suma_pesos, (fila, col))]
    viene_desde = {}
    costo = {inicio: 0}              # Costo g(n) desde el inicio hasta la casilla actual
    casillas_visitadas = set()       # Conjunto de casillas ya evaluadas

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while len(open_set) > 0:
        nodo_menor = min(open_set)
        open_set.remove(nodo_menor)
        f_actual, casilla_actual = nodo_menor

        # En caso de llegar a la bomba "EXITO"
        if casilla_actual == bomba:
            camino = []
            ubi_actual = casilla_actual

            # Reconstruccion de la ruta desde la bomba hasta el inicio siguiendo el historial
            while ubi_actual in viene_desde:
                camino.append(ubi_actual)
                ubi_actual = viene_desde[ubi_actual]
            camino.append(inicio)
            camino.reverse()
            return camino, costo[bomba]

        casillas_visitadas.add(casilla_actual)

        for movimiento in movimientos:
            fila_vecino = casilla_actual[0] + movimiento[0]
            col_vecino = casilla_actual[1] + movimiento[1]
            vecino = (fila_vecino, col_vecino)

            if (0 <= fila_vecino < filas and 0 <= col_vecino < columnas and 
                str(tablero[fila_vecino][col_vecino]) != "X" and 
                vecino not in casillas_visitadas):

                costo_g = costo[casilla_actual] + 1

                if vecino not in costo or costo_g < costo[vecino]:
                    costo[vecino] = costo_g
                    suma_pesos = costo_g + distancia_bomba(vecino, bomba)
                    open_set.append((suma_pesos, vecino))
                    viene_desde[vecino] = casilla_actual

    return None, 0 # Retorna None si no se encuentra un camino


def imprimir_camino(tablero, camino):
    """
    Imprime el tablero con el camino encontrado marcado con '*'.e
    """
    print("\n ========== TABLERO =========")
    for fila in range(len(tablero)):
        linea = ""
        for col in range(len(tablero[0])):
            val = str(tablero[fila][col])
            if (fila, col) in camino and val != "R" and val != "B":
                linea = linea + " * "
            else:
                linea = linea + " " + val + " "
        print(linea)
    print(" =============================")


if __name__ == "__main__":
    print("==========================================")
    print("              PATHFINDING A*              ")
    print("==========================================")

    tablero, inicio, bomba = cargar_tablero("Tablero.json")

    if tablero is not None and inicio is not None and bomba is not None:
        print("Robot encontrado en:", inicio)
        print("Bomba encontrada en:", bomba)

        camino, total_pasos = a_path(tablero, inicio, bomba)

        if camino is not None:
            print("\n¡YEIIII CAMINO ENCONTRADO! XD\n")
            print("Total de pasos (costo g):", total_pasos)
            print("Camino Recorrido:", camino)
            imprimir_camino(tablero, camino)
        else:
            print("\nNo existe un camino posible hacia la bomba.")
    else:
        print("Revisa que el archivo Tablero.json exista y tenga una 'R' y una 'B'.")