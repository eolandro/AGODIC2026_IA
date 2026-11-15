import json
from pathlib import Path


# R007: Leer configuracion del tablero
def leer_tablero(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


# R007: Generar posiciones validas
def crear_posiciones(filas):
    posiciones = []

    for fila in range(filas):
        for columna in range(fila + 1):
            posiciones.append((fila, columna))

    return posiciones


# R007: Generar movimientos posibles
def generar_movimientos(posiciones):
    direcciones = [
        (0, -1), (0, 1),
        (-1, -1), (-1, 0),
        (1, 0), (1, 1)
    ]

    movimientos = []
    indice = {}

    for numero in range(len(posiciones)):
        indice[posiciones[numero]] = numero

    for numero, posicion in enumerate(posiciones):
        fila, columna = posicion

        for df, dc in direcciones:
            intermedia = (fila + df, columna + dc)
            destino = (fila + 2 * df, columna + 2 * dc)

            if intermedia in indice and destino in indice:
                movimientos.append(
                    (numero, indice[intermedia], indice[destino])
                )

    return movimientos


# R007: Imprimir tablero con numeros
def imprimir_tablero(estado, posiciones, resaltar=None):
    indice = {}
    for numero in range(len(posiciones)):
        indice[posiciones[numero]] = numero

    print()

    for fila in range(5):
        espacios = " " * (4 - fila)
        texto = espacios

        for columna in range(fila + 1):
            numero = indice[(fila, columna)]

            if estado & (1 << numero):
                if resaltar is not None and numero == resaltar:
                    texto += "1 "          # ficha final
                else:
                    texto += f"{numero + 1:2d} "  # ficha normal
            else:
                texto += " 0 "             # hueco vacio

        print(texto)


# R007: Resolver Come Solo mediante DFS
def resolver(estado, movimientos, posiciones):
    visitados = set()
    camino = []

    def buscar(estado):
        # Condicion de finalizacion
        if estado.bit_count() == 1:
            return True

        # Evitar repetir estados
        if estado in visitados:
            return False

        visitados.add(estado)

        for origen, medio, destino in movimientos:

            pieza_origen = 1 << origen
            pieza_medio = 1 << medio
            pieza_destino = 1 << destino

            # Verificar si el movimiento es valido
            if (estado & pieza_origen
                    and estado & pieza_medio
                    and not estado & pieza_destino):

                nuevo_estado = estado ^ (
                    pieza_origen | pieza_medio | pieza_destino
                )

                camino.append((origen, medio, destino))

                if buscar(nuevo_estado):
                    return True

                camino.pop()

        return False

    if buscar(estado):
        return camino

    return None


# R007: Mostrar solucion
def mostrar_solucion(camino, estado, posiciones):

    print("\nTABLERO INICIAL")
    imprimir_tablero(estado, posiciones)

    for numero, movimiento in enumerate(camino, 1):

        origen, medio, destino = movimiento

        estado ^= (
            (1 << origen) |
            (1 << medio) |
            (1 << destino)
        )

        print(f"\nMovimiento {numero}: "
            f"{posiciones[origen]} -> {posiciones[destino]} "
            f"(elimina {posiciones[medio]})")

        imprimir_tablero(estado, posiciones)

    print("\nRESULTADO FINAL")
    print("Piezas restantes:", estado.bit_count())

    # Marcar la ficha que sobrevivio
    for i in range(len(posiciones)):
        if estado & (1 << i):
            imprimir_tablero(estado, posiciones, resaltar=i)
            break


# Programa principal
def main():

    ruta = Path(__file__).resolve().parent / "come_solo.json"

    configuracion = leer_tablero(ruta)

    filas = configuracion["filas"]
    tablero = configuracion["tablero"]

    posiciones = crear_posiciones(filas)

    # Identificar la posicion vacia
    vacias = []

    for fila in range(filas):
        for columna in range(fila + 1):
            if tablero[fila][columna] == 0:
                vacias.append((fila, columna))

    if len(vacias) != 1:
        print("Error: debe existir exactamente una posicion vacia.")
        return

    if len(posiciones) != sum(len(fila) for fila in tablero):
        print("Error: la estructura del tablero no es valida.")
        return

    movimientos = generar_movimientos(posiciones)

    # Crear estado inicial
    estado = (1 << len(posiciones)) - 1

    indice = {}
    for numero in range(len(posiciones)):
        indice[posiciones[numero]] = numero

    estado ^= 1 << indice[vacias[0]]

    print("PROBLEMA DEL COME SOLO")
    print("Tablero triangular:", filas, "filas")
    print("Posiciones:", len(posiciones))
    print("Piezas iniciales:", estado.bit_count())
    print("Posicion vacia:", vacias[0])
    print("Algoritmo: DFS con Backtracking")

    # Buscar solucion
    camino = resolver(estado, movimientos, posiciones)

    if camino is None:
        print("\nNo se encontro una solucion.")
    else:
        print("\nSOLUCION ENCONTRADA")
        print("Total de movimientos:", len(camino))

        mostrar_solucion(camino, estado, posiciones)


if __name__ == "__main__":
    main()