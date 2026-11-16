# caballos1.py
# Problema de los caballos 1: dos caballos blancos y dos negros en un tablero de 6x6 intercambian sus lugares.
#
# Reglas (confirmadas):
#   - Las posiciones iniciales se piden por input, en notación de ajedrez.
#   - Los turnos se alternan: blancos, negros, blancos, ...  (empiezan las blancas).
#   - Un caballo solo puede moverse a una casilla vacía (no hay capturas).
#
# Algoritmo elegido: BÚSQUEDA EN ANCHURA (BFS) sobre el espacio de estados.
#   Justificación: el espacio completo tiene menos de ~710 mil estados
#   (C(36,2) * C(34,2) * 2 turnos), así que BFS lo recorre en pocos segundos, nunca
#   se cicla porque guarda los estados ya vistos, y además la primera solución que
#   encuentra es la de menos movimientos.
#   Optimización sugerida por el profe: los movimientos de cada casilla se
#   PRECOMPUTAN una sola vez (MOVIMIENTOS) en lugar de recalcularlos en cada estado.

from collections import deque

# ---------------------------------------------------------------------------
# Constantes del tablero
# ---------------------------------------------------------------------------
N = 6                                   # tablero de N x N
COLUMNAS = "ABCDEF"                     # columnas (x) en notación de ajedrez
BLANCAS, NEGRAS = 0, 1                  # identificadores de turno / color

# Los 8 saltos posibles de un caballo: (delta_columna, delta_fila)
DELTAS = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))


# ---------------------------------------------------------------------------
# NÚCLEO FUNCIONAL
# ---------------------------------------------------------------------------

