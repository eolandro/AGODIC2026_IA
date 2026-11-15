import json
import heapq

class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion  # (fila, columna)
        self.padre = padre
        self.g = 0  # Costo desde el inicio hasta el nodo actual
        self.h = 0  # Heurística estimada desde el nodo actual al objetivo
        self.f = 0  # Costo total f = g + h

    def __lt__(self, otro):
        return self.f < otro.f

def heuristica_manhattan(pos_actual, pos_destino):
    """Calcula la distancia de Manhattan entre dos posiciones."""
    return abs(pos_actual[0] - pos_destino[0]) + abs(pos_actual[1] - pos_destino[1])

def cargar_tablero(ruta_archivo="tablero.json"):
    """Carga el tablero 10x10 desde el archivo JSON."""
    with open(ruta_archivo, 'r') as f:
        datos = json.load(f)
    return datos["tablero"]

def encontrar_posiciones(tablero):
    """Busca las posiciones iniciales del personaje (R) y la bomba (B)."""
    inicio = None
    destino = None
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if tablero[i][j] == 'R':
                inicio = (i, j)
            elif tablero[i][j] == 'B':
                destino = (i, j)
    return inicio, destino

def a_estrella(tablero, inicio, destino):
    """Algoritmo de búsqueda de camino A*."""
    nodo_inicio = Nodo(inicio)
    nodo_destino = Nodo(destino)

    lista_abierta = []
    conjunto_cerrado = set()

    heapq.heappush(lista_abierta, nodo_inicio)

    # Movimientos posibles: arriba, abajo, izquierda, derecha
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while lista_abierta:
        nodo_actual = heapq.heappop(lista_abierta)

        if nodo_actual.posicion in conjunto_cerrado:
            continue

        conjunto_cerrado.add(nodo_actual.posicion)

        # Si llegamos a la bomba
        if nodo_actual.posicion == nodo_destino.posicion:
            camino = []
            curr = nodo_actual
            while curr is not None:
                camino.append(curr.posicion)
                curr = curr.padre
            return camino[::-1]  # Retorna el camino invertido (desde inicio a fin)

        r, c = nodo_actual.posicion

        for dr, dc in movimientos:
            nr, nc = r + dr, c + dc

            # Validar límites del tablero 10x10
            if 0 <= nr < len(tablero) and 0 <= nc < len(tablero[0]):
                # Si es un obstáculo ('X'), se ignora
                if tablero[nr][nc] == 'X':
                    continue

                if (nr, nc) in conjunto_cerrado:
                    continue

                vecino = Nodo((nr, nc), nodo_actual)
                vecino.g = nodo_actual.g + 1
                vecino.h = heuristica_manhattan(vecino.posicion, nodo_destino.posicion)
                vecino.f = vecino.g + vecino.h

                heapq.heappush(lista_abierta, vecino)

    return None  # No se encontró camino

def imprimir_tablero_con_camino(tablero, camino):
    """Imprime el tablero marcando la ruta óptima con '*'."""
    tablero_resultado = [row[:] for row in tablero]

    for pos in camino:
        r, c = pos
        if tablero_resultado[r][c] not in ('R', 'B'):
            tablero_resultado[r][c] = '*'

    print("\n--- Tablero con el camino óptimo marcado con '*' ---")
    for fila in tablero_resultado:
        print(" ".join(fila))

# --- Ejecución Principal ---
if __name__ == "__main__":
    try:
        tablero = cargar_tablero("tablero.json")
        inicio, destino = encontrar_posiciones(tablero)

        if not inicio or not destino:
            print("Error: El tablero debe contener un inicio 'R' y un objetivo 'B'.")
        else:
            print(f"Posición del personaje (R): {inicio}")
            print(f"Posición de la bomba (B): {destino}")

            camino = a_estrella(tablero, inicio, destino)

            if camino:
                print(f"\nCamino encontrado con éxito ({len(camino) - 1} pasos):")
                print(camino)
                imprimir_tablero_con_camino(tablero, camino)
            else:
                print("\nNo se encontró un camino hacia la bomba.")
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'tablero.json'. Asegúrate de crearlo en la misma carpeta.")