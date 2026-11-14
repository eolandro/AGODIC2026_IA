DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]
N = 5

CELDAS = [(r, c) for r in range(N) for c in range(r + 1)]
INDICE = {p: i for i, p in enumerate(CELDAS)}
TOTAL = len(CELDAS)  # 15

def generar_saltos():
    """Todos los saltos posibles geométricamente: (origen, medio, destino)."""
    saltos = []
    for (r, c) in CELDAS:
        for dr, dc in DIRECCIONES:
            m = (r + dr, c + dc)
            d = (r + 2 * dr, c + 2 * dc)
            if m in INDICE and d in INDICE:
                saltos.append((INDICE[(r, c)], INDICE[m], INDICE[d]))
    return saltos

SALTOS = generar_saltos()
def mostrar(estado, numerado=False):
    ancho = len(str(TOTAL))
    for r in range(N):
        fila = []
        for c in range(r + 1):
            i = INDICE[(r, c)]
            if numerado:
                fila.append(str(i + 1).rjust(ancho))
            else:
                fila.append(("O" if (estado >> i) & 1 else ".").rjust(ancho))
        print(" " * ((N - r - 1) * (ancho + 1) // 2) + " ".join(fila))
    print()


def resolver(hueco):
    """Devuelve (estado_inicial, camino) o (estado_inicial, None) si no hay solución."""
    inicial = ((1 << TOTAL) - 1) & ~(1 << hueco)
    visitados = set()
    camino = []

    def dfs(estado):
        if bin(estado).count("1") == 1:
            return True
        if estado in visitados:
            return False
        visitados.add(estado)

        for o, m, d in SALTOS:
            if (estado >> o) & 1 and (estado >> m) & 1 and not (estado >> d) & 1:
                nuevo = (estado & ~(1 << o) & ~(1 << m)) | (1 << d)
                camino.append((o, m, d))
                if dfs(nuevo):
                    return True
                camino.pop()
        return False
    return inicial, (camino if dfs(inicial) else None)

def pedir_entero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
        except ValueError:
            pass
        print(f"Ingresa un número entre {minimo} y {maximo}.")

def main():
    print("=== COME SOLO (tablero triangular 5x5x5) ===\n")
    print("Posiciones del tablero:\n")
    mostrar(0, numerado=True)

    hueco = pedir_entero(f"¿Qué posición estará vacía al inicio (1-{TOTAL})? ",1, TOTAL) - 1
    inicial, camino = resolver(hueco)

    if camino is None:
        print("\nNo existe solución con esa posición vacía.")
        return
    print("\nTablero inicial (O = ficha, . = vacío):\n")
    mostrar(inicial)
    estado = inicial
    for k, (o, m, d) in enumerate(camino, 1):
        estado = (estado & ~(1 << o) & ~(1 << m)) | (1 << d)
        print(f"Movimiento {k}: la ficha {o + 1} salta sobre {m + 1} y cae en {d + 1}")
        mostrar(estado)
    print(f"¡Resuelto en {len(camino)} movimientos! Queda 1 ficha.")

if __name__ == "__main__":
    main()