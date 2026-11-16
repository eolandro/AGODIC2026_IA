import heapq

# Orden fijo de movimientos (fila, columna). Es tambien el ultimo desempate.
# mov(arriba, -1, 0). mov(abajo, 1, 0). mov(izq, 0, -1). mov(der, 0, 1).
MOVS = [
    ("arriba", (-1, 0)),
    ("abajo",  ( 1, 0)),
    ("izq",    ( 0, -1)),
    ("der",    ( 0, 1)),
]

#manhattan(A,B,H) :- H is |Fa - Fb| + |Ca - Cb|.
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

#buscar_simbolo(Tablero, S, Pos) :- member(Fila, Tablero), member(S, Fila).
def buscar_simbolo(tablero, simbolo):
    return [
        (f, c)
        for f, fila in enumerate(tablero)
        for c, e in enumerate(fila)
        if e == simbolo
    ]

#libre(Tablero, (F,C)) :- dentro del tablero, y la casilla no es "X".
def libre(tablero, pos):
    f, c = pos
    return (
        0 <= f < len(tablero)
        and 0 <= c < len(tablero[f])
        and tablero[f][c] != "X"
    )

#vecinos(Tablero, Pos, Mov, Nueva) :- mov(Mov, D), suma(Pos, D, Nueva), libre(Tablero, Nueva).
def vecinos(tablero, pos):
    f, c = pos
    return [
        (mov, (f + df, c + dc))
        for mov, (df, dc) in MOVS
        if libre(tablero, (f + df, c + dc))
    ]

#reconstruir: sigue los padres desde la meta hasta el inicio y devuelve los movimientos
def reconstruir(padre, pos):
    match padre.get(pos):
        case None:
            return []
        case (anterior, mov):
            return reconstruir(padre, anterior) + [mov]

#A*: f = g + h, g = pasos desde el inicio (cada paso cuesta 1), h = Manhattan a la meta.
#Desempates: menor f, luego menor h (la casilla mas cercana a la bomba),
#luego el orden de MOVS (arriba, abajo, izq, der).
def buscar(tablero, inicio, meta):
    h0 = manhattan(inicio, meta)
    abiertos = [(h0, h0, 0, inicio)]   # (f, h, orden de insercion, posicion)
    g = {inicio: 0}
    padre = {}
    cerrados = set()
    orden = 0
    while abiertos:
        _, _, _, actual = heapq.heappop(abiertos)
        if actual in cerrados:
            continue
        if actual == meta:
            return (True, reconstruir(padre, meta))
        cerrados.add(actual)
        for mov, sig in vecinos(tablero, actual):
            nuevo_g = g[actual] + 1
            if sig in cerrados or nuevo_g >= g.get(sig, float("inf")):
                continue
            g[sig] = nuevo_g
            padre[sig] = (actual, mov)
            h = manhattan(sig, meta)
            orden += 1
            heapq.heappush(abiertos, (nuevo_g + h, h, orden, sig))
    return (False, "Boome no puede llegar a la bomba: los bloqueos la aislan")
