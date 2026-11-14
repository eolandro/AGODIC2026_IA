
posiciones = []
for fila in range(5):
    for columna in range(fila + 1):
        posiciones.append((fila, columna))
indice = {}
for i in range(len(posiciones)):
    indice[posiciones[i]] = i
movimientos = []
direcciones = [
    (0, 1), (0, -1),
    (1, 0), (-1, 0),
    (1, 1), (-1, -1)
]
for fila, columna in posiciones:
    for df, dc in direcciones:
        medio = (fila + df, columna + dc)
        destino = (fila + 2 * df, columna + 2 * dc)
        if medio in indice and destino in indice:
            movimientos.append((
                indice[(fila, columna)],
                indice[medio],
                indice[destino]
            ))
def buscar(estado):
    if estado & (estado - 1) == 0:
        return []
    for origen, medio, destino in movimientos:
        pieza1 = 1 << origen
        pieza2 = 1 << medio
        pieza3 = 1 << destino
        if (estado & pieza1 and estado & pieza2
                and not estado & pieza3):
            nuevo_estado = estado ^ pieza1 ^ pieza2 ^ pieza3
            resultado = buscar(nuevo_estado)
            if resultado is not None:
                return [(origen, medio, destino)] + resultado
    return None
def mostrar(estado):
    numero = 0
    for fila in range(5):
        print(" " * (4 - fila), end=" ")
        for columna in range(fila + 1):
            posicion = indice[(fila, columna)]
            if estado & (1 << posicion):
                print(" O", end=" ")
            else:
                print(" .", end=" ")
            numero += 1
        print()

def main():
    print("=== JUEGO COME SOLO ===")
    print("Tablero triangular de 15 posiciones")
    print()
    numero = 1
    for fila in range(5):
        print(" " * (4 - fila), end=" ")
        for columna in range(fila + 1):
            print("%2d" % numero, end=" ")
            numero += 1
        print()
    try:
        vacio = int(input("\nQue posicion quieres dejar vacia (1-15): "))
        if vacio < 1 or vacio > 15:
            print("El numero debe estar entre 1 y 15")
            return
    except ValueError:
        print("Debes escribir un numero entero")
        return
    estado = (1 << 15) - 1
    estado = estado ^ (1 << (vacio - 1))
    print("\nTablero inicial:")
    mostrar(estado)
    print("\nBuscando una solucion...")
    solucion = buscar(estado)
    if solucion is None:
        print("No se encontro una solucion")
        return
    print("\nSolucion encontrada")
    print("Total de movimientos:", len(solucion))
    numero = 1
    for origen, medio, destino in solucion:
        estado = estado ^ (1 << origen)
        estado = estado ^ (1 << medio)
        estado = estado ^ (1 << destino)
        print("\nMovimiento", numero)
        print("Mover pieza de", origen + 1,"a la posicion", destino + 1)
        print("Se quita la pieza", medio + 1)
        mostrar(estado)
        numero += 1
    print("\nJuego terminado")
    print("Piezas restantes:", bin(estado).count("1"))
main()
