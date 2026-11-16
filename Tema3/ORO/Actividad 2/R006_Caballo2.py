import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")   # para la consola de Windows
except AttributeError:
    pass

sys.setrecursionlimit(10000)

SALTOS = [(1, 2), (2, 1), (2, -1), (1, -2),
          (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def a_nombre(coord):
    c, f = coord
    return f"{chr(ord('a') + c)}{f + 1}"


def a_coord(texto, n):
    """'b3' -> (1, 2); regresa None si no es válida."""
    texto = texto.strip().lower()
    if len(texto) < 2 or not texto[1:].isdigit():
        return None
    c, f = ord(texto[0]) - ord("a"), int(texto[1:]) - 1
    return (c, f) if 0 <= c < n and 0 <= f < n else None


class RecorridoCaballo:
    def __init__(self, n):
        self.n = n
        self.tablero = [[0] * n for _ in range(n)]   # 0 = no visitada, k = número de salto
        self.recorrido = []
        self.retrocesos = 0

    def libres(self, c, f):
        """Saltos válidos desde (c, f) a casillas no visitadas."""
        for dc, df in SALTOS:
            nc, nf = c + dc, f + df
            if 0 <= nc < self.n and 0 <= nf < self.n and self.tablero[nf][nc] == 0:
                yield nc, nf

    def grado(self, c, f):
        """Cuántas salidas libres tiene una casilla (para Warnsdorff)."""
        return sum(1 for _ in self.libres(c, f))

    def resolver(self, c, f, paso=1):
        self.tablero[f][c] = paso
        self.recorrido.append((c, f))

        if paso == self.n * self.n:                  # estado meta
            return True

        # Warnsdorff: primero la casilla con menos salidas
        candidatos = sorted(self.libres(c, f), key=lambda p: self.grado(*p))
        for nc, nf in candidatos:
            if self.resolver(nc, nf, paso + 1):
                return True

        # Callejón sin salida: backtracking
        self.tablero[f][c] = 0
        self.recorrido.pop()
        self.retrocesos += 1
        return False

    def dibujar(self):
        ancho = len(str(self.n * self.n))
        linea = "   +" + ("-" * (ancho + 2) + "+") * self.n
        print(linea)
        for f in range(self.n - 1, -1, -1):
            celdas = "|".join(f" {self.tablero[f][c]:>{ancho}} " for c in range(self.n))
            print(f"{f + 1:>2} |{celdas}|")
            print(linea)
        letras = "".join(f"{chr(ord('a') + c):^{ancho + 3}}" for c in range(self.n))
        print(f"    {letras}")


def pedir_n():
    texto = input("Tamaño del tablero [8]: ").strip()
    while texto and (not texto.isdigit() or int(texto) < 1):
        texto = input("  Escribe un número entero mayor que 0: ").strip()
    return int(texto) if texto else 8


if __name__ == "__main__":
    n = pedir_n()
    entrada = input(f"Casilla de entrada del caballo (a1 - {chr(ord('a') + n - 1)}{n}) [a1]: ")
    inicio = a_coord(entrada, n) if entrada.strip() else (0, 0)
    while inicio is None:
        inicio = a_coord(input("  Casilla no válida, intenta de nuevo: "), n)

    juego = RecorridoCaballo(n)
    print(f"\nEl caballo entra en {a_nombre(inicio)} en un tablero de {n}x{n}...\n")

    if juego.resolver(*inicio):
        print("Recorrido (orden de las casillas visitadas):")
        for i in range(0, len(juego.recorrido), 8):
            tramo = juego.recorrido[i:i + 8]
            print("  " + " -> ".join(f"{i + j + 1}:{a_nombre(p)}" for j, p in enumerate(tramo)))

        print("\nTablero (cada número es el salto en que se visitó la casilla):")
        juego.dibujar()
        print(f"\n¡Recorrido completo! {n * n} casillas visitadas, "
              f"{juego.retrocesos} retrocesos.")
    else:
        print(f"No existe recorrido completo desde {a_nombre(inicio)} en {n}x{n}.")
