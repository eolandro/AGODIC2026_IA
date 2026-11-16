import json
import os
import sys
from collections import deque

try:
    sys.stdout.reconfigure(encoding="utf-8")   # para la consola de Windows
except AttributeError:
    pass

ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"


def cargar_grafo(ruta):
    """Lee el grafo desde un JSON y lo arma como nodo -> {vecino: costo}."""
    with open(ruta, encoding="utf-8") as archivo:
        datos = json.load(archivo)
    grafo = {}
    for arista in datos["aristas"]:
        a, b, costo = arista["origen"], arista["destino"], arista["costo"]
        grafo.setdefault(a, {})[b] = costo
        grafo.setdefault(b, {})[a] = costo   # no dirigido: va en ambos sentidos
    return grafo, datos.get("inicio"), datos.get("meta")


def ordenar(nodos):
    """Orden alfabético en español (la Ñ va después de la N)."""
    return sorted(nodos, key=lambda n: [ALFABETO.find(ch) if ch in ALFABETO
                                        else 100 + ord(ch) for ch in n.upper()])


def heuristica(grafo, meta):
    """h(n): saltos mínimos de cada nodo a la meta (BFS desde la meta)."""
    h = {meta: 0}
    cola = deque([meta])
    while cola:
        n = cola.popleft()
        for v in grafo[n]:
            if v not in h:
                h[v] = h[n] + 1
                cola.append(v)
    return h


def alcanza_meta(grafo, desde, meta, prohibidos):
    """True si desde 'desde' se llega a la meta sin pasar por 'prohibidos'."""
    if desde == meta:
        return True
    vistos = set(prohibidos) | {desde}
    cola = deque([desde])
    while cola:
        n = cola.popleft()
        for v in grafo[n]:
            if v == meta:
                return True
            if v not in vistos:
                vistos.add(v)
                cola.append(v)
    return False


def camino_corto(grafo, h, inicio, meta):
    """Subir la colina clásico: siempre al vecino con menor h."""
    actual, camino, costo, paso = inicio, [inicio], 0, 0
    while actual != meta:
        paso += 1
        vecinos = ordenar(grafo[actual])
        print(f"Paso {paso} | Actual: {actual} (h={h[actual]})")
        print("       | Vecinos: " +
              ", ".join(f"{v}(h={h[v]}, costo={grafo[actual][v]})" for v in vecinos))

        # Mejor vecino: menor h; en empate, la arista más barata
        mejor = min(vecinos, key=lambda v: (h[v], grafo[actual][v]))
        if h[mejor] >= h[actual]:
            print(f"       | Ningún vecino mejora h={h[actual]}: óptimo local")
            return camino, costo, False

        print(f"       | Subo a {mejor} (el más cercano a la meta)")
        costo += grafo[actual][mejor]
        actual = mejor
        camino.append(actual)
    return camino, costo, True


def camino_largo(grafo, h, inicio, meta):
    """Variante para rodear: siempre al vecino con mayor h que todavía
    pueda llegar a la meta, sin repetir nodos."""
    actual, camino, costo, paso = inicio, [inicio], 0, 0
    while actual != meta:
        paso += 1
        visitados = set(camino)
        vecinos = [v for v in ordenar(grafo[actual]) if v not in visitados]
        print(f"Paso {paso} | Actual: {actual} (h={h[actual]})")
        print("       | Vecinos sin visitar: " +
              (", ".join(f"{v}(h={h[v]}, costo={grafo[actual][v]})" for v in vecinos)
               or "ninguno"))

        # Solo sirven los vecinos desde donde aún se puede llegar a la meta
        validos = [v for v in vecinos if alcanza_meta(grafo, v, meta, visitados)]
        descartados = [v for v in vecinos if v not in validos]
        if descartados:
            print(f"       | Descarto {', '.join(descartados)}: desde ahí ya no se llega a {meta}")
        if not validos:
            print("       | No queda ningún vecino útil: se atora")
            return camino, costo, False

        # Peor vecino: mayor h; en empate, la arista más cara
        elegido = max(validos, key=lambda v: (h[v], grafo[actual][v]))
        print(f"       | Voy a {elegido} (el que más rodea)")
        costo += grafo[actual][elegido]
        actual = elegido
        camino.append(actual)
    return camino, costo, True


def subir_la_colina(grafo, inicio, meta, tipo):
    h = heuristica(grafo, meta)
    if inicio not in h:
        print(f"\nDesde {inicio} no se puede llegar a {meta}.")
        return [inicio], 0, False
    print(f"\nHeurística h(n) hacia {meta}:")
    print("  " + "  ".join(f"{n}={h[n]}" for n in ordenar(h)))
    nombre = "CORTO" if tipo == "corto" else "LARGO"
    print(f"\nBuscando de {inicio} a {meta} con Subir la colina (camino {nombre})\n")
    if tipo == "corto":
        return camino_corto(grafo, h, inicio, meta)
    return camino_largo(grafo, h, inicio, meta)


def menu():
    print("\n" + "=" * 40)
    print("  SUBIR LA COLINA - ¿Qué camino quieres?")
    print("  1) Camino corto")
    print("  2) Camino largo")
    print("  3) Salir")
    print("=" * 40)
    opcion = input("Elige una opción: ").strip()
    while opcion not in ("1", "2", "3"):
        opcion = input("  Escribe 1, 2 o 3: ").strip()
    return opcion


def pedir_nodo(grafo, mensaje, por_defecto):
    valor = input(f"{mensaje} [{por_defecto}]: ").strip().upper() or por_defecto
    while valor not in grafo:
        valor = input(f"  Nodo no válido. Opciones {ordenar(grafo)}: ").strip().upper()
    return valor


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "grafo.json")
    try:
        grafo, inicio_def, meta_def = cargar_grafo(ruta)
    except (OSError, ValueError, KeyError) as error:
        print(f"Error al leer {ruta}: {error}")
        sys.exit(1)

    print(f"Grafo cargado de {ruta} (nodo: vecinos con costo)")
    for n in ordenar(grafo):
        print(f"  {n}: {grafo[n]}")

    while True:
        opcion = menu()
        if opcion == "3":
            print("¡Hasta luego!")
            break
        tipo = "corto" if opcion == "1" else "largo"

        inicio = pedir_nodo(grafo, "\nNodo inicial", inicio_def or ordenar(grafo)[0])
        meta = pedir_nodo(grafo, "Nodo meta", meta_def or ordenar(grafo)[-1])

        camino, costo, exito = subir_la_colina(grafo, inicio, meta, tipo)
        print(f"\nCamino {tipo} recorrido: {' -> '.join(camino)}")
        print(f"Saltos: {len(camino) - 1}   Costo total: {costo}")
        print("Llegó a la meta." if exito else "No llegó a la meta.")
