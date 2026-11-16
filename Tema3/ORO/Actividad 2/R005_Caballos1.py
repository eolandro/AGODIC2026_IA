import sys
from collections import deque

try:
    sys.stdout.reconfigure(encoding="utf-8")   # para la consola de Windows
except AttributeError:
    pass

N = 6  # tamaño del tablero

# Posiciones iniciales (se pueden cambiar). Notación de ajedrez:
# columnas a-f, filas 1-6 (la fila 6 se dibuja arriba).
NEGROS_INICIO = ["a6", "f6"]
BLANCOS_INICIO = ["a1", "f1"]

SALTOS = [(1, 2), (2, 1), (2, -1), (1, -2),
          (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

NEGRO, BLANCO, VACIA = "♞", "♘", "·"


def a_coord(casilla):
    """'b3' -> (columna 1, fila 2)"""
    return ord(casilla[0]) - ord("a"), int(casilla[1:]) - 1


def a_nombre(coord):
    c, f = coord
    return f"{chr(ord('a') + c)}{f + 1}"


def saltos_validos(coord):
    c, f = coord
    for dc, df in SALTOS:
        nc, nf = c + dc, f + df
        if 0 <= nc < N and 0 <= nf < N:
            yield nc, nf


def sucesores(estado):
    """Todos los estados a un movimiento de distancia."""
    negros, blancos = estado
    ocupadas = negros | blancos
    for color, grupo in (("negro", negros), ("blanco", blancos)):
        for origen in grupo:
            for destino in saltos_validos(origen):
                if destino in ocupadas:
                    continue
                nuevo = (grupo - {origen}) | {destino}
                nuevo_estado = (nuevo, blancos) if color == "negro" else (negros, nuevo)
                yield nuevo_estado, (color, origen, destino)


def bfs(inicio, meta):
    cola = deque([inicio])
    padre = {inicio: None}          # estado -> (estado anterior, movimiento)
    explorados = 0

    while cola:
        estado = cola.popleft()
        explorados += 1
        if estado == meta:
            break
        for siguiente, movimiento in sucesores(estado):
            if siguiente not in padre:
                padre[siguiente] = (estado, movimiento)
                cola.append(siguiente)
    else:
        return None, explorados, len(padre)

    # Reconstruir el camino de la meta hacia atrás
    camino = []
    estado = meta
    while padre[estado] is not None:
        anterior, movimiento = padre[estado]
        camino.append((movimiento, estado))
        estado = anterior
    camino.reverse()
    return camino, explorados, len(padre)


def dibujar(estado, sangria="    "):
    negros, blancos = estado
    for f in range(N - 1, -1, -1):
        fila = []
        for c in range(N):
            if (c, f) in negros:
                fila.append(NEGRO)
            elif (c, f) in blancos:
                fila.append(BLANCO)
            else:
                fila.append(VACIA)
        print(f"{sangria}{f + 1} {' '.join(fila)}")
    print(f"{sangria}  {' '.join(chr(ord('a') + c) for c in range(N))}")


if __name__ == "__main__":
    negros = frozenset(a_coord(c) for c in NEGROS_INICIO)
    blancos = frozenset(a_coord(c) for c in BLANCOS_INICIO)
    inicio = (negros, blancos)
    meta = (blancos, negros)        # intercambiados

    print(f"Caballos negros ({NEGRO}): {NEGROS_INICIO}")
    print(f"Caballos blancos ({BLANCO}): {BLANCOS_INICIO}")
    print("\nEstado inicial:")
    dibujar(inicio)
    print("\nEstado meta:")
    dibujar(meta)

    print("\nBuscando con Primero en Anchura...")
    camino, explorados, generados = bfs(inicio, meta)

    if camino is None:
        print("No hay solución.")
    else:
        print(f"Estados explorados: {explorados}   Estados generados: {generados}")
        print(f"Solución con {len(camino)} movimientos:\n")
        for i, ((color, origen, destino), estado) in enumerate(camino, 1):
            print(f"Movimiento {i}: caballo {color} {a_nombre(origen)} -> {a_nombre(destino)}")
            dibujar(estado)
            print()
        print(f"¡Intercambio completado en {len(camino)} movimientos!")
