import json

def cargar_arbol(archivo="rel.json"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'.")
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo '{archivo}' no tiene un formato JSON válido.")
        return []

arbol = cargar_arbol("rel.json")

def obtener_hijos(nodo, arbol):
    """Devuelve la lista de hijos directos de un nodo."""
    hijos = []
    for padre, hijo in arbol:
        if padre == nodo:
            hijos.append(hijo)
    return hijos

def pa(inicio, objetivo):
    # Búsqueda Primero en Anchura 
    if not arbol:
        print("El árbol está vacío o no se pudo cargar.\n")
        return False

    cola = [(inicio, [inicio])]
    visitados = []

    while cola:
        actual, camino = cola.pop(0)
        visitados.append(actual)

        if actual == objetivo:
            print(f"PA: ¡Elemento buscado '{objetivo}' encontrado!")
            print(f"Ruta óptima: {' -> '.join(camino)}")
            print(f"Nodos explorados en total: {visitados}\n")
            return True

        for hijo in obtener_hijos(actual, arbol):
            cola.append((hijo, camino + [hijo]))

    print(f"PA: Elemento '{objetivo}' no encontrado.\n")
    return False

def pp_recursivo(nodo, objetivo, visitados, camino):
    visitados.append(nodo)
    if nodo == objetivo:
        print(f"-> PP: ¡Elemento buscado '{objetivo}' encontrado!")
        print(f"-> Ruta óptima: {' -> '.join(camino)}")
        print(f"-> Nodos explorados en total: {visitados}\n")
        return True
    # Llamada recursiva para explorar los hijos en profundidad
    for hijo in reversed(obtener_hijos(nodo, arbol)):
        if pp_recursivo(hijo, objetivo, visitados, camino + [hijo]):
            return True
    return False

def pp(inicio, objetivo):
    if not arbol:
        print("El árbol está vacío o no se pudo cargar.\n")
        return False

    visitados = []
    camino = [inicio]
    return pp_recursivo(inicio, objetivo, visitados, camino)
    
print("**********************BUSQUEDAS**************************")
print("Ejemplos de funcion: Primero en Anchura -> pa('O', 'OKEN') o Primero en Profundidad ->  pp('O', 'OKEN')")
print("Escribe 'q' para salir.\n")

while True:
    comando = input("Ingrese la búsqueda: ")
    
    if comando.lower() == 'q':
        print("Programa finalizado.")
        break
    
    try:
        eval(comando)
    except Exception as e:
        print(f"Error al evaluar la instrucción: {e}")
        print("Sintaxis correcta: pp('O', 'OKEN') o pa('O', 'OKEN')\n")