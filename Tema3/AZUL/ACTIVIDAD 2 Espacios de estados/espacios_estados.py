"""
Nombre: Espacios de estados
Descripción: Demostración de algoritmos de búsqueda.
Reactivos: R004, R005, R006 y R007.

Archivos JSON necesarios:
- caballos_1.json
- come_solo.json

Los archivos JSON deben estar en la misma carpeta que este programa.
"""

import json
from collections import deque
from pathlib import Path

CARPETA = Path(__file__).resolve().parent

MOVIMIENTOS_CABALLO = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1)
]


def cargar_json(nombre):
    ruta = CARPETA / nombre
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(str(c) for c in fila))
    print()


def convertir_casilla(casilla, tamano):
    casilla = casilla.strip().upper()
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if len(casilla) < 2 or casilla[0] not in letras[:tamano]:
        raise ValueError(f"Casilla no válida: {casilla}")

    try:
        fila = int(casilla[1:]) - 1
    except ValueError:
        raise ValueError(f"Casilla no válida: {casilla}")

    columna = letras.index(casilla[0])

    if not (0 <= fila < tamano):
        raise ValueError(f"Casilla fuera del tablero: {casilla}")

    return fila, columna


def nombre_casilla(fila, columna):
    return "ABCDEFGH"[columna] + str(fila + 1)


# ============================================================
# R004. PROBLEMA DE LAS 4 REINAS
# ============================================================

def cuatro_reinas():
    n = 4
    posiciones = [-1] * n
    soluciones = []

    def buscar(fila):
        if fila == n:
            soluciones.append(posiciones.copy())
            return

        for columna in range(n):
            segura = True

            for anterior in range(fila):
                misma_columna = posiciones[anterior] == columna
                misma_diagonal = (
                    abs(posiciones[anterior] - columna)
                    == abs(anterior - fila)
                )

                if misma_columna or misma_diagonal:
                    segura = False
                    break

            if segura:
                posiciones[fila] = columna
                buscar(fila + 1)
                posiciones[fila] = -1

    buscar(0)

    print("\nR004 - PROBLEMA DE LAS 4 REINAS")
    print("Q = Reina | . = Casilla vacía")
    print("Soluciones encontradas:", len(soluciones))

    for numero, solucion in enumerate(soluciones, 1):
        print(f"\nSolución {numero}:")
        tablero = [["." for _ in range(n)] for _ in range(n)]

        for fila, columna in enumerate(solucion):
            tablero[fila][columna] = "Q"

        imprimir_tablero(tablero)


# ============================================================
# R005. INTERCAMBIO DE CABALLOS EN TABLERO 6x6
# Búsqueda bidireccional en anchura
# ============================================================

def intercambiar_caballos():
    configuracion = cargar_json("caballos_1.json")
    n = configuracion["tamano"]
    inicio = tuple(
        convertir_casilla(c, n)[0] * n + convertir_casilla(c, n)[1]
        for c in configuracion["inicio"]
    )
    objetivo = tuple(
        convertir_casilla(c, n)[0] * n + convertir_casilla(c, n)[1]
        for c in configuracion["objetivo"]
    )
    nombres = configuracion["piezas"]

    if len(set(inicio)) != len(inicio) or len(set(objetivo)) != len(objetivo):
        print("La configuración contiene posiciones repetidas.")
        return

    def sucesores(estado):
        ocupadas = set(estado)

        for i, posicion in enumerate(estado):
            fila, columna = divmod(posicion, n)

            for df, dc in MOVIMIENTOS_CABALLO:
                nf, nc = fila + df, columna + dc

                if 0 <= nf < n and 0 <= nc < n:
                    destino = nf * n + nc

                    if destino not in ocupadas:
                        nuevo = list(estado)
                        nuevo[i] = destino
                        yield tuple(nuevo)

    def reconstruir(camino_inicio, camino_objetivo, encuentro):
        camino = []
        actual = encuentro

        while actual is not None:
            camino.append(actual)
            actual = camino_inicio[actual]

        camino.reverse()

        actual = camino_objetivo[encuentro]
        while actual is not None:
            camino.append(actual)
            actual = camino_objetivo[actual]

        return camino

    def buscar_bidireccional():
        if inicio == objetivo:
            return [inicio]

        cola_inicio = deque([inicio])
        cola_objetivo = deque([objetivo])

        anterior_inicio = {inicio: None}
        anterior_objetivo = {objetivo: None}

        while cola_inicio and cola_objetivo:
            if len(cola_inicio) <= len(cola_objetivo):
                estado = cola_inicio.popleft()

                for nuevo in sucesores(estado):
                    if nuevo not in anterior_inicio:
                        anterior_inicio[nuevo] = estado

                        if nuevo in anterior_objetivo:
                            return reconstruir(
                                anterior_inicio,
                                anterior_objetivo,
                                nuevo
                            )

                        cola_inicio.append(nuevo)
            else:
                estado = cola_objetivo.popleft()

                for nuevo in sucesores(estado):
                    if nuevo not in anterior_objetivo:
                        anterior_objetivo[nuevo] = estado

                        if nuevo in anterior_inicio:
                            return reconstruir(
                                anterior_inicio,
                                anterior_objetivo,
                                nuevo
                            )

                        cola_objetivo.append(nuevo)

        return None

    print(f"\nR005 - INTERCAMBIO DE CABALLOS ({n}x{n})")
    print("Algoritmo: búsqueda bidireccional en anchura (BFS).")

    camino = buscar_bidireccional()

    if camino is None:
        print("No se encontró una solución con esta configuración.")
        return

    print("Movimientos necesarios:", len(camino) - 1)

    for paso, estado in enumerate(camino):
        tablero = [["." for _ in range(n)] for _ in range(n)]

        for i, posicion in enumerate(estado):
            fila, columna = divmod(posicion, n)
            tablero[fila][columna] = nombres[i]

        print(f"\nPaso {paso}:")
        imprimir_tablero(tablero)


