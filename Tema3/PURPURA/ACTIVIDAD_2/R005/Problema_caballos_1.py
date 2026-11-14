N = 3

NEGRO = "♘"
BLANCO = "♞"
VACIO = " "

# Anillo de casillas (fila, columna) que recorre el caballo en L,
# en el sentido de las manecillas del reloj
ANILLO = [(0, 0), (1, 2), (2, 0), (0, 1), (2, 2), (1, 0), (0, 2), (2, 1)]

# Caballos en el orden de turno: negro1, negro2, blanco1, blanco2
caballos = [
    {"nombre": "Negro 1",  "simbolo": NEGRO,  "pos": (0, 0)},
    {"nombre": "Negro 2",  "simbolo": NEGRO,  "pos": (0, 2)},
    {"nombre": "Blanco 1", "simbolo": BLANCO, "pos": (2, 0)},
    {"nombre": "Blanco 2", "simbolo": BLANCO, "pos": (2, 2)},
]


def construir_tablero():
    tablero = [[VACIO for _ in range(N)] for _ in range(N)]
    for c in caballos:
        f, col = c["pos"]
        tablero[f][col] = c["simbolo"]
    return tablero


def dibujar():
    tablero = construir_tablero()
    print("    ┌───┬───┬───┐")
    for i, fila in enumerate(tablero):
        print("    │" + "│".join(f" {x} " for x in fila) + "│")
        print("    ├───┼───┼───┤" if i < N - 1 else "    └───┴───┴───┘")


def esta_ocupada(pos):
    return any(c["pos"] == pos for c in caballos)


def es_solucion():
    """Blancos arriba (fila 0) y negros abajo (fila 2)."""
    for c in caballos:
        fila = c["pos"][0]
        if c["simbolo"] == BLANCO and fila != 0:
            return False
        if c["simbolo"] == NEGRO and fila != N - 1:
            return False
    return True


def main():
    print("=" * 40)
    print("  CABALLOS EN TABLERO 3x3")
    print("=" * 40)
    print("\nTablero inicial:")
    dibujar()

    paso = 0
    turno = 0
    sin_movimiento = 0

    while not es_solucion():
        c = caballos[turno % 4]
        i = ANILLO.index(c["pos"])
        destino = ANILLO[(i + 1) % len(ANILLO)]  # siguiente casilla en sentido horario

        if esta_ocupada(destino):
            print(f"\n{c['nombre']} no puede moverse (casilla ocupada), pasa el turno.")
            sin_movimiento += 1
            if sin_movimiento >= 4:
                print("Ningún caballo puede moverse. No hay solución.")
                return
        else:
            sin_movimiento = 0
            paso += 1
            origen = c["pos"]
            c["pos"] = destino
            print(f"\n[Paso {paso}] {c['nombre']} {c['simbolo']}: "
                  f"({origen[0] + 1},{origen[1] + 1}) -> ({destino[0] + 1},{destino[1] + 1})")
            dibujar()

        turno += 1

    print("\n" + "=" * 40)
    print(f"  ★ ¡SOLUCIÓN ENCONTRADA EN {paso} MOVIMIENTOS! ★")
    print("=" * 40)


if __name__ == "__main__":
    main()
