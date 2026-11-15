ciclo = [(0, 0), (1, 2), (2, 0), (0, 1), (2, 2), (1, 0), (0, 2), (2, 1)]

def imprimir_tablero(posiciones):
    tablero = [["", "", ""], ["", "", ""], ["", "", ""]]
    for nombre, indice in posiciones.items():
        fila, columna = ciclo[indice]
        tablero[fila][columna] = nombre
    linea = "+-----+-----+-----+"
    print(linea)
    for fila in tablero:
        print("| " + " | ".join(f"{celda:<3}" for celda in fila) + " |")
        print(linea)

# CN = caballo negro, CB = caballo blanco.
posiciones = {
    "CN1": ciclo.index((0, 0)),
    "CN2": ciclo.index((0, 2)),
    "CB1": ciclo.index((2, 0)),
    "CB2": ciclo.index((2, 2)),
}

lugares_negros = {posiciones["CN1"], posiciones["CN2"]}
lugares_blancos = {posiciones["CB1"], posiciones["CB2"]}

# ---------------- MAIN ----------------
print("* * * PROBLEMA DE LOS CABALLOS 1 * * *")
print("Los caballos negros (CN) y blancos (CB) deben intercambiar sus lugares.\n")
print("Estado inicial:")
imprimir_tablero(posiciones)

print("\nElige la dirección de la rotación:")
print("1) En dirección de las manecillas del reloj ->")
print("2) En contra de las manecillas del reloj <-")
opción = input("Opción: ")
while opción != "1" and opción != "2":
    opción = input("Opción inválida, escribe 1 o 2: ")
if opción == "1":
    salto = 1      # hacia adelante en el círculo
else:
    salto = -1     # hacia atrás en el círculo

movimiento = 0
intercambiados = False
while not intercambiados:
    for nombre in posiciones:
        movimiento += 1
        origen = ciclo[posiciones[nombre]]
        posiciones[nombre] = (posiciones[nombre] + salto) % len(ciclo)
        destino = ciclo[posiciones[nombre]]
        print(f"\nMovimiento {movimiento}: {nombre} ({origen[0] + 1},{origen[1] + 1}) -> ({destino[0] + 1},{destino[1] + 1})")
        imprimir_tablero(posiciones)
        negros_actualizados = {posiciones["CN1"], posiciones["CN2"]}
        blancos_actualizados = {posiciones["CB1"], posiciones["CB2"]}
        intercambiados = (negros_actualizados == lugares_blancos and blancos_actualizados == lugares_negros)
        if intercambiados:
            break

print(f"\n¡Listo! Los caballos intercambiaron sus lugares en {movimiento} movimientos.")