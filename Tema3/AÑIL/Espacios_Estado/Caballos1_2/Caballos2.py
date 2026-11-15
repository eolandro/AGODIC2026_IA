Tamaño_tablero = 8
Letras_coordenadas = "ABCDEFGH"
# Los 8 saltos posibles de un caballo: (cambio de fila, cambio de columna)
SALTOS = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

def nombre_casilla(fila, columna):
    return Letras_coordenadas[columna] + str(fila + 1) #Convierte (fila, columna) internas a notación de ajedrez

def saltos_posibles(tablero, fila, columna):
    casillas = []
    for cambio_fila, cambio_columna in SALTOS:
        nueva_fila = fila + cambio_fila
        nueva_columna = columna + cambio_columna
        dentro = 0 <= nueva_fila < Tamaño_tablero and 0 <= nueva_columna < Tamaño_tablero
        if dentro and tablero[nueva_fila][nueva_columna] == 0:
            casillas.append((nueva_fila, nueva_columna))
    return casillas

def recorrer(tablero, fila, columna, numero_salto):
    tablero[fila][columna] = numero_salto
    if numero_salto == Tamaño_tablero * Tamaño_tablero:   # caso base: ya se visitaron todas
        return True
    # Regla de Warnsdorff: ordenar las opciones por cuántas salidas les quedan
    opciones = []
    for nueva_fila, nueva_columna in saltos_posibles(tablero, fila, columna):
        salidas = len(saltos_posibles(tablero, nueva_fila, nueva_columna))
        opciones.append((salidas, nueva_fila, nueva_columna))
    opciones.sort()
    for salidas, nueva_fila, nueva_columna in opciones:
        if recorrer(tablero, nueva_fila, nueva_columna, numero_salto + 1):
            return True
    tablero[fila][columna] = 0               # retroceder (backtrack)
    return False

# ---------------- MAIN ----------------
print("* * * PROBLEMA DE LOS CABALLOS 2 * * *")
print("El caballo debe recorrer las 64 casillas del tablero sin repetir ninguna.\n")

entrada = input("Casilla donde entra el caballo (letra A-H y número 1-8): ").strip().upper()
while len(entrada) != 2 or entrada[0] not in Letras_coordenadas or entrada[1] not in "12345678":
    entrada = input("Casilla inválida, escribe una letra de A a H y un número de 1 a 8 (ejemplo D4): ").strip().upper()

columna_inicial = Letras_coordenadas.index(entrada[0])
fila_inicial = int(entrada[1]) - 1

print(f"\nEl caballo entra en la casilla {entrada}.\n")
tablero = [[0] * Tamaño_tablero for _ in range(Tamaño_tablero)]
encontrado = recorrer(tablero, fila_inicial, columna_inicial, 1)

if not encontrado:
    print("No existe un recorrido completo desde esta casilla.")
else:
    # Ordenar las casillas según el número de salto para reconstruir el recorrido
    recorrido = [None] * (Tamaño_tablero * Tamaño_tablero)
    for fila in range(Tamaño_tablero):
        for columna in range(Tamaño_tablero):
            recorrido[tablero[fila][columna] - 1] = (fila, columna)

    print("Recorrido del caballo:")
    for numero, (fila, columna) in enumerate(recorrido, start=1):
        print(f"  Salto {numero:>2}: {nombre_casilla(fila, columna)}")

    print("\nTablero con el orden en que el caballo visitó cada casilla:")
    encabezado = "   " + "".join(f"  {letra}  " for letra in Letras_coordenadas)
    linea = "  +" + "----+" * Tamaño_tablero
    print(encabezado)
    print(linea)
    for fila in range(Tamaño_tablero - 1, -1, -1):   # la fila 8 se imprime arriba y la 1 abajo
        celdas = " | ".join(f"{numero:>2}" for numero in tablero[fila])
        print(f"{fila + 1} | {celdas} | {fila + 1}")
        print(linea)
    print(encabezado)

    print(f"\n¡Listo! El caballo recorrió las {Tamaño_tablero * Tamaño_tablero} casillas sin repetir ninguna.")