# ============================================================
# R006. RECORRIDO COMPLETO DEL CABALLO EN TABLERO 8x8
# Warnsdorff + backtracking
# ============================================================

def recorrido_caballo():
    n = 8
    tablero = [[-1] * n for _ in range(n)]

    entrada = input(
        "\nIndica la casilla inicial del caballo (A1-H8, ejemplo D4): "
    ).strip().upper()

    try:
        fila_inicial, columna_inicial = convertir_casilla(entrada, n)
    except ValueError as error:
        print(error)
        return

    tablero[fila_inicial][columna_inicial] = 1

    def contar_salidas(fila, columna):
        total = 0

        for df, dc in MOVIMIENTOS_CABALLO:
            nf, nc = fila + df, columna + dc

            if (0 <= nf < n and 0 <= nc < n
                    and tablero[nf][nc] == -1):
                total += 1

        return total

    def buscar(fila, columna, paso):
        if paso == n * n:
            return True

        candidatos = []

        for df, dc in MOVIMIENTOS_CABALLO:
            nf, nc = fila + df, columna + dc

            if (0 <= nf < n and 0 <= nc < n
                    and tablero[nf][nc] == -1):
                candidatos.append((contar_salidas(nf, nc), nf, nc))

        candidatos.sort()

        for _, nf, nc in candidatos:
            tablero[nf][nc] = paso + 1

            if buscar(nf, nc, paso + 1):
                return True

            tablero[nf][nc] = -1

        return False

    print("\nR006 - RECORRIDO DEL CABALLO (8x8)")
    print("Casilla inicial:", entrada)
    print("Buscando un recorrido por las 64 casillas...")

    if buscar(fila_inicial, columna_inicial, 1):
        print("\nRecorrido encontrado.")
        print("Cada número indica el orden de visita:")
        print("El tablero se muestra desde la fila 8 hasta la fila 1.\n")

        for fila in range(n - 1, -1, -1):
            print(" ".join(f"{tablero[fila][col]:02d}" for col in range(n)))
    else:
        print("No se encontró un recorrido completo desde esa casilla.")


# ============================================================
# R007. JUEGO DEL COME SOLO
# DFS + backtracking + representación binaria de estados
# ============================================================

