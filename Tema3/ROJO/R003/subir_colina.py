import json
import os
import heapq

def cargar_grafo(nombre_archivo):
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        aristas = json.load(f)

    grafo = {}
    for a, b, peso in aristas:
        grafo.setdefault(a, {})[b] = peso
        grafo.setdefault(b, {})[a] = peso
    return grafo


def subir_colina(grafo, inicio, meta, modo):
    camino = [inicio]
    visitados = {inicio}
    descartados = {}  # vecinos que ya se probaron desde cada nodo
    paso = 1

    while camino[-1] != meta:
        actual = camino[-1]
        opciones = {v: p for v, p in grafo[actual].items()
                    if v not in visitados and v not in descartados.get(actual, set())}

        print(f"\nPaso {paso} - Nodo actual: {actual}")
        print(f"  Vecinos disponibles: {opciones if opciones else 'ninguno'}")

        if not opciones:
            # Callejón sin salida: se regresa un nodo
            if len(camino) == 1:
                print("  No hay forma de llegar a la meta.")
                return None, 0
            camino.pop()
            anterior = camino[-1]
            descartados.setdefault(anterior, set()).add(actual)
            print(f"  Sin salida, se regresa a {anterior}")
        else:
            if modo == "corto":
                siguiente = min(opciones, key=opciones.get)
            else:
                siguiente = max(opciones, key=opciones.get)
            print(f"  Se elige: {siguiente} (peso {opciones[siguiente]})")
            camino.append(siguiente)
            visitados.add(siguiente)
        paso += 1

    costo = sum(grafo[camino[i]][camino[i + 1]] for i in range(len(camino) - 1))
    print(f"\n  ¡Meta '{meta}' alcanzada!")
    return camino, costo


def camino_optimo(grafo, inicio, meta):
    cola = [(0, inicio, [inicio])]
    vistos = set()
    while cola:
        costo, nodo, camino = heapq.heappop(cola)
        if nodo == meta:
            return camino, costo
        if nodo in vistos:
            continue
        vistos.add(nodo)
        for vecino, peso in grafo[nodo].items():
            if vecino not in vistos:
                heapq.heappush(cola, (costo + peso, vecino, camino + [vecino]))
    return None, 0


def formato(camino, grafo):
    texto = camino[0]
    for i in range(len(camino) - 1):
        texto += f" -({grafo[camino[i]][camino[i + 1]]})-> {camino[i + 1]}"
    return texto


def mostrar_grafo(grafo):
    print("\nGrafo cargado desde grafoclase.json:")
    for nodo, vecinos in grafo.items():
        lista = ", ".join(f"{v}({p})" for v, p in vecinos.items())
        print(f"  {nodo}: {lista}")


def pedir_nodos(grafo):
    print(f"\nNodos disponibles: {', '.join(grafo.keys())}")
    inicio = input("Nodo de inicio: ").strip().upper()
    meta = input("Nodo meta: ").strip().upper()
    if inicio not in grafo or meta not in grafo:
        print("Alguno de los nodos no existe en el grafo.")
        return None, None
    return inicio, meta


def ejecutar(grafo, inicio, meta, modo):
    criterio = "menor" if modo == "corto" else "mayor"
    print("\n" + "-" * 55)
    print(f"  CAMINO {modo.upper()} (elige siempre la arista de {criterio} peso)")
    print("-" * 55)
    camino, costo = subir_colina(grafo, inicio, meta, modo)
    if camino:
        print(f"\nCamino {modo}: {formato(camino, grafo)}")
        print(f"  Costo total: {costo}")
    return camino, costo


def comparar(grafo, inicio, meta):
    corto, costo_corto = ejecutar(grafo, inicio, meta, "corto")
    largo, costo_largo = ejecutar(grafo, inicio, meta, "largo")
    optimo, costo_optimo = camino_optimo(grafo, inicio, meta)

    print("\n" + "=" * 55)
    print("  COMPARACIÓN")
    print("=" * 55)
    if corto:
        print(f"Camino corto: {formato(corto, grafo)}  | Costo: {costo_corto}")
    if largo:
        print(f"Camino largo: {formato(largo, grafo)}  | Costo: {costo_largo}")
    if optimo:
        print(f"Óptimo real (Dijkstra): {formato(optimo, grafo)}  | Costo: {costo_optimo}")
        if corto and costo_corto > costo_optimo:
            print("\nNota: Subir la colina NO encontró el camino óptimo porque")
            print("solo ve a los vecinos inmediatos (se queda en un óptimo local).")


def main():
    grafo = cargar_grafo("grafoclase.json")

    while True:
        print("\n" + "*" * 55)
        print("  SUBIR LA COLINA (HILL CLIMBING)")
        print("*" * 55)
        print("  1. Buscar camino corto")
        print("  2. Buscar camino largo")
        print("  3. Comparar ambos caminos")
        print("  4. Ver grafo")
        print("  5. Salir\n")
        opcion = input("Elige una opción: \n").strip()

        if opcion in ("1", "2", "3"):
            inicio, meta = pedir_nodos(grafo)
            if inicio is None:
                continue
            if opcion == "1":
                ejecutar(grafo, inicio, meta, "corto")
            elif opcion == "2":
                ejecutar(grafo, inicio, meta, "largo")
            else:
                comparar(grafo, inicio, meta)
        elif opcion == "4":
            mostrar_grafo(grafo)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

        input("\nPresiona Enter para volver al menú...")


if __name__ == "__main__":
    main()
