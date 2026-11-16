import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")   # para la consola de Windows
except AttributeError:
    pass

PIEZA, VACIO = "●", "○"
FILAS = 5
TOTAL = FILAS * (FILAS + 1) // 2               # 15 agujeros

# Casillas como (fila, columna): fila f tiene f+1 agujeros
CASILLAS = [(f, c) for f in range(FILAS) for c in range(f + 1)]
INDICE = {pos: i for i, pos in enumerate(CASILLAS)}

# 6 direcciones: derecha, izquierda, abajo, arriba y las dos diagonales
DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]


def generar_saltos():
    """Lista de saltos posibles como (origen, comida, destino) en índices."""
    saltos = []
    for (f, c) in CASILLAS:
        for df, dc in DIRECCIONES:
            medio = (f + df, c + dc)
            destino = (f + 2 * df, c + 2 * dc)
            if medio in INDICE and destino in INDICE:
                saltos.append((INDICE[(f, c)], INDICE[medio], INDICE[destino]))
    return saltos


SALTOS = generar_saltos()


class Comesolo:
    def __init__(self):
        self.sin_salida = set()
        self.explorados = 0

    def resolver(self, estado, solucion):
        """DFS: regresa True si desde 'estado' se llega a 1 pieza."""
        if bin(estado).count("1") == 1:          # estado meta
            return True
        if estado in self.sin_salida:
            return False
        self.explorados += 1

        for origen, comida, destino in SALTOS:
            if (estado >> origen & 1) and (estado >> comida & 1) and not (estado >> destino & 1):
                nuevo = estado & ~(1 << origen) & ~(1 << comida) | (1 << destino)
                solucion.append((origen, comida, destino))
                if self.resolver(nuevo, solucion):
                    return True
                solucion.pop()                   # backtracking

        self.sin_salida.add(estado)
        return False


def dibujar(estado=None, numeros=False, marcar=()):
    for f in range(FILAS):
        linea = " " * (2 * (FILAS - f - 1))
        for c in range(f + 1):
            i = INDICE[(f, c)]
            if numeros:
                simbolo = f"{i + 1:>2}"
            else:
                simbolo = PIEZA if estado >> i & 1 else VACIO
                simbolo = f"[{simbolo}]" if i in marcar else f" {simbolo} "
            linea += f"{simbolo:^4}"
        print("    " + linea.rstrip())


if __name__ == "__main__":
    print("Comesolo - tablero triangular de 15 agujeros\n")
    print("Número de cada agujero:")
    dibujar(numeros=True)

    texto = input(f"\n¿Qué pieza falta? (1-{TOTAL}) [1]: ").strip()
    while texto and not (texto.isdigit() and 1 <= int(texto) <= TOTAL):
        texto = input(f"  Escribe un número del 1 al {TOTAL}: ").strip()
    hueco = (int(texto) if texto else 1) - 1

    inicio = ((1 << TOTAL) - 1) & ~(1 << hueco)  # todo lleno menos el hueco
    print("\nEstado inicial:")
    dibujar(inicio)

    print("\nBuscando solución...")
    juego = Comesolo()
    solucion = []
    if not juego.resolver(inicio, solucion):
        print(f"No hay forma de dejar una sola pieza empezando con el hueco {hueco + 1}.")
        sys.exit()

    print(f"¡Solución encontrada! {len(solucion)} saltos "
          f"(estados explorados: {juego.explorados})\n")
    estado = inicio
    for k, (o, m, d) in enumerate(solucion, 1):
        estado = estado & ~(1 << o) & ~(1 << m) | (1 << d)
        print(f"Salto {k}: la pieza {o + 1} salta sobre la {m + 1} y cae en {d + 1}")
        dibujar(estado, marcar=(d,))
        print()
    final = next(i for i in range(TOTAL) if estado >> i & 1)
    print(f"Queda una sola pieza, en el agujero {final + 1}. ¡Comesolo resuelto!")