def come_solo():
    configuracion = cargar_json("come_solo.json")
    tablero_config = configuracion["tablero"]
    filas = configuracion["filas"]

    if len(tablero_config) != filas or any(
        len(fila) != filas for fila in tablero_config
    ):
        print("El tablero del archivo JSON no tiene dimensiones válidas.")
        return

    casillas = [
        (f, c)
        for f in range(filas)
        for c in range(filas)
        if tablero_config[f][c] != -1
    ]

    vacias = [
        (f, c)
        for f in range(filas)
        for c in range(filas)
        if tablero_config[f][c] == 0
    ]

    if len(vacias) != 1:
        print("El archivo JSON debe contener exactamente una casilla vacía (0).")
        return

    if any(tablero_config[f][c] not in (-1, 0, 1)
           for f in range(filas) for c in range(filas)):
        print("El JSON solo puede contener -1, 0 y 1.")
        return

    indice = {posicion: i for i, posicion in enumerate(casillas)}
    vacia = indice[vacias[0]]

    estado_inicial = (1 << len(casillas)) - 1
    estado_inicial &= ~(1 << vacia)

    movimientos = []

    for fila, columna in casillas:
        for df, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            medio = (fila + df, columna + dc)
            destino = (fila + 2 * df, columna + 2 * dc)

            if medio in indice and destino in indice:
                movimientos.append((
                    indice[(fila, columna)],
                    indice[medio],
                    indice[destino]
                ))

    def imprimir_estado(estado):
        tablero = []

        for f in range(filas):
            fila = []

            for c in range(filas):
                if tablero_config[f][c] == -1:
                    fila.append(" ")
                elif estado & (1 << indice[(f, c)]):
                    fila.append("X")
                else:
                    fila.append(".")

            tablero.append(fila)

        imprimir_tablero(tablero)

    fallidos = set()
    camino = []

    def resolver(estado, piezas):
        if piezas == 1:
            return True

        if estado in fallidos:
            return False

        for origen, medio, destino in movimientos:
            bit_origen = 1 << origen
            bit_medio = 1 << medio
            bit_destino = 1 << destino

            if (estado & bit_origen
                    and estado & bit_medio
                    and not estado & bit_destino):

                nuevo_estado = estado ^ (
                    bit_origen | bit_medio | bit_destino
                )

                # Se guardan las tres posiciones para reproducir
                # correctamente cada movimiento.
                camino.append((origen, medio, destino))

                if resolver(nuevo_estado, piezas - 1):
                    return True

                camino.pop()

        fallidos.add(estado)
        return False

    piezas_iniciales = estado_inicial.bit_count()

    print("\nR007 - JUEGO DEL COME SOLO")
    print("Tablero cargado desde come_solo.json.")
    print("Casilla vacía inicial:", (vacias[0][0] + 1, vacias[0][1] + 1))
    print("\nTablero inicial:")
    imprimir_estado(estado_inicial)
    print("Piezas iniciales:", piezas_iniciales)
    print("Algoritmo: DFS con backtracking y estados binarios.")
    print("Buscando solución...")

    if resolver(estado_inicial, piezas_iniciales):
        print("\nSolución encontrada.")
        print("Movimientos:", len(camino))

        estado = estado_inicial
        for numero, (origen, medio, destino) in enumerate(camino, 1):
            estado ^= (
                (1 << origen)
                | (1 << medio)
                | (1 << destino)
            )

            fila_o, col_o = casillas[origen]
            fila_m, col_m = casillas[medio]
            fila_d, col_d = casillas[destino]

            print(
                f"\nMovimiento {numero}: "
                f"({fila_o + 1},{col_o + 1}) salta sobre "
                f"({fila_m + 1},{col_m + 1}) y llega a "
                f"({fila_d + 1},{col_d + 1})"
            )
            imprimir_estado(estado)

        print("Piezas restantes:", estado.bit_count())
    else:
        print("No se encontró solución para la casilla vacía indicada.")


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def main():
    while True:
        print("=" * 48)
        print("       ALGORITMOS DE ESPACIOS DE ESTADOS")
        print("=" * 48)
        print("1. Problema de las 4 reinas (R004)")
        print("2. Intercambio de caballos 6x6 (R005)")
        print("3. Recorrido del caballo 8x8 (R006)")
        print("4. Juego del come solo (R007)")
        print("5. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            cuatro_reinas()
        elif opcion == "2":
            intercambiar_caballos()
        elif opcion == "3":
            recorrido_caballo()
        elif opcion == "4":
            come_solo()
        elif opcion == "5":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida.")

        input("\nPresiona Enter para regresar al menú...")


if __name__ == "__main__":
    print("\nPROGRAMA DE ESPACIOS DE ESTADOS INICIADO")
    print("Verificando archivos de configuración...")
    for archivo in ("caballos_1.json", "come_solo.json"):
        ruta = CARPETA / archivo
        if ruta.exists():
            print(f"[OK] {archivo}")
        else:
            print(f"[AVISO] No se encontró {archivo}; se necesitará para ejecutar su ejercicio.")
    print()
    main()
