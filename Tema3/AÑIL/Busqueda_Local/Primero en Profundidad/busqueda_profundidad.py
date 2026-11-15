import json


def cargar_arbol(ruta="arbol.json"):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def elementos_disponibles(arbol, raiz):
    """Devuelve la raíz y todos los nodos que descienden de ella."""
    disponibles = []
    pendientes = [raiz]
    while pendientes:
        nodo = pendientes.pop(0)
        disponibles.append(nodo)
        pendientes.extend(arbol.get(nodo, []))
    return disponibles


def busqueda_en_profundidad(arbol, raiz, objetivo):
    pila = []
    actual = raiz
    paso = 1

    while True:
        # Cada vez que se asigna una nueva raíz, se imprime el punto actual y la pila
        print(f"\n--- Paso {paso} ---")
        print(f"Punto actual (raíz): {actual}")

        # 1. Revisar si la raíz actual es el elemento buscado
        if actual == objetivo:
            print(f"\n¡Elemento '{objetivo}' encontrado en el paso {paso}!")
            return True

        # 2. Obtener la lista de hijos y agregarlos a la pila
        hijos = arbol.get(actual, [])
        for hijo in hijos:
            pila.append(hijo)
        print(f"Hijos agregados: {hijos if hijos else 'ninguno'}")
        print(f"Pila (tope a la derecha): {pila}")

        # 3. Si la pila está vacía, ya no hay más elementos por explorar
        if not pila:
            print(f"\nEl elemento '{objetivo}' no se encontró en el árbol.")
            return False

        # 4. Extraer el elemento del tope de la pila y convertirlo en la nueva raíz
        actual = pila.pop()
        paso += 1


def main():
    arbol = cargar_arbol()

    # Opciones de raíz
    print("Opciones disponibles para tomar como raíz:")
    print(", ".join(arbol.keys()))
    raiz = input("\n¿Cuál es la raíz? ").strip()
    if raiz not in arbol:
        print(f"La raíz '{raiz}' no existe en el árbol.")
        return

    # Elementos disponibles para buscar a partir de la raíz elegida
    disponibles = elementos_disponibles(arbol, raiz)
    print(f"\nElementos disponibles para buscar desde '{raiz}':")
    print(", ".join(disponibles))
    objetivo = input("\n¿Qué elemento deseas buscar? ").strip()
    resultado = busqueda_en_profundidad(arbol, raiz, objetivo)
    print(f"\nResultado: {resultado}")


if __name__ == "__main__":
    main()