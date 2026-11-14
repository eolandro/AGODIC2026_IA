import json
import os
import sys
import time

N = 8
MOVIMIENTOS = [[1, 2], [2, 1], [-1, 2], [-2, 1], [1, -2], [2, -1], [-1, -2], [-2, -1]]

sys.setrecursionlimit(10000)

def indice(casilla):
    casilla = str(casilla).strip().upper()
    if len(casilla) < 2 or not casilla[0].isalpha() or not casilla[1:].isdigit():
        raise ValueError("\nEscribe la casilla en coordenadas de ajedrez, por ejemplo A1 o E4")
    col = ord(casilla[0]) - ord("A")
    fila = int(casilla[1:]) - 1
    if col < 0 or col >= N or fila < 0 or fila >= N:
        raise ValueError("\nLa casilla " + casilla + " no existe en un tablero de " + str(N) + "x" + str(N))
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
        print("Tabla de saltos cargada de", archivo_saltos)
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

def salidas_libres(casilla, visitado):
    total = 0
    for d in SALTOS[casilla]:
        if not visitado[d]:
            total = total + 1
    return total

def ordenar_opciones(casilla, visitado, optimizado):
    opciones = []
    for d in SALTOS[casilla]:
        if not visitado[d]:
            opciones.append(d)
    if optimizado:
        opciones.sort(key=lambda d: salidas_libres(d, visitado))
    return opciones

def backtracking(casilla, camino, visitado, optimizado, contador):
    if len(camino) == N * N:
        return True
    for d in ordenar_opciones(casilla, visitado, optimizado):
        visitado[d] = True
        camino.append(d)
        if backtracking(d, camino, visitado, optimizado, contador):
            return True
        camino.pop()               
        visitado[d] = False
        contador[0] = contador[0] + 1
    return False

def dibujar(camino):
    numero = [0] * (N * N)
    for paso in range(len(camino)):
        numero[camino[paso]] = paso + 1
    print("     +" + "----" * N + "+")
    for fila in range(N - 1, -1, -1):
        linea = ""
        for col in range(N):
            valor = numero[fila * N + col]
            if valor == 0:
                linea = linea + "   ."
            else:
                linea = linea + str(valor).rjust(4)
        print("   " + str(fila + 1) + " |" + linea + "|")
    print("     +" + "----" * N + "+")
    print("      " + "".join(chr(ord("A") + c).rjust(4) for c in range(N)))

def recorrido(casilla="A1", optimizado=True):
    inicio = indice(casilla)
    print()
    print("\nRecorrido del caballo en un tablero de", str(N) + "x" + str(N),
          "empezando en", nombre(inicio))
    if optimizado:
        print("\nBacktracking con la regla de Warnsdorff")
    else:
        print("\nBacktracking puro (puede tardar horas; Ctrl+C para cancelar)")

    visitado = [False] * (N * N)
    visitado[inicio] = True
    camino = [inicio]
    contador = [0]

    t0 = time.time()
    try:
        encontrado = backtracking(inicio, camino, visitado, optimizado, contador)
    except KeyboardInterrupt:
        print()
        print("\nBusqueda cancelada despues de", contador[0], "retrocesos")
        return False
    tiempo = time.time() - t0

    print("\nTiempo de busqueda:", round(tiempo, 3), "segundos")
    print("Retrocesos (caminos malos descartados):", contador[0])
    print()

    if not encontrado:
        print("\nNo hay recorrido completo desde", nombre(inicio))
        return False

    print("\nRecorrido completo (" + str(len(camino)) + " casillas):")
    for k in range(len(camino)):
        texto = str(k + 1).rjust(2) + ". " + nombre(camino[k])
        if k % 8 == 7 or k == len(camino) - 1:
            print("  " + texto)
        else:
            print("  " + texto.ljust(8), end="")
    print()
    print("\nTablero numerado (el numero indica en que paso paso el caballo por la casilla):")
    dibujar(camino)
    return True

def consola():
    print()
    print("\nModo consola: recorrido(casilla, optimizado)  y  ver_saltos(casilla)")
    print('\nEjemplos:  recorrido("A1")   recorrido("E4")   recorrido("A1", False)   ver_saltos("A2")')
    print("\nEscribe S para volver al menu")

    funciones = {"recorrido": recorrido, "ver_saltos": ver_saltos}
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
            print("Error:", error)

def pedir_casilla():
    while True:
        dato = input("Casilla inicial en coordenadas de ajedrez (por ejemplo A1): ").strip()
        try:
            indice(dato)
            return dato.upper()
        except ValueError as error:
            print("\n  ", error)

def menu():
    print("\n" + "=" * 62)
    print("     CABALLOS 2: RECORRIDO DEL CABALLO EN TABLERO DE", str(N) + "x" + str(N))
    print("=" * 62)
    while True:
        print()
        print("\n1. Recorrer el tablero (backtracking + regla de Warnsdorff)")
        print("2. Recorrer el tablero con backtracking puro (muy lento)")
        print("3. Consultar a donde salta el caballo desde una casilla")
        print("4. Modo consola (escribir la funcion)")
        print("0. Salir")
        opcion = input("\nOpcion: ").strip()
        if opcion == "1":
            recorrido(pedir_casilla(), True)
        elif opcion == "2":
            recorrido(pedir_casilla(), False)
        elif opcion == "3":
            try:
                casilla = pedir_casilla()
                print("\nDesde", casilla, "salta a:", ", ".join(ver_saltos(casilla)))
            except Exception as error:
                print("\n  Casilla no valida:", error)
        elif opcion == "4":
            consola()
        elif opcion == "0":
            break
        else:
            print("\nOpcion no valida")

if __name__ == "__main__":
    menu()