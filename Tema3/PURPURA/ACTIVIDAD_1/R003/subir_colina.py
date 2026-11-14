##R003##
##10##
"""
Descripción: Un programa que aplique Subir la colina
Restricciones: NA.
"""

from collections import deque


ARISTAS = [
    ("Ñ", "O", 10),
    ("O", "S", 15),
    ("S", "T", 6),
    ("T", "U", 10),
    ("U", "V", 2),
    ("V", "A", 10),
    ("Ñ", "V", 30),
    ("Ñ", "P", 11),
    ("P", "Q", 11),
    ("P", "R", 5),
    ("R", "Q", 6),
    ("Q", "U", 12),
]


def construir_grafo(aristas):
    """Crea un diccionario de adyacencia: nodo -> {vecino: peso}."""
    grafo = {}
    for a, b, peso in aristas:
        grafo.setdefault(a, {})[b] = peso
        grafo.setdefault(b, {})[a] = peso
    return grafo


def subir_colina(grafo, inicio, meta, estrategia="corto", tam_cache=3, max_pasos=50):
    cache = deque(maxlen=tam_cache)   # al pasar de 3 elementos, elimina el más antiguo
    actual = inicio
    camino = [inicio]
    costo_total = 0
    pasos = 0

    print(f"\n=== Estrategia: camino {estrategia.upper()} | {inicio} -> {meta} ===")

    while actual != meta:
        if pasos >= max_pasos:
            print("Se alcanzó el límite de pasos sin llegar a la meta.")
            return None, costo_total

        # Vecinos disponibles (los que no están en el caché)
        candidatos = {v: p for v, p in grafo[actual].items() if v not in cache}

        if not candidatos:
            print(f"Atorado en {actual}: todos sus vecinos están en el caché {list(cache)}.")
            return None, costo_total

        # Elegir según la estrategia
        if estrategia == "corto":
            siguiente = min(candidatos, key=candidatos.get)
        else:
            siguiente = max(candidatos, key=candidatos.get)

        peso = candidatos[siguiente]
        print(f"Paso {pasos + 1}: en {actual}, opciones {candidatos} "
            f"-> voy a {siguiente} (costo {peso})")

        cache.append(actual)          # agrego mi anterior al caché
        print(f"         caché: {list(cache)}")

        costo_total += peso
        actual = siguiente
        camino.append(actual)
        pasos += 1

    print(f"Camino encontrado: {' -> '.join(camino)}")
    print(f"Costo total: {costo_total}")
    return camino, costo_total


def main():
    grafo = construir_grafo(ARISTAS)

    print("Nodos del grafo:", ", ".join(grafo.keys()))
    inicio = input("Nodo de inicio : ").strip().upper() or "Ñ"
    meta = input("Nodo meta : ").strip().upper() or "A"

    if inicio not in grafo or meta not in grafo:
        print("Nodo no válido.")
        return

    print("\n1) Camino corto\n2) Camino largo\n3) Ambos")
    opcion = input("Elige estrategia : ").strip() or "3"

    if opcion in ("1", "3"):
        subir_colina(grafo, inicio, meta, "corto")
    if opcion in ("2", "3"):
        subir_colina(grafo, inicio, meta, "largo")


if __name__ == "__main__":
    main()
