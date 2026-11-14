import json
import os
import time
from collections import deque
from math import comb

MOVIMIENTOS = [[1, 2], [2, 1], [-1, 2], [-2, 1], [1, -2], [2, -1], [-1, -2], [-2, -1]]

with open("caballos_datos.json", encoding="utf-8") as archivo:
    datos = json.load(archivo)

N = datos["tablero"]

def indice(casilla):
    col = ord(casilla[0].upper()) - ord("A")
    fila = int(casilla[1:]) - 1
    if col < 0 or col >= N or fila < 0 or fila >= N:
        raise ValueError("La casilla " + casilla + " no existe en un tablero de " + str(N) + "x" + str(N))
    return fila * N + col

def nombre(num):
    return chr(ord("A") + num % N) + str(num // N + 1)

def calcular_saltos(n):
    tabla = []
    for fila in range(n):
        for col in range(n):
            destinos = []
            for df, dc in MOVIMIENTOS:
                nf = fila + df
                nc = col + dc
                if 0 <= nf < n and 0 <= nc < n:
                    destinos.append(nf * n + nc)
            tabla.append(destinos)
    return tabla

def cargar_saltos(n):
    archivo_saltos = "saltos_" + str(n) + "x" + str(n) + ".json"
    if os.path.exists(archivo_saltos):
        with open(archivo_saltos, encoding="utf-8") as f:
            tabla = json.load(f)
        print("\nTabla de saltos cargada de", archivo_saltos)
    else:
        tabla = calcular_saltos(n)
        with open(archivo_saltos, "w", encoding="utf-8") as f:
            json.dump(tabla, f)
        print("\nTabla de saltos calculada y guardada en", archivo_saltos)
    return tabla

SALTOS = cargar_saltos(N)

def ver_saltos(casilla):
    destinos = []
    for d in SALTOS[indice(casilla)]:
        destinos.append(nombre(d))
    return destinos

NOMBRES_CUADRANTES = ["abajo-izquierda", "arriba-izquierda", "arriba-derecha", "abajo-derecha"]

def cuadrante(num):
    fila = num // N
    col = num % N
    arriba = fila >= N / 2
    derecha = col >= N / 2
    if not arriba and not derecha:
        return 0
    if arriba and not derecha:
        return 1
    if arriba and derecha:
        return 2
    return 3

def movimiento_permitido(origen, destino, sentido):
    q1 = cuadrante(origen)
    q2 = cuadrante(destino)
    if q1 == q2:
        return True
    if sentido == "horario":
        return q2 == (q1 + 1) % 4
    return q2 == (q1 - 1) % 4

def normalizar(n1, n2, b1, b2):
    if n1 > n2:
        n1, n2 = n2, n1
    if b1 > b2:
        b1, b2 = b2, b1
    return (n1, n2, b1, b2)

def dibujar(estado):
    for fila in range(N - 1, -1, -1):
        linea = ""
        for col in range(N):
            num = fila * N + col
            if num in estado[:2]:
                linea = linea + "N "
            elif num in estado[2:]:
                linea = linea + "B "
            else:
                linea = linea + ". "
        print("    " + str(fila + 1) + " " + linea)
    print("      " + " ".join(chr(ord("A") + c) for c in range(N)))

def describir_movimiento(anterior, nuevo):
    negros_antes = set(anterior[:2])
    negros_ahora = set(nuevo[:2])
    if negros_antes != negros_ahora:
        color = "negro"
        salida = (negros_antes - negros_ahora).pop()
        llegada = (negros_ahora - negros_antes).pop()
    else:
        color = "blanco"
        salida = (set(anterior[2:]) - set(nuevo[2:])).pop()
        llegada = (set(nuevo[2:]) - set(anterior[2:])).pop()
    return ("caballo " + color + " " + nombre(salida) + " -> " + nombre(llegada)
            + "   (" + NOMBRES_CUADRANTES[cuadrante(salida)] + " -> "
            + NOMBRES_CUADRANTES[cuadrante(llegada)] + ")")

def buscar(inicio, meta, sentido):
    padres = {inicio: None}
    cola = deque([inicio])
    while len(cola) > 0:
        estado = cola.popleft()
        if estado == meta:
            return estado, padres
        for i in range(4):
            for destino in SALTOS[estado[i]]:
                if destino in estado:                 
                    continue
                if not movimiento_permitido(estado[i], destino, sentido):
                    continue
                lista = list(estado)
                lista[i] = destino
                nuevo = normalizar(lista[0], lista[1], lista[2], lista[3])
                if nuevo not in padres:
                    padres[nuevo] = estado
                    cola.append(nuevo)
    return None, padres

def leer_sentido(sentido):
    sentido = str(sentido).strip().lower()
    if sentido in ("h", "horario"):
        return "horario"
    if sentido in ("a", "antihorario"):
        return "antihorario"
    raise ValueError("\nEl sentido debe ser 'horario' o 'antihorario'")

def caballos(sentido="horario", tableros=False):
    sentido = leer_sentido(sentido)
    inicio = normalizar(indice(datos["negros"][0]), indice(datos["negros"][1]),
                        indice(datos["blancos"][0]), indice(datos["blancos"][1]))
    meta = (inicio[2], inicio[3], inicio[0], inicio[1])

    print()
    print("\nNegros en", nombre(inicio[0]), nombre(inicio[1]),
          "- Blancos en", nombre(inicio[2]), nombre(inicio[3]))
    print("\nMeta: negros en", nombre(meta[0]), nombre(meta[1]),
          "- blancos en", nombre(meta[2]), nombre(meta[3]))
    print("\nSentido de giro:", sentido)
    print()
    dibujar(inicio)
    print()

    t0 = time.time()
    final, padres = buscar(inicio, meta, sentido)
    tiempo = time.time() - t0

    posibles = comb(N * N, 2) * comb(N * N - 2, 2)
    print("\nPosiciones exploradas:", len(padres), "de", posibles, "posibles")
    print("\nTiempo de busqueda:", round(tiempo, 2), "segundos")
    print()

    if final is None:
        print("\nNo hay solucion girando en sentido", sentido)
        return 0

    camino = []
    estado = final
    while estado is not None:
        camino.append(estado)
        estado = padres[estado]
    camino.reverse()

    print("\nSolucion en sentido", sentido, "en", len(camino) - 1, "movimientos:")
    for k in range(1, len(camino)):
        print(" ", str(k).rjust(2) + ".", describir_movimiento(camino[k - 1], camino[k]))
        if tableros:
            dibujar(camino[k])
            print()
    if not tableros:
        print()
        dibujar(final)
    return len(camino) - 1

def consola():
    print()
    print("\nModo consola: caballos(sentido, tableros)  y  ver_saltos(casilla)")
    print('\nEjemplos:  caballos("horario")   caballos("antihorario", True)   ver_saltos("B3")')
    print("\nEscribe S para volver al menu")

    funciones = {"caballos": caballos, "ver_saltos": ver_saltos}
    while True:
        comando = input(">").strip()
        if comando == "":
            continue
        if comando.upper() == "S":
            break
        try:
            resultado = eval(comando, {"__builtins__": {}}, funciones)
            print(resultado)
        except Exception as error:
            print("\nError:", error)

def pedir_sentido():
    while True:
        dato = input("\nSentido horario (h) o antihorario (a): ").strip().lower()
        try:
            return leer_sentido(dato)
        except ValueError:
            print("\n  Responde h o a")

def pedir_si_no(mensaje):
    while True:
        dato = input(mensaje + " (s/n): ").strip().lower()
        if dato == "s" or dato == "n":
            return dato == "s"
        print("\n  Responde s o n")

def menu():
    print("\n","=" * 62)
    print("        CABALLOS 1: INTERCAMBIO EN TABLERO DE", str(N) + "x" + str(N))
    print("=" * 62)
    while True:
        print()
        print("\n1. Resolver el intercambio (eligiendo horario o antihorario)")
        print("2. Consultar a donde salta un caballo desde una casilla")
        print("3. Modo consola (escribir la funcion)")
        print("0. Salir")
        opcion = input("\nOpcion: ").strip()
        if opcion == "1":
            sentido = pedir_sentido()
            tableros = pedir_si_no("\nDibujar el tablero en cada movimiento")
            caballos(sentido, tableros)
        elif opcion == "2":
            casilla = input("\nCasilla (por ejemplo B3): ").strip()
            try:
                print("\nDesde", casilla.upper(), "salta a:", ", ".join(ver_saltos(casilla)))
            except Exception as error:
                print("\n  Casilla no valida:", error)
        elif opcion == "3":
            consola()
        elif opcion == "0":
            break
        else:
            print("\nOpcion no valida")

if __name__ == "__main__":
    menu()