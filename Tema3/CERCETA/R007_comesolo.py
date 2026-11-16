"""R007 - Come Solo con tablero triangular de 15 casillas."""

# El tablero tiene 5 filas y 15 casillas en total.
CASILLAS = []
for fila in range(5):
    for columna in range(fila + 1):
        CASILLAS.append((fila, columna))

# Cada casilla tiene un numero del 1 al 15.
NUMEROS = {}
for i, casilla in enumerate(CASILLAS):
    NUMEROS[casilla] = i + 1

# Direcciones en las que una ficha puede saltar.
DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]


def mostrar_numeros():
    print("\nNUMEROS DE LAS CASILLAS:")
    for fila in range(5):
        espacios = " " * (3 * (4 - fila))
        linea = []
        for columna in range(fila + 1):
            linea.append(f" {NUMEROS[(fila, columna)]:02d} ")
        print(espacios + "  ".join(linea))


def mostrar_tablero(piezas):
    for fila in range(5):
        espacios = " " * (3 * (4 - fila))
        linea = []
        for columna in range(fila + 1):
            casilla = (fila, columna)
            simbolo = "O" if casilla in piezas else "."
            linea.append(f"{NUMEROS[casilla]:02d}:{simbolo}")
        print(espacios + "  ".join(linea))


def resolver(casilla_vacia):
    piezas = set(CASILLAS)
    piezas.remove(CASILLAS[casilla_vacia - 1])

    # Crear todos los saltos posibles en el triangulo.
    saltos = []
    for fila, columna in CASILLAS:
        for df, dc in DIRECCIONES:
            origen = (fila, columna)
            medio = (fila + df, columna + dc)
            destino = (fila + 2 * df, columna + 2 * dc)
            if medio in NUMEROS and destino in NUMEROS:
                saltos.append((origen, medio, destino))

    camino = []
    estados_revisados = set()

    def buscar():
        # La meta es dejar una sola ficha.
        if len(piezas) == 1:
            return True

        estado = frozenset(piezas)
        if estado in estados_revisados:
            return False

        for origen, medio, destino in saltos:
            if origen in piezas and medio in piezas and destino not in piezas:
                # Mover una ficha y quitar la que se salto.
                piezas.remove(origen)
                piezas.remove(medio)
                piezas.add(destino)
                camino.append((origen, medio, destino))

                if buscar():
                    return True

                # Si no resulta, deshacer el movimiento.
                camino.pop()
                piezas.remove(destino)
                piezas.add(origen)
                piezas.add(medio)

        estados_revisados.add(estado)
        return False

    if buscar():
        return camino
    return None


def main():
    print("COMESOLO - TABLERO TRIANGULAR")
    print("O = ficha     . = casilla vacia")
    mostrar_numeros()

    # El usuario elige que casilla empieza sin ficha.
    while True:
        entrada = input("\nElige la casilla vacia al inicio (1 al 15): ").strip()
        if entrada.isdigit() and 1 <= int(entrada) <= 15:
            casilla_vacia = int(entrada)
            break
        print("Escribe un numero del 1 al 15.")

    piezas = set(CASILLAS)
    piezas.remove(CASILLAS[casilla_vacia - 1])

    print("\nTABLERO INICIAL:")
    mostrar_tablero(piezas)
    print("Fichas que quedan:", len(piezas))

    camino = resolver(casilla_vacia)
    if camino is None:
        print("No se encontro una solucion.")
        return

    print("\nRECORRIDO PASO A PASO:")
    for numero_paso, (origen, medio, destino) in enumerate(camino, 1):
        print(f"\nMovimiento {numero_paso} de {len(camino)}:")
        print(f"Ficha que se mueve: casilla {NUMEROS[origen]}")
        print(f"Se mueve a: casilla {NUMEROS[destino]}")
        print(f"Se elimina la ficha de: casilla {NUMEROS[medio]}")

        piezas.remove(origen)
        piezas.remove(medio)
        piezas.add(destino)

        mostrar_tablero(piezas)
        print("Fichas que quedan:", len(piezas))

    print("\nRESULTADO FINAL: queda una sola ficha.")
    print("Ultima ficha en la casilla:", NUMEROS[next(iter(piezas))])
    print("Total de movimientos:", len(camino))


if __name__ == "__main__":
    main()
