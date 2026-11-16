N = 4                  
POR_RENGLON = 4         
def esta_atacada(tablero, fila, col):
    for f in range(N):
        c = tablero[f]
        if c == -1:                    
            continue
        if f == fila:                   
            return True
        if c == col:                    
            return True
        if fila - f == col - c:         
            return True
        if fila - f == c - col:       
            return True
    return False
def texto_fila(tablero, fila):
    linea = ""
    for col in range(N):
        if tablero[fila] == col:
            linea = linea + "R "
        elif esta_atacada(tablero, fila, col):
            linea = linea + "X "
        else:
            linea = linea + ". "
    return linea
def contar_disponibles(tablero):
    total = 0
    for fila in range(N):
        if tablero[fila] != -1:        
            continue
        for col in range(N):
            if not esta_atacada(tablero, fila, col):
                total = total + 1
    return total
def fila_vacia(tablero):
    for fila in range(N):
        if tablero[fila] == -1:
            return fila
    return -1   
def buscar_desde(fila_inicio, col_inicio):
    inicio = [-1, -1, -1, -1]
    inicio[fila_inicio] = col_inicio
    pila = [inicio]
    while len(pila) > 0:
        tablero = pila.pop()        

        fila = fila_vacia(tablero)
        if fila == -1:                  
            return tablero
        hijos = []
        for col in range(N):
            if not esta_atacada(tablero, fila, col):
                nuevo = []
                for x in tablero:      
                    nuevo.append(x)
                nuevo[fila] = col   
                hijos.append(nuevo)
        for h in hijos:
            pila.append(h)
    return None                 
def proceso_solucion(solucion, fila_inicio):
    tablero = [-1, -1, -1, -1]
    tablero[fila_inicio] = solucion[fila_inicio]
    proceso = []
    while True:
        copia = []
        for x in tablero:
            copia.append(x)
        proceso.append(copia)
        fila = fila_vacia(tablero)
        if fila == -1:                 
            return proceso
        tablero[fila] = solucion[fila] 
def imprimir_proceso(proceso):
    total = len(proceso)
    for inicio in range(0, total, POR_RENGLON):
        grupo = proceso[inicio:inicio + POR_RENGLON]
        linea = ""
        for i in range(len(grupo)):
            linea = linea + ("Reina " + str(inicio + i + 1)).ljust(14)
        print(linea)
        for fila in range(N):
            linea = ""
            for i in range(len(grupo)):
                tablero = grupo[i]
                linea = linea + texto_fila(tablero, fila)
                ultimo = (inicio + i == total - 1)
                if fila == 1 and not ultimo:
                    linea = linea + " ->   "
                else:
                    linea = linea + "      "
            print(linea)
        linea = ""
        for i in range(len(grupo)):
            if inicio + i == total - 1:
                estado = "SOLUCION"
            else:
                estado = "Disp: " + str(contar_disponibles(grupo[i]))
            linea = linea + estado.ljust(14)
        print(linea)
print("==============================================")
print("       PROBLEMA DE LAS 4 REINAS  EQUIPO NARANJA")
print("==============================================")
print("R = reina   X = casilla atacada   . = casilla disponible")
print("\n Tablero principal:")
print("         Col 1  Col 2  Col 3  Col 4")
for fila in range(N):
    linea = "Fila " + str(fila + 1) + "  "
    for col in range(N):
        linea = linea + "     . "
    print(linea)
calculos = 0
soluciones = []
for casilla in range(1, N * N + 1):
    fila = (casilla - 1) // N
    col = (casilla - 1) % N
    solucion = buscar_desde(fila, col)
    calculos = calculos + 1
    if solucion is not None and solucion not in soluciones:
        soluciones.append(solucion)
print("Casillas calculadas:", calculos)
print("Soluciones encontradas:", len(soluciones))
for i in range(len(soluciones)):
    s = soluciones[i]
    posiciones = ""
    for f in range(N):
        posiciones = posiciones + "(" + str(f + 1) + "," + str(s[f] + 1) + ") "
    print("==============================================")
    print("SOLUCION", i + 1)
    print("Reinas en (fila,columna):", posiciones)
    print("==============================================")
    imprimir_proceso(proceso_solucion(s, 0))
