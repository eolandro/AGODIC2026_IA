def conflicto(tablero, fila, col):
    for f in range(len(tablero)):
        c = tablero[f]
        if c == col:
            return "misma columna que la reina de la fila " + str(f + 1)
        if abs(c - col) == abs(f - fila):
            return "misma diagonal que la reina de la fila " + str(f + 1)
    return None

def dibujar(tablero):
    n = len(tablero)
    for f in range(n):
        linea = ""
        for c in range(n):
            if tablero[f] == c:
                linea = linea + " Q"
            else:
                linea = linea + " ."
        print("     " + linea)

def colocar(fila, n, tablero, soluciones, traza, todas):
    sangria = ""
    if traza:
        sangria = "  " * fila          

    if fila == n:                             
        soluciones.append(list(tablero))
        columnas = []
        for c in tablero:
            columnas.append(c + 1)
        print(sangria + "Solucion", len(soluciones), "-> columnas por fila:", columnas)
        if traza:
            dibujar(tablero)
        return not todas

    for col in range(n):
        motivo = conflicto(tablero, fila, col)
        if motivo is None:
            if traza:
                print(sangria + "Fila", fila + 1, "columna", col + 1, "-> libre, se coloca la reina")
            tablero.append(col)
            if colocar(fila + 1, n, tablero, soluciones, traza, todas):
                return True
            tablero.pop()                      
        else:
            if traza:
                print(sangria + "Fila", fila + 1, "columna", col + 1, "-> choca,", motivo)

    if traza and fila > 0:
        print(sangria + "Fila", fila + 1, "sin columnas libres, se regresa a la fila", fila)
    return False

def reinas(n=4, traza=True, todas=True):
    if n < 1:
        print("\nEl tablero debe tener al menos 1 casilla")
        return 0
    print()
    print("\nProblema de las", n, "reinas (traza:", traza, "- todas las soluciones:", todas, ")")
    print("-" * 70)
    soluciones = []
    colocar(0, n, [], soluciones, traza, todas)
    print("-" * 70)
    if len(soluciones) == 0:
        print("\nEl tablero de", n, "x", n, "no tiene solucion")
    else:
        print("\nSoluciones encontradas:", len(soluciones))
    return len(soluciones)

def pedir_numero(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato.isdigit() and int(dato) > 0:
            return int(dato)
        print("  Escribe un numero entero mayor que 0")

def pedir_si_no(mensaje):
    while True:
        dato = input(mensaje + " (s/n): ").strip().lower()
        if dato == "s" or dato == "n":
            return dato == "s"
        print("  Responde s o n")

def consola():
    print()
    print("\nModo consola: reinas(n, traza, todas)")
    print('\nEjemplos:  reinas()   reinas(4, True, False)   reinas(6, False)')
    print("\nEscribe S para volver al menu")

    funciones = {"reinas": reinas}
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

def menu():
    print("\n" + "=" * 62)
    print("                  PROBLEMA DE LAS N REINAS")
    print("=" * 62)
    while True:
        print()
        print("1. Resolver 4 reinas con traza (el caso del enunciado)")
        print("2. Elegir el numero de reinas y las opciones")
        print("3. Modo consola (escribir la funcion)")
        print("0. Salir")
        opcion = input("\nOpcion: ").strip()
        if opcion == "1":
            reinas(4, True, True)
        elif opcion == "2":
            n = pedir_numero("\nNumero de reinas: ")
            traza = pedir_si_no("\nMostrar cada intento y retroceso (con mas de 6 reinas es muy largo)")
            todas = pedir_si_no("\nBuscar todas las soluciones (n = no, se detiene en la primera)")
            reinas(n, traza, todas)
        elif opcion == "3":
            consola()
        elif opcion == "0":
            break
        else:
            print("\nOpcion no valida")

if __name__ == "__main__":
    menu()