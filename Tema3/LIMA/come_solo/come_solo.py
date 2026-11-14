import sys

FILAS = 5
N = FILAS * (FILAS + 1) // 2 

coord = []          
indice = {}        
for f in range(FILAS):
    for c in range(f + 1):
        indice[(f, c)] = len(coord)
        coord.append((f, c))

DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]
SALTOS = []

for i, (f, c) in enumerate(coord):
    for df, dc in DIRECCIONES:
        medio = (f + df, c + dc)
        destino = (f + 2 * df, c + 2 * dc)
        if medio in indice and destino in indice:
            SALTOS.append((i, indice[medio], indice[destino]))

def resolver(hoyo_vacio):
    inicio = ((1 << N) - 1) & ~(1 << hoyo_vacio)
    sin_salida = set()
    camino = []

    def dfs(tablero, piezas):
        if piezas == 1:
            return True
        if tablero in sin_salida:
            return False
        for a, b, d in SALTOS:
            if (tablero >> a) & 1 and (tablero >> b) & 1 and not (tablero >> d) & 1:
                nuevo = tablero & ~(1 << a) & ~(1 << b) | (1 << d)
                camino.append((a, b, d))
                if dfs(nuevo, piezas - 1):
                    return True
                camino.pop()
        sin_salida.add(tablero)
        return False

    if dfs(inicio, N - 1):
        return [(a + 1, b + 1, d + 1) for a, b, d in camino]
    return None

def dibujar(tablero, movida=None):
    lineas = []
    for f in range(FILAS):
        fila = []
        for c in range(f + 1):
            i = indice[(f, c)]
            if i == movida:
                fila.append("◉")
            elif (tablero >> i) & 1:
                fila.append("●")
            else:
                fila.append("○")
        lineas.append("  " * (FILAS - 1 - f) + "   ".join(fila))
    return "\n".join(lineas)

def mostrar_solucion(hoyo, movimientos):
    tablero = ((1 << N) - 1) & ~(1 << (hoyo - 1))
    print("\nSimbología:  ● pieza   ○ hoyo vacío   ◉ pieza que se acaba de mover")
    print(f"\nTablero inicial (hoyo {hoyo} vacío, {N - 1} piezas):\n")
    print(dibujar(tablero))

    for paso, (a, b, d) in enumerate(movimientos, 1):
        tablero = tablero & ~(1 << (a - 1)) & ~(1 << (b - 1)) | (1 << (d - 1))
        piezas = N - 1 - paso
        print(f"\nMovimiento {paso:2d}: la pieza del hoyo {a} salta sobre el {b}, "
              f"cae en el {d} y se come la pieza del {b}.")
        print(dibujar(tablero, movida=d - 1))

    print("\n" + "=" * 60)
    print(f"SOLUCIÓN (camino correcto) con el hoyo {hoyo} vacío al inicio:")
    print("=" * 60)
    for paso, (a, b, d) in enumerate(movimientos, 1):
        print(f"  {paso:2d}.  {a:2d} → {d:2d}   (come la pieza del {b})")
    ultimo = movimientos[-1][2]
    print(f"\n¡Resuelto en {len(movimientos)} movimientos! "
          f"Queda una sola pieza, en el hoyo {ultimo}.")

def leer_hoyo(texto):
    while True:
        try:
            valor = int(input(texto))
            if 1 <= valor <= N:
                return valor
        except ValueError:
            pass
        print(f"  Escribe un número entre 1 y {N}.")

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    print("\n *** COMESOLO - TABLERO TRIANGULAR DE 15 HOYOS ***\n")
    print("=" * 53)
    print("            Así están numerados los hoyos:\n         ")
    print("                         1                           ")
    print("                       2   3                         ")
    print("                     4   5   6                       ")
    print("                   7   8   9  10                     ")
    print("                11  12  13  14  15\n                 ")
    print("=" * 53)

    args = sys.argv[1:]
    if args:
        try:
            hoyo = int(args[0])
        except ValueError:
            sys.exit("El argumento debe ser un número del 1 al 15.")
        if not 1 <= hoyo <= N:
            sys.exit("Los hoyos van del 1 al 15.")
    else:
        hoyo = leer_hoyo("\n¿Qué hoyo está vacío al inicio? (1-15): ")

    movimientos = resolver(hoyo - 1)
    if movimientos is None:
        print(f"\nNo existe solución empezando con el hoyo {hoyo} vacío.")
    else:
        mostrar_solucion(hoyo, movimientos)
    
if __name__ == "__main__":
    main()