def a_nombre(indice):
    """Casilla (entero 0..35) -> notación de ajedrez. Ej: 0 -> 'A1', 7 -> 'B2'."""
    return COLUMNAS[indice % N] + str(indice // N + 1)


def a_indice(texto):
    """Notación de ajedrez -> entero 0..35, o None si no es una casilla válida.
    Ej: 'b3' -> 14. Usa match/case para 'unificar' la cadena con [columna, fila]."""
    match list(texto.strip().upper()):
        case [columna, fila] if columna in COLUMNAS and fila in "123456":
            return (int(fila) - 1) * N + COLUMNAS.index(columna)
        case _:
            return None


def saltos_desde(indice):
    """Casillas a las que un caballo puede saltar desde 'indice' (ignora ocupación).
    Comprensión: genera cada destino (columna+dc, fila+df) y filtra los que caen fuera."""
    columna, fila = indice % N, indice // N
    return tuple(
        nueva_fila * N + nueva_columna
        for dc, df in DELTAS
        for nueva_columna, nueva_fila in [(columna + dc, fila + df)]
        if 0 <= nueva_columna < N and 0 <= nueva_fila < N
    )


# PRECÓMPUTO: tabla casilla -> casillas destino. Se calcula una sola vez.
MOVIMIENTOS = tuple(saltos_desde(i) for i in range(N * N))


def sucesores(estado):
    """Todos los estados alcanzables en UN movimiento desde 'estado'.
    Un estado es (blancos, negros, turno): blancos y negros son tuplas ORDENADAS de
    2 casillas (así {A1,B3} y {B3,A1} son el mismo estado) y turno indica quién mueve.
    Devuelve una lista de (estado_siguiente, (color, origen, destino))."""
    blancos, negros, turno = estado
    propios = blancos if turno == BLANCAS else negros       # caballos que mueven
    ocupadas = set(blancos) | set(negros)                    # casillas no disponibles
    return [
        (
            # Se reemplaza el caballo movido; se reordena para normalizar el estado
            (tuple(sorted(destino if c == origen else c for c in propios)), negros, NEGRAS)
            if turno == BLANCAS else
            (blancos, tuple(sorted(destino if c == origen else c for c in propios)), BLANCAS),
            (turno, origen, destino),
        )
        for origen in propios
        for destino in MOVIMIENTOS[origen]
        if destino not in ocupadas                           # solo casillas vacías
    ]


def reconstruir(estado, padres):
    """Recorre la cadena de padres hacia atrás (recursión) y devuelve la tupla de
    movimientos desde el estado inicial hasta 'estado'.
    Equivale a: camino(Inicial, []). camino(E, [M|R]) :- padre(E, P, M), camino(P, R)."""
    match padres[estado]:
        case None:                                   # llegamos al estado inicial
            return ()
        case (anterior, movimiento):                 # unifica el par (padre, movimiento)
            return reconstruir(anterior, padres) + (movimiento,)


def buscar(inicial, meta_blancos, meta_negros):
    """BFS. Devuelve la tupla de movimientos de la solución, o None si no existe.
    EXCEPCIÓN a la inmutabilidad: 'padres' (estados vistos) y la cola 'frontera' se
    mutan localmente. Copiar un diccionario de cientos de miles de estados en cada
    paso haría el programa muchísimo más lento, y la mutación no escapa de esta
    función (desde fuera se comporta como una función pura)."""
    padres = {inicial: None}                         # estado -> (estado_previo, movimiento)
    frontera = deque([inicial])                      # cola FIFO: garantiza orden por nivel
    while frontera:
        actual = frontera.popleft()
        for siguiente, movimiento in sucesores(actual):
            if siguiente in padres:                  # ya visitado: se descarta
                continue
            padres[siguiente] = (actual, movimiento)
            # Meta: cada color ocupa las casillas iniciales del otro (el turno no importa)
            if siguiente[0] == meta_blancos and siguiente[1] == meta_negros:
                return reconstruir(siguiente, padres)
            frontera.append(siguiente)
    return None                                      # se agotó el espacio: sin solución


def aplicar(blancos, negros, movimiento):
    """Aplica un movimiento (color, origen, destino) y devuelve (blancos, negros) nuevos."""
    color, origen, destino = movimiento
    mover = lambda grupo: tuple(destino if c == origen else c for c in grupo)
    return (mover(blancos), negros) if color == BLANCAS else (blancos, mover(negros))


def dibujar(blancos, negros):
    """Tablero en texto. 'B' = caballo blanco, 'N' = caballo negro, '.' = vacía.
    Se dibuja con la fila 6 arriba, como un tablero de ajedrez real."""
    def simbolo(i):
        return "B" if i in blancos else "N" if i in negros else "."
    filas = [
        f"{fila + 1} | " + " ".join(simbolo(fila * N + c) for c in range(N))
        for fila in reversed(range(N))
    ]
    pie = ["  +" + "-" * (2 * N), "    " + " ".join(COLUMNAS)]
    return "\n".join(filas + pie)


# ---------------------------------------------------------------------------
# ENTRADA / SALIDA (imperativa, aislada del núcleo funcional)
# ---------------------------------------------------------------------------

def pedir_casilla(mensaje, ocupadas):
    """Pide una casilla por input hasta que sea válida (A1..F6) y no esté repetida."""
    while True:
        indice = a_indice(input(mensaje))
        if indice is None:
            print("  Casilla inválida. Usa notación de ajedrez, de A1 a F6.")
        elif indice in ocupadas:
            print("  Esa casilla ya está ocupada por otro caballo.")
        else:
            return indice


def main():
    print(f"Problema de los caballos 1 (tablero {N}x{N}): intercambio de lugares.")
    ocupadas = []
    for color, nombre in ((BLANCAS, "blanco"), (NEGRAS, "negro")):
        for numero in (1, 2):
            ocupadas.append(pedir_casilla(f"Casilla del caballo {nombre} {numero}: ", ocupadas))
    blancos = tuple(sorted(ocupadas[:2]))
    negros = tuple(sorted(ocupadas[2:]))

    # La meta es el intercambio: blancos donde estaban los negros y viceversa
    solucion = buscar((blancos, negros, BLANCAS), negros, blancos)

    if solucion is None:
        print("No existe solución para esas posiciones (con turnos alternados).")
        return

    print(f"\nSolución en {len(solucion)} movimientos.\n")
    print("Inicio:")
    print(dibujar(blancos, negros))
    for numero, movimiento in enumerate(solucion, start=1):
        color, origen, destino = movimiento
        blancos, negros = aplicar(blancos, negros, movimiento)
        print(f"\n{numero}. {'Blanco' if color == BLANCAS else 'Negro'}: "
              f"{a_nombre(origen)} -> {a_nombre(destino)}")
        print(dibujar(blancos, negros))


if __name__ == "__main__":
    main()
