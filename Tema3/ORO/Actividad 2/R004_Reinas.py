import sys

# Para que la consola de Windows muestre bien la reina y los acentos
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

VACIA = "·"
REINA = "♛"


def es_segura(reinas, fila, columna):
    """True si una reina en (fila, columna) no es atacada por las ya puestas."""
    for f, c in enumerate(reinas):
        if c == columna:
            return False                       # misma columna
        if abs(c - columna) == abs(f - fila):
            return False                       # misma diagonal
    return True                                # la fila nunca choca: una reina por fila


def dibujar(reinas, n, sangria="    "):
    letras = " ".join(chr(ord("a") + i) for i in range(n))
    print(f"{sangria}  {letras}")
    for fila in range(n):
        celdas = [REINA if fila < len(reinas) and reinas[fila] == col else VACIA
                  for col in range(n)]
        print(f"{sangria}{fila + 1} {' '.join(celdas)}")


class NReinas:
    def __init__(self, n, mostrar_pasos=True):
        self.n = n
        self.mostrar_pasos = mostrar_pasos
        self.soluciones = []
        self.pasos = 0
        self.retrocesos = 0

    def log(self, texto, reinas=None):
        if self.mostrar_pasos:
            print(texto)
            if reinas is not None:
                dibujar(reinas, self.n)

    def resolver(self, reinas=None):
        if reinas is None:
            reinas = []
        fila = len(reinas)

        if fila == self.n:                     # estado meta
            self.soluciones.append(reinas.copy())
            self.log(f"  >>> ¡Solución {len(self.soluciones)} encontrada! {self.posiciones(reinas)}")
            return

        for columna in range(self.n):
            self.pasos += 1
            casilla = f"{chr(ord('a') + columna)}{fila + 1}"
            if es_segura(reinas, fila, columna):
                reinas.append(columna)
                self.log(f"Paso {self.pasos}: pongo reina en {casilla}", reinas)
                self.resolver(reinas)
                reinas.pop()                   # backtracking: se quita para probar otra
                self.retrocesos += 1
                self.log(f"  <- quito la reina de {casilla} y regreso")
            else:
                self.log(f"Paso {self.pasos}: {casilla} está atacada, no se puede")

    @staticmethod
    def posiciones(reinas):
        return [f"{chr(ord('a') + c)}{f + 1}" for f, c in enumerate(reinas)]


def pedir_n():
    texto = input("¿Cuántas reinas? [4]: ").strip()
    while texto and (not texto.isdigit() or int(texto) < 1):
        texto = input("  Escribe un número entero mayor que 0: ").strip()
    return int(texto) if texto else 4


if __name__ == "__main__":
    n = pedir_n()
    # Con muchas reinas el paso a paso sería enorme, así que solo se muestra hasta 6
    mostrar = n <= 6
    if not mostrar:
        print("(Con más de 6 reinas se omite el paso a paso y solo se dan resultados)")

    print(f"\nResolviendo {n} reinas en un tablero de {n}x{n}\n")
    juego = NReinas(n, mostrar_pasos=mostrar)
    juego.resolver()

    print("\n" + "=" * 40)
    print(f"Casillas probadas: {juego.pasos}   Retrocesos: {juego.retrocesos}")
    print(f"Soluciones encontradas: {len(juego.soluciones)}")
    for i, sol in enumerate(juego.soluciones[:5], 1):
        print(f"\nSolución {i}: {NReinas.posiciones(sol)}")
        dibujar(sol, n)
    if len(juego.soluciones) > 5:
        print(f"\n... y {len(juego.soluciones) - 5} soluciones más")
