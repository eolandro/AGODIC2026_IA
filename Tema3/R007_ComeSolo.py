FILAS = 5
TOTAL_POSICIONES = 15

def crear_coordenadas():
    """Crea las coordenadas de las 15 posiciones."""
    coordenadas = []
    for fila in range(FILAS):
        for columna in range(fila + 1):
            coordenadas.append((fila, columna))
    return coordenadas
coordenadas = crear_coordenadas()

def obtener_coordenada(posicion):
    """Devuelve la coordenada de una posición."""
    return coordenadas[posicion]

def obtener_posicion(coordenada):
    """Busca el número de una coordenada triangular."""
    posicion = 0
    while posicion < len(coordenadas):
        if coordenadas[posicion] == coordenada:
            return posicion
        posicion = posicion + 1
    return -1

def crear_movimientos():
    """Crea los saltos posibles según la forma del tablero."""
    direcciones = [
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 0),
        (1, 0),
        (1, 1)
    ]
    movimientos = []
    origen = 0

    while origen < len(coordenadas):
        fila = coordenadas[origen][0]
        columna = coordenadas[origen][1]
        for direccion in direcciones:
            cambio_fila = direccion[0]
            cambio_columna = direccion[1]
            fila_intermedia = fila + cambio_fila
            columna_intermedia = columna + cambio_columna
            fila_destino = fila + 2 * cambio_fila
            columna_destino = columna + 2 * cambio_columna
            coordenada_intermedia = (fila_intermedia, columna_intermedia)
            coordenada_destino = (fila_destino, columna_destino)
            intermedia = obtener_posicion(coordenada_intermedia)
            destino = obtener_posicion(coordenada_destino)
            if intermedia != -1 and destino != -1:
                movimiento = [origen, intermedia, destino]
                movimientos.append(movimiento)
        origen = origen + 1
    return movimientos
movimientos = crear_movimientos()

def contar_fichas(tablero):
    """Cuenta cuantas fichas hay en el tablero."""
    fichas = 0
    for valor in tablero:
        if valor == 1:
            fichas = fichas + 1
    return fichas

def movimiento_es_valido(tablero, movimiento):
    """Comprueba si un movimiento se puede realizar."""
    origen = movimiento[0]
    intermedia = movimiento[1]
    destino = movimiento[2]
    if tablero[origen] == 1:
        if tablero[intermedia] == 1:
            if tablero[destino] == 0:
                return True
    return False

def obtener_movimientos_validos(tablero):
    """Devuelve los movimientos válidos para el estado actual."""
    validos = []
    for movimiento in movimientos:
        if movimiento_es_valido(tablero, movimiento):
            validos.append(movimiento)
    return validos

def hacer_movimiento(tablero, movimiento):
    """Realiza un salto en el tablero."""
    origen = movimiento[0]
    intermedia = movimiento[1]
    destino = movimiento[2]
    tablero[origen] = 0
    tablero[intermedia] = 0
    tablero[destino] = 1

def deshacer_movimiento(tablero, movimiento):
    """Deshace un salto para probar otra opción."""
    origen = movimiento[0]
    intermedia = movimiento[1]
    destino = movimiento[2]
    tablero[origen] = 1
    tablero[intermedia] = 1
    tablero[destino] = 0

def resolver(tablero, camino, estadisticas):
    """Busca una solución usando backtracking.
    La función se llama a sí misma para continuar con el siguiente salto.
    Si una opción no funciona, deshace el movimiento y prueba otra.
    """
    estadisticas[0] = estadisticas[0] + 1
    if contar_fichas(tablero) == 1:
        return True
    movimientos_validos = obtener_movimientos_validos(tablero)
    for movimiento in movimientos_validos:
        hacer_movimiento(tablero, movimiento)
        camino.append(movimiento)
        solucion_encontrada = resolver(tablero, camino, estadisticas)
        if solucion_encontrada:
            return True
        camino.pop()
        deshacer_movimiento(tablero, movimiento)
        estadisticas[1] = estadisticas[1] + 1
    return False

def crear_tablero(posicion_vacia):
    """Crea un tablero con 14 fichas y un espacio vacío."""
    tablero = []
    for posicion in range(TOTAL_POSICIONES):
        if posicion == posicion_vacia:
            tablero.append(0)
        else:
            tablero.append(1)
    return tablero

def mostrar_tablero(tablero):
    """Imprime el tablero con forma triangular."""
    posicion = 0
    for fila in range(FILAS):
        espacios = " " * ((FILAS - fila - 1) * 2)
        texto_fila = ""
        for columna in range(fila + 1):
            texto_fila = texto_fila + str(tablero[posicion])
            if columna < fila:
                texto_fila = texto_fila + "   "
            posicion = posicion + 1
        print(espacios + texto_fila)

def mostrar_posiciones():
    """Imprime los números de las posiciones del tablero."""
    tablero_numeros = []
    for posicion in range(TOTAL_POSICIONES):
        tablero_numeros.append(posicion)
    print("Tablero de posiciones:")
    mostrar_tablero(tablero_numeros)

def mostrar_movimiento(numero, movimiento, tablero):
    """Imprime un movimiento y el tablero resultante."""
    origen = movimiento[0]
    intermedia = movimiento[1]
    destino = movimiento[2]
    print("Movimiento", numero)
    print("Origen:", origen, obtener_coordenada(origen))
    print("Ficha saltada:", intermedia, obtener_coordenada(intermedia))
    print("Destino:", destino, obtener_coordenada(destino))
    mostrar_tablero(tablero)

def pedir_posicion_vacia():
    """Solicita una posición y revisa que sea válida."""
    posicion_correcta = False
    posicion = 0
    while posicion_correcta is False:
        entrada = input("Indica la posición vacía inicial (0-14): ")
        try:
            posicion = int(entrada)
            if posicion >= 0 and posicion < TOTAL_POSICIONES:
                posicion_correcta = True
            else:
                print("La posición debe estar entre 0 y 14.")
        except ValueError:
            print("Escribe un número entero entre 0 y 14.")
    return posicion

def ejecutar():
    """Ejecuta el programa completo."""
    mostrar_posiciones()
    posicion_vacia = pedir_posicion_vacia()
    tablero = crear_tablero(posicion_vacia)
    camino = []
    estadisticas = [0, 0]
    print("\nTablero inicial:")
    mostrar_tablero(tablero)
    print("Posición vacía:", posicion_vacia,
          obtener_coordenada(posicion_vacia))
    print("Fichas iniciales:", contar_fichas(tablero))
    print("\nBuscando una solución...")

    solucion_encontrada = resolver(tablero, camino, estadisticas)

    if solucion_encontrada is False:
        print("No se encontró una solución para esta posición.")
        print("Estados revisados:", estadisticas[0])
        print("Retrocesos:", estadisticas[1])
        return
    print("\nMovimientos realizados:")
    tablero_mostrado = crear_tablero(posicion_vacia)
    numero_movimiento = 1
    for movimiento in camino:
        hacer_movimiento(tablero_mostrado, movimiento)
        mostrar_movimiento(numero_movimiento, movimiento, tablero_mostrado)
        numero_movimiento = numero_movimiento + 1
    print("\nTablero final:")
    mostrar_tablero(tablero_mostrado)
    print("Fichas restantes:", contar_fichas(tablero_mostrado))
    print("Estados revisados:", estadisticas[0])
    print("Retrocesos:", estadisticas[1])
    if contar_fichas(tablero_mostrado) == 1:
        print("Comprobación correcta: queda una sola ficha.")
if __name__ == "__main__":
    ejecutar()
