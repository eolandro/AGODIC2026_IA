import json

archivo = open("saltos.json")
saltos = json.load(archivo)
archivo.close()

letras = "abcdefgh"
numeros = "87654321"


def contar_libres(casilla, ruta):
    libres = 0
    for destino in saltos[casilla]:
        if destino not in ruta:
            libres = libres + 1
    return libres


def buscar_ruta(origen):
    pila = [[origen]]
    regresos = 0

    while len(pila) > 0:
        ruta = pila.pop()

        if len(ruta) == 64:
            return ruta, regresos

        ultima = ruta[len(ruta) - 1]
        opciones = []
        for destino in saltos[ultima]:
            if destino not in ruta:
                libres = contar_libres(destino, ruta + [destino])
                opciones.append([libres, destino])

        if len(opciones) == 0:
            regresos = regresos + 1
        else:
            opciones.sort(reverse=True)
            for op in opciones:
                pila.append(ruta + [op[1]])

    return None, regresos


def imprimir_coordenadas():
    print("     +" + "----" * 8 + "+")
    for n in numeros:
        renglon = "  " + n + "  |"
        for l in letras:
            renglon = renglon + " " + l + n + " "
        print(renglon + "|")
    print("     +" + "----" * 8 + "+")
    renglon = "      "
    for l in letras:
        renglon = renglon + l.rjust(3) + " "
    print(renglon)


def imprimir_pasos(ruta):
    turno = {}
    for i in range(len(ruta)):
        turno[ruta[i]] = i + 1

    print("     +" + "----" * 8 + "+")
    for n in numeros:
        renglon = "  " + n + "  |"
        for l in letras:
            renglon = renglon + str(turno[l + n]).rjust(3) + " "
        print(renglon + "|")
    print("     +" + "----" * 8 + "+")
    renglon = "      "
    for l in letras:
        renglon = renglon + l.rjust(3) + " "
    print(renglon)


print("==============================================")
print("   PROBLEMA DE LOS CABALLOS 2  EQUIPO NARANJA")
print("==============================================")
print("Coordenadas del tablero (letra = columna, numero = fila):")
imprimir_coordenadas()
print()

entrada = input("Coordenada inicial del caballo (ej. e4): ").strip().lower()
while entrada not in saltos:
    print("Coordenada no valida. Usa una letra de a-h y un numero de 1-8.")
    entrada = input("Coordenada inicial del caballo (ej. e4): ").strip().lower()

print()
print("El caballo inicia en", entrada)
print("Desde ahi puede saltar a:", ", ".join(saltos[entrada]))

ruta, regresos = buscar_ruta(entrada)

if ruta is None:
    print("No se encontro un recorrido completo")
else:
    print()
    print("Tablero (numero = paso en que se visito la casilla):")
    imprimir_pasos(ruta)

    print()
    print("Recorrido:")
    renglon = ""
    for i in range(len(ruta)):
        renglon = renglon + ruta[i]
        if i < len(ruta) - 1:
            renglon = renglon + " -> "
        if (i + 1) % 8 == 0:
            print(renglon)
            renglon = ""

    print()
    print("==============================================")
    print("Casillas visitadas:", len(ruta), "de 64")
    print("Regresos (backtracking):", regresos)
    print("==============================================")
