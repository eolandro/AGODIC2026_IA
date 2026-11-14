import json
import sys

COLUMNAS = "abcdefgh"
FILAS = "12345678"

sys.setrecursionlimit(10000)


def cargar_movimientos(ruta="movimientos_caballo.json"):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def grado(casilla, movimientos, visitadas):
    """Cuántas salidas libres tiene una casilla (casillas aún no visitadas)."""
    return sum(1 for d in movimientos[casilla] if d not in visitadas)


def recorrer(casilla, movimientos, visitadas, camino):
    """Backtracking guiado por la regla de Warnsdorff:
    primero intenta ir a la casilla con MENOS salidas libres."""
    if len(camino) == 64:
        return True

    candidatos = [d for d in movimientos[casilla] if d not in visitadas]
    candidatos.sort(key=lambda d: grado(d, movimientos, visitadas))

    for siguiente in candidatos:
        visitadas.add(siguiente)
        camino.append(siguiente)
        if recorrer(siguiente, movimientos, visitadas, camino):
            return True
        # No funcionó: deshacer y probar otra opción
        visitadas.remove(siguiente)
        camino.pop()
    return False


def imprimir_tablero(camino):
    paso = {casilla: i + 1 for i, casilla in enumerate(camino)}
    print("\n     a   b   c   d   e   f   g   h")
    print("   +" + "---+" * 8)
    for fila in reversed(FILAS):  # la fila 8 arriba, como en el tablero real
        linea = f" {fila} |"
        for col in COLUMNAS:
            linea += f"{paso[col + fila]:>3}|"
        print(linea + f" {fila}")
        print("   +" + "---+" * 8)
    print("     a   b   c   d   e   f   g   h")


def main():
    movimientos = cargar_movimientos()

    while True:
        inicio = input("¿En qué casilla entra el caballo? (ej. a1, d4): ").strip().lower()
        if inicio in movimientos:
            break
        print("Casilla no válida. Usa una letra a-h y un número 1-8.")

    visitadas = {inicio}
    camino = [inicio]

    if recorrer(inicio, movimientos, visitadas, camino):
        print(f"\nRecorrido completo desde {inicio} ({len(camino)} casillas):\n")
        for i, casilla in enumerate(camino, start=1):
            print(f"{i:>2}. {casilla}", end="   ")
            if i % 8 == 0:
                print()
        print("\nRecorrido en orden:")
        print(" -> ".join(camino))
        imprimir_tablero(camino)
    else:
        print("No se encontró un recorrido completo desde esa casilla.")


if __name__ == "__main__":
    main()
