# caballos2.py
# Problema de los caballos 2: un caballo entra a un tablero de 8x8 vacío y debe
# visitar TODAS las casillas exactamente una vez.
# Se imprime solo el tablero final, enumerado en el orden de visita.
#
# Algoritmo elegido: BACKTRACKING ORDENADO POR LA HEURÍSTICA DE WARNSDORFF.
#   - Warnsdorff: desde la casilla actual, probar primero el destino que tenga MENOS
#     salidas libres. Así se visitan primero las casillas "difíciles" (esquinas y
#     bordes) antes de que se queden aisladas.
#   - Backtracking: si aun así se llega a un callejón sin salida, se retrocede y se
#     prueba la siguiente opción. Esto garantiza encontrar solución desde cualquier
#     casilla inicial (Warnsdorff solo, sin retroceso, no lo garantiza).
#   Justificación: en la práctica Warnsdorff casi nunca se equivoca, por lo que el
#   backtracking casi no retrocede y la respuesta es instantánea, en vez de explorar
#   miles de millones de caminos como haría un backtracking sin orden.
#   Optimización sugerida por el profesor: los movimientos se PRECOMPUTAN una vez.
#   Además, las casillas visitadas se guardan como un entero (máscara de bits) 
#   y contar salidas libres sea muy barato.

N = 8                                   # tablero de N x N
COLUMNAS = "ABCDEFGH"                   # columnas (x) en notación de ajedrez

# Los 8 saltos posibles de un caballo: (delta_columna, delta_fila)
DELTAS = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))


# ---------------------------------------------------------------------------
# NÚCLEO FUNCIONAL
# ---------------------------------------------------------------------------

def a_nombre(indice):
    """Casilla (entero 0..63) -> notación de ajedrez. Ej: 0 -> 'A1', 9 -> 'B2'."""
    return COLUMNAS[indice % N] + str(indice // N + 1)


def a_indice(texto):
    """Notación de ajedrez -> entero 0..63, o None si no es una casilla válida.
    Usa match/case para 'unificar' la cadena con el patrón [columna, fila]."""
    match list(texto.strip().upper()):
        case [columna, fila] if columna in COLUMNAS and fila in "12345678":
            return (int(fila) - 1) * N + COLUMNAS.index(columna)
        case _:
            return None


def saltos_desde(indice):
    """Casillas a las que un caballo puede saltar desde 'indice' (tablero vacío)."""
    columna, fila = indice % N, indice // N
    return tuple(
        nueva_fila * N + nueva_columna
        for dc, df in DELTAS
        for nueva_columna, nueva_fila in [(columna + dc, fila + df)]
        if 0 <= nueva_columna < N and 0 <= nueva_fila < N
    )


# PRECÓMPUTO: casilla -> casillas destino, y lo mismo como máscara de bits
MOVIMIENTOS = tuple(saltos_desde(i) for i in range(N * N))
MASCARAS = tuple(sum(1 << d for d in destinos) for destinos in MOVIMIENTOS)


def salidas_libres(casilla, visitadas):
    """Cuántos destinos sin visitar tiene 'casilla' (el 'grado' de Warnsdorff).
    Con máscaras: AND entre sus vecinos y las NO visitadas, y se cuentan los bits."""
    return (MASCARAS[casilla] & ~visitadas).bit_count()


def recorrer(camino, visitadas):
    """Backtracking. 'camino' es la tupla de casillas en orden de visita y
    'visitadas' su máscara de bits. Devuelve el recorrido completo, o None si esta
    rama no lleva a ninguna solución.
    Equivale a: recorrer(Camino) :- completo(Camino), !.
                recorrer(Camino) :- siguiente(Camino, Nuevo), recorrer([Nuevo|Camino]).
    Nada se muta: cada llamada recibe un camino y una máscara NUEVOS, así que
    'retroceder' es simplemente regresar de la llamada recursiva."""
    if len(camino) == N * N:                                   # caso base: tablero completo
        return camino
    actual = camino[-1]
    # Destinos libres ordenados por Warnsdorff (menos salidas primero)
    candidatas = sorted(
        (d for d in MOVIMIENTOS[actual] if not (visitadas >> d) & 1),
        key=lambda d: salidas_libres(d, visitadas),
    )
    # Se prueba cada candidata en orden; la primera rama que devuelva solución gana.
    # (next + generador = "el primer elemento que cumpla", sin ciclos explícitos)
    return next(
        (r for d in candidatas
         if (r := recorrer(camino + (d,), visitadas | (1 << d))) is not None),
        None,
    )


def dibujar(camino):
    """Tablero en texto con el número de visita en cada casilla (fila 8 arriba)."""
    orden = {casilla: numero for numero, casilla in enumerate(camino, start=1)}
    filas = [
        f"{fila + 1} | " + " ".join(f"{orden[fila * N + c]:2}" for c in range(N))
        for fila in reversed(range(N))
    ]
    pie = ["  +" + "-" * (3 * N), "    " + "  ".join(COLUMNAS)]
    return "\n".join(filas + pie)


# ---------------------------------------------------------------------------
# ENTRADA / SALIDA 
# ---------------------------------------------------------------------------

def pedir_casilla(mensaje):
    """Pide la casilla inicial por input hasta que sea válida (A1..H8)."""
    while True:
        indice = a_indice(input(mensaje))
        if indice is not None:
            return indice
        print("  Casilla inválida. Usa notación de ajedrez, de A1 a H8.")


def main():
    print(f"Problema de los caballos 2 (tablero {N}x{N}): recorrido completo.")
    inicio = pedir_casilla("¿En qué casilla inicia el caballo? ")
    camino = recorrer((inicio,), 1 << inicio)
    # Sobre un tablero 8x8 siempre existe recorrido desde cualquier casilla, pero se
    # valida igualmente para no imprimir basura si algo cambiara (p. ej. otro N).
    if camino is None:
        print("No existe un recorrido completo desde esa casilla.")
        return
    print(f"\nRecorrido completo desde {a_nombre(inicio)} (número = orden de visita):\n")
    print(dibujar(camino))


if __name__ == "__main__":
    main()
