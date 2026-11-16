import sys

# ============================================
# COMESOLO - TABLERO TRIANGULAR DE 15 POSICIONES
# ============================================
#
# Distribución del tablero:
#
#       (1,1)
#     (2,1) (2,2)
#   (3,1) (3,2) (3,3)
# (4,1) (4,2) (4,3) (4,4)
# (5,1) (5,2) (5,3) (5,4) (5,5)
#
# El usuario ingresa la posición de la ficha faltante.
# El programa busca dejar una sola ficha en esa misma posición.
# Imprime el tablero después de cada movimiento.

FILAS = 5

# Direcciones válidas en el tablero triangular.
# Cada salto recorre dos posiciones en la misma dirección.
DIRS = [
    (0, 1),    # derecha
    (0, -1),   # izquierda
    (1, 0),    # abajo izquierda
    (1, 1),    # abajo derecha
    (-1, 0),   # arriba derecha
    (-1, -1)   # arriba izquierda
]


def coordenada_valida(fila, columna):
    """
    Verifica si una posición pertenece a la pirámide de 15 huecos.
    """
    return 1 <= fila <= FILAS and 1 <= columna <= fila


def convertir_posicion(texto):
    """
    Convierte una entrada como '1,1', '3,2' o '5 5'
    en una tupla (fila, columna).
    """
    texto = texto.replace(",", " ").strip()
    partes = texto.split()

    if len(partes) != 2:
        raise ValueError("Usa el formato: fila,columna. Ejemplo: 1,1")

    try:
        fila = int(partes[0])
        columna = int(partes[1])
    except ValueError:
        raise ValueError("La fila y la columna deben ser números enteros.")

    if not coordenada_valida(fila, columna):
        raise ValueError(
            "Coordenada inválida.\n"
            "La columna debe estar entre 1 y el número de la fila.\n"
            "Ejemplo válido: 3,2"
        )

    return fila, columna


def generar_movimientos():
    """
    Genera todos los saltos posibles del tablero triangular.

    Cada movimiento es una tupla:
    (origen, ficha que se elimina, destino)
    """
    movimientos = []

    for fila in range(1, FILAS + 1):
        for columna in range(1, fila + 1):
            if not coordenada_valida(fila, columna):
                continue

            for df, dc in DIRS:
                fila_intermedia = fila + df
                columna_intermedia = columna + dc

                fila_destino = fila + 2 * df
                columna_destino = columna + 2 * dc

                if coordenada_valida(fila_intermedia, columna_intermedia) and \
                   coordenada_valida(fila_destino, columna_destino):

                    movimientos.append(
                        (
                            (fila, columna),
                            (fila_intermedia, columna_intermedia),
                            (fila_destino, columna_destino)
                        )
                    )

    return movimientos


MOVIMIENTOS = generar_movimientos()


def formato(pos):
    """
    Convierte una posición (fila, columna) en texto legible.
    """
    fila, columna = pos
    return f"({fila},{columna})"


def resolver(hueco_inicial):
    """
    Resuelve el comesolo dejando una sola ficha
    exactamente en el hueco inicial.
    """
    f0, c0 = hueco_inicial

    # Al inicio hay fichas en todas las posiciones,
    # excepto en el hueco indicado por el usuario.
    tablero_inicial = frozenset(
        (fila, columna)
        for fila in range(1, FILAS + 1)
        for columna in range(1, fila + 1)
        if (fila, columna) != (f0, c0)
    )

    visitados = set()
    solucion = []

    def buscar(tablero_actual):
        # Si queda una sola ficha, se verifica que esté en el hueco inicial.
        if len(tablero_actual) == 1:
            return (f0, c0) in tablero_actual

        clave = (tablero_actual, (f0, c0))

        if clave in visitados:
            return False

        visitados.add(clave)

        for origen, intermedio, destino in MOVIMIENTOS:
            if (
                origen in tablero_actual
                and intermedio in tablero_actual
                and destino not in tablero_actual
            ):
                nuevo_tablero = (tablero_actual - {origen, intermedio}) | {destino}
                solucion.append((origen, intermedio, destino))

                if buscar(nuevo_tablero):
                    return True

                solucion.pop()

        return False

    if buscar(tablero_inicial):
        return solucion

    return None


def imprimir_tablero(tablero, hueco_inicial):
    """
    Imprime el estado actual del tablero triangular.
    """
    print()

    for fila in range(1, FILAS + 1):
        espacios = "  " * (FILAS - fila)
        linea = espacios

        for columna in range(1, fila + 1):
            if (fila, columna) in tablero:
                linea += "O "
            elif (fila, columna) == hueco_inicial:
                linea += "* "
            else:
                linea += ". "

        print(linea)

    print()


def main():
    print("COMESOLO - TABLERO TRIANGULAR DE 15 POSICIONES")
    print("\nDistribución del tablero:")
    print("      (1,1)")
    print("    (2,1) (2,2)")
    print("  (3,1) (3,2) (3,3)")
    print("(4,1) (4,2) (4,3) (4,4)")
    print("(5,1) (5,2) (5,3) (5,4) (5,5)")

    print("\nFormato para ingresar la pieza faltante: fila,columna")
    print("Ejemplo: 1,1")

    try:
        entrada = input("\nIngresa la posición de la pieza faltante: ")
        hueco_inicial = convertir_posicion(entrada)
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)

    print(f"\nBuscando solución dejando la última ficha en {formato(hueco_inicial)}...\n")

    solucion = resolver(hueco_inicial)

    if solucion is None:
        print("No existe solución dejando la última ficha en esa misma posición.")
        sys.exit(0)

    print(f"Solución encontrada con {len(solucion)} movimientos:\n")

    # Estado inicial del tablero.
    tablero = set(
        (fila, columna)
        for fila in range(1, FILAS + 1)
        for columna in range(1, fila + 1)
        if (fila, columna) != hueco_inicial
    )

    print("Estado inicial:")
    imprimir_tablero(tablero, hueco_inicial)

    # Se aplica cada movimiento y se imprime el tablero resultante.
    for numero, (origen, intermedio, destino) in enumerate(solucion, start=1):
        print(
            f"Movimiento {numero}: "
            f"{formato(origen)} salta sobre {formato(intermedio)} "
            f"hacia {formato(destino)}"
        )

        tablero.remove(origen)
        tablero.remove(intermedio)
        tablero.add(destino)

        print(f"Estado después del movimiento {numero}:")
        imprimir_tablero(tablero, hueco_inicial)

    # Movimiento final obligatorio.
    ultimo_origen, ultimo_intermedio, ultimo_destino = solucion[-1]

    print("MOVIMIENTO FINAL:")
    print(
        f"{formato(ultimo_origen)} salta sobre {formato(ultimo_intermedio)} "
        f"hacia {formato(ultimo_destino)}"
    )


if __name__ == "__main__":
    main()