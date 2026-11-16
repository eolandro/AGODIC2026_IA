import argparse
import json
import os
import sys
import time

N = 8
COLUMNAS = "ABCDEFGH"
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_MOV = os.path.join(CARPETA, "movimientos.json")
ARCHIVO_REC = os.path.join(CARPETA, "recorridos.json")
sys.setrecursionlimit(10000)


# ---------------------------------------------------------------- precómputo
def generar_movimientos():
    saltos = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
    mov = {}
    for f in range(N):
        for c in range(N):
            destinos = [f"{COLUMNAS[c + dc]}{f + df + 1}"
                        for dc, df in saltos
                        if 0 <= c + dc < N and 0 <= f + df < N]
            mov[f"{COLUMNAS[c]}{f + 1}"] = sorted(destinos)
    return mov


def cargar_movimientos():
    try:
        with open(ARCHIVO_MOV, encoding="utf-8") as f:
            datos = json.load(f)
        if set(datos) == set(generar_movimientos()):
            return datos
    except (OSError, ValueError):
        pass
    datos = generar_movimientos()
    with open(ARCHIVO_MOV, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2)
    return datos


MOVIMIENTOS = cargar_movimientos()


# --------------------------------------------------------------- backtracking
def libres(casilla, visitadas):
    return [h for h in MOVIMIENTOS[casilla] if h not in visitadas]


def dist_centro(casilla):
    c = COLUMNAS.index(casilla[0])
    f = int(casilla[1]) - 1
    return (c - 3.5) ** 2 + (f - 3.5) ** 2


def hijos(casilla, visitadas):
    """Optimización (Warnsdorff): menos salidas primero; en empate, la más
    alejada del centro. Así el caballo casi nunca necesita retroceder."""
    return sorted(libres(casilla, visitadas),
                  key=lambda h: (len(libres(h, visitadas)), -dist_centro(h)))


def resolver(casilla, visitadas, camino, eventos=None):
    camino.append(casilla)
    visitadas.add(casilla)
    opciones = hijos(casilla, visitadas)
    if eventos is not None:
        eventos.append(("avanza", casilla, list(camino), opciones))
    if len(camino) == N * N:
        return True
    for h in opciones:
        if resolver(h, visitadas, camino, eventos):
            return True
    # Backtracking: sin salida, regresar y probar otro hijo
    camino.pop()
    visitadas.remove(casilla)
    if eventos is not None:
        eventos.append(("retrocede", casilla, list(camino), []))
    return False


def recorrido(inicio, eventos=None):
    camino = []
    return camino if resolver(inicio, set(), camino, eventos) else None


def generar_recorridos():
    return {c: recorrido(c) for c in MOVIMIENTOS}


def cargar_recorridos():
    try:
        with open(ARCHIVO_REC, encoding="utf-8") as f:
            datos = json.load(f)
        if set(datos) == set(MOVIMIENTOS) and all(len(v) == N * N for v in datos.values()):
            return datos
    except (OSError, ValueError):
        pass
    datos = generar_recorridos()
    with open(ARCHIVO_REC, "w", encoding="utf-8") as f:
        json.dump(datos, f)
    return datos


# ------------------------- pantalla
def tablero_texto(camino):
    """Tablero 8x8: número de paso en cada casilla, [n] = donde está el caballo."""
    paso = {c: i + 1 for i, c in enumerate(camino)}
    actual = camino[-1] if camino else None
    lineas = ["      " + "    ".join(COLUMNAS)]
    for f in range(N, 0, -1):
        celdas = []
        for c in COLUMNAS:
            casilla = f"{c}{f}"
            if casilla not in paso:
                celdas.append("  . ")
            elif casilla == actual:
                celdas.append(f"[{paso[casilla]:2d}]")
            else:
                celdas.append(f" {paso[casilla]:2d} ")
        lineas.append(f" {f}   " + " ".join(celdas))
    return "\n".join(lineas)


def imprimir_evento(num, total, ev):
    tipo, casilla, camino, opciones = ev
    print("=" * 52)
    if tipo == "avanza":
        print(f"Evento {num}/{total} | Paso {len(camino)}: el caballo está en {casilla}")
        print(f"Posibles movimientos (hijos): {', '.join(opciones) if opciones else 'ninguno'}")
        if not opciones and len(camino) < N * N:
            print("Sin salida -> BACKTRACKING")
    else:
        print(f"Evento {num}/{total} | BACKTRACKING: se regresa desde {casilla}")
        print(f"Vuelve a {camino[-1]} y prueba otro hijo")
    print(tablero_texto(camino))
    sys.stdout.flush()


def imprimir_resultado(camino):
    print("\n" + "#" * 52)
    print(f"RECORRIDO COMPLETO desde {camino[0]} ({len(camino)} casillas)\n")
    for i in range(len(camino) - 1):
        print(f"{i + 1:2d}. {camino[i]},{camino[i + 1]}")
    print("\nCamino:", " -> ".join(camino))
    print("\nTablero final:\n")
    print(tablero_texto(camino).replace("[", " ").replace("]", " "))


# ---------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Problema de los caballos 2 ")
    ap.add_argument("--duracion", type=float, default=60.0,
                    help="segundos que dura la animación del backtracking (default 60)")
    ap.add_argument("--rapido", action="store_true", help="sin animación ni espera")
    args = ap.parse_args()

    print("=== PROBLEMA DE LOS CABALLOS 2 (tablero 8x8) ===")

    while True:
        inicio = (input("Casilla inicial (A1-H8) [A1]: ").strip() or "A1").upper()
        while inicio not in MOVIMIENTOS:
            inicio = input("Casilla inválida. Usa letra A-H y número 1-8: ").strip().upper()

        if args.rapido:
            imprimir_resultado(cargar_recorridos()[inicio])
        else:
            eventos = []
            camino = recorrido(inicio, eventos)
            if camino is None:
                print("No se encontró recorrido completo.")
            else:
                espera = max(args.duracion, 0) / len(eventos)
                print(f"\nBacktracking: {len(eventos)} eventos, {args.duracion:.0f} s en total "
                      f"({espera:.2f} s por tablero)\n")
                for i, ev in enumerate(eventos, 1):
                    imprimir_evento(i, len(eventos), ev)
                    time.sleep(espera)
                imprimir_resultado(camino)

        if input("\n¿Quieres seguir jugando? (s/n): ").strip().lower() not in ("s", "si", "sí"):
            break


if __name__ == "__main__":
    main()
