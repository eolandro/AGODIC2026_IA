from collections import deque

N = 6

# Posiciones iniciales
inicio = {
    "N1": (0, 0),
    "N2": (0, 5),
    "B1": (5, 0),
    "B2": (5, 5)
}

# Meta: los caballos intercambian lugares
meta = {
    "N1": (5, 0),
    "N2": (5, 5),
    "B1": (0, 0),
    "B2": (0, 5)
}

# Movimientos válidos del caballo
movimientos = [
    (-2, -1), (-2, 1),
    (-1, -2), (-1, 2),
    (1, -2), (1, 2),
    (2, -1), (2, 1)
]

def dentro(f, c):
    return 0 <= f < N and 0 <= c < N

def estado_a_tupla(estado):
    return tuple(sorted(estado.items()))

def imprimir_tablero(estado, titulo):
    tablero = [["." for _ in range(N)] for _ in range(N)]

    for caballo, (f, c) in estado.items():
        tablero[f][c] = caballo[0]

    print(f"\n{titulo}")
    print("    0  1  2  3  4  5")
    print("  +------------------")

    for f in range(N):
        linea = f"{f} |"

        for c in range(N):
            linea += f" {tablero[f][c]} "

        print(linea)

    print()

def imprimir_recorrido(camino):
    print("\nRecorrido de los caballos:")

    for paso, (caballo, origen, destino) in enumerate(camino, 1):
        print(
            f"Paso {paso}: mover {caballo} "
            f"de {origen} a {destino}"
        )

def resolver():
    cola = deque()
    visitados = set()

    # La cola guarda el estado actual y el recorrido hasta ese estado
    cola.append((inicio, []))
    visitados.add(estado_a_tupla(inicio))

    imprimir_tablero(inicio, "ESTADO INICIAL")

    while cola:
        estado, camino = cola.popleft()

        # Se llegó a la meta
        if estado == meta:
            return camino

        ocupadas = set(estado.values())

        for caballo, (f, c) in estado.items():
            for df, dc in movimientos:
                nf = f + df
                nc = c + dc

                if not dentro(nf, nc):
                    continue

                if (nf, nc) in ocupadas:
                    continue

                nuevo_estado = dict(estado)
                nuevo_estado[caballo] = (nf, nc)

                clave = estado_a_tupla(nuevo_estado)

                if clave in visitados:
                    continue

                visitados.add(clave)

                nuevo_camino = camino + [
                    (caballo, (f, c), (nf, nc))
                ]

                cola.append((nuevo_estado, nuevo_camino))

    return None

solucion = resolver()

if solucion:
    print(f"\nSolución encontrada en {len(solucion)} movimientos.")

    imprimir_recorrido(solucion)

    # Reconstruir e imprimir el tablero después de cada movimiento
    estado_actual = dict(inicio)

    for paso, (caballo, origen, destino) in enumerate(solucion, 1):
        estado_actual[caballo] = destino

        imprimir_tablero(
            estado_actual,
            f"Después del paso {paso}: {caballo} se movió de {origen} a {destino}"
        )

    imprimir_tablero(estado_actual, "ESTADO FINAL")

    if estado_actual == meta:
        print("Los caballos intercambiaron correctamente sus posiciones.")
else:
    print("No se encontró solución.")