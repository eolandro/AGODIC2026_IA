# R005 - Problema de las N reinas (4 reinas en un tablero de 4x4)
# Q = reina, x = casilla atacada (ya no se puede usar), . = casilla libre

N = 4

reinas = []       
soluciones = []   
pasos = 0


def esta_atacada(lista, fila, col):
    for f, c in lista:
        if f == fila or c == col or abs(f - fila) == abs(c - col):
            return True
    return False


def mostrar_tablero(lista):
    for fila in range(N):
        linea = ""
        for col in range(N):
            if (fila, col) in lista:
                linea = linea + " Q "
            elif esta_atacada(lista, fila, col):
                linea = linea + " x "
            else:
                linea = linea + " . "
        print(linea)
    print()


def coordenadas(lista):
    texto = ""
    for fila, col in lista:
        texto = texto + "(" + str(fila + 1) + "," + str(col + 1) + ") "
    return texto


def buscar(inicio):
    global pasos

    if len(reinas) == N:
        soluciones.append(list(reinas))
        print("*** SOLUCIÓN", len(soluciones), "***\n")
        return

    for casilla in range(inicio, N * N):
        fila = casilla // N
        col = casilla % N

        if not esta_atacada(reinas, fila, col):
            reinas.append((fila, col))
            pasos = pasos + 1
            print("Paso", pasos)
            mostrar_tablero(reinas)

            buscar(casilla + 1)

            reinas.pop()


print("PROBLEMA DE LAS", N, "REINAS\n")
buscar(0)

print("==============================")
print("SOLUCIONES ENCONTRADAS:", len(soluciones))
print("==============================\n")
for numero in range(len(soluciones)):
    print("Solución", numero + 1)
    print(coordenadas(soluciones[numero]))
    mostrar_tablero(soluciones[numero])
