import json
import os
import sys

SIMBOLOS_VALIDOS = {"R", "B", "X", "."}

def cargar_tablero(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError as error:
        raise ValueError(f"no existe el archivo '{ruta}'.") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"el JSON no es válido: {error.msg}.") from error
    except UnicodeError as error:
        raise ValueError("el archivo debe estar guardado en UTF-8.") from error
    except OSError as error:
        raise ValueError(f"no se pudo leer el archivo: {error}.") from error
    if not isinstance(datos, dict) or "tablero" not in datos:
        raise ValueError("el JSON debe contener la clave 'tablero'.")
    tablero = datos["tablero"]
    if not isinstance(tablero, list) or not tablero:
        raise ValueError("'tablero' debe ser una lista no vacía.")
    if not all(isinstance(fila, list) for fila in tablero):
        raise ValueError("cada fila del tablero debe ser una lista.")
    columnas = len(tablero[0])
    if columnas == 0 or any(len(fila) != columnas for fila in tablero):
        raise ValueError("todas las filas deben tener la misma longitud y no estar vacías.")
    posiciones = {"R": [], "B": []}
    fila = 0
    while fila < len(tablero):
        valores = tablero[fila]
        columna = 0
        while columna < len(valores):
            valor = valores[columna]
            if not isinstance(valor, str) or valor not in SIMBOLOS_VALIDOS:
                raise ValueError(
                    f"símbolo no válido en fila {fila + 1}, columna {columna + 1}: {valor!r}."
                )
            if valor in posiciones:
                posiciones[valor].append((columna, len(tablero) - 1 - fila))
            columna = columna + 1
        fila = fila + 1
    if len(posiciones["R"]) != 1:
        raise ValueError("el tablero debe contener exactamente un robot 'R'.")
    if len(posiciones["B"]) != 1:
        raise ValueError("el tablero debe contener exactamente una bomba 'B'.")
    return tablero, posiciones["R"][0], posiciones["B"][0]

def distancia_manhattan(origen, destino):
    """Calcula h(n) para movimientos horizontales y verticales."""
    return abs(destino[0] - origen[0]) + abs(destino[1] - origen[1])

def vecinos_validos(posicion, tablero):
    """Devuelve vecinos (X, Y) dentro del tablero y que no son obstáculos."""
    x, y = posicion
    filas = len(tablero)
    columnas = len(tablero[0])
    candidatos = (
        (x, y + 1),
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
    )
    vecinos = []
    for vecino_x, vecino_y in candidatos:
        if 0 <= vecino_x < columnas and 0 <= vecino_y < filas:
            fila = filas - 1 - vecino_y
            if tablero[fila][vecino_x] != "X":
                vecinos.append((vecino_x, vecino_y))
    return vecinos

def costo_movimiento(origen, destino):
    """Devuelve el costo 1 de un movimiento horizontal o vertical."""
    return 1

def buscar_camino(tablero, inicio, destino):
    """Aplica A* y devuelve la ruta ordenada desde R hasta B, o None."""
    pendientes = [inicio]
    en_pendientes = {inicio}
    cerradas = set()
    predecesores = {}
    costos = {inicio: 0}
    while pendientes:
        def clave(posicion):
            h = distancia_manhattan(posicion, destino)
            f = costos[posicion] + h
            return f, h, posicion[1], posicion[0]
        actual = min(
            pendientes,
            key=clave,
        )
        pendientes.remove(actual)
        en_pendientes.remove(actual)
        if actual == destino:
            return reconstruir_camino(predecesores, inicio, destino)
        cerradas.add(actual)
        for vecino in vecinos_validos(actual, tablero):
            nuevo_costo = costos[actual] + costo_movimiento(actual, vecino)
            if nuevo_costo >= costos.get(vecino, float("inf")):
                continue
            costos[vecino] = nuevo_costo
            predecesores[vecino] = actual
            if vecino in cerradas:
                cerradas.remove(vecino)
            if vecino not in en_pendientes:
                pendientes.append(vecino)
                en_pendientes.add(vecino)
    return None

def reconstruir_camino(predecesores, inicio, destino):
    """Retrocede de B a R usando los predecesores y luego invierte la ruta."""
    camino = [destino]
    actual = destino
    while actual != inicio:
        actual = predecesores[actual]
        camino.append(actual)
    camino.reverse()
    return camino

def marcar_camino(tablero, camino):
    """Copia el tablero y marca solo las casillas intermedias con '-'."""
    resultado = [fila[:] for fila in tablero]
    filas = len(resultado)
    for x, y in camino[1:-1]:
        resultado[filas - 1 - y][x] = "-"
    return resultado

def imprimir_tablero(tablero):
    """Imprime únicamente el tablero final."""
    for fila in tablero:
        print(" ".join(fila))

def ejecutar(ruta_json):
    """Ejecuta la lectura, búsqueda y presentación del resultado."""
    try:
        tablero, inicio, destino = cargar_tablero(ruta_json)
    except ValueError as error:
        print(f"Error de configuración: {error}")
        return 1
    camino = buscar_camino(tablero, inicio, destino)
    if camino is None:
        print("No existe una ruta entre el robot y la bomba.")
        return 0
    imprimir_tablero(marcar_camino(tablero, camino))
    return 0
if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "tablero.json"
    )
    sys.exit(ejecutar(archivo))
