"""R002 - Busqueda primero en anchura."""

from collections import deque


def buscar(grafo, inicio, meta):
    pendientes = deque([[inicio]])
    visitados = [inicio]

    while pendientes:
        # La cola saca el primer camino agregado.
        camino = pendientes.popleft()
        actual = camino[-1]
        print("Visitando:", actual)

        if actual == meta:
            return camino

        for vecino in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.append(vecino)
                pendientes.append(camino + [vecino])

    return None


def main():

    grafo = {
        "O": ["OJ", "OK", "OL"],
        "OJ": ["OJB", "OJC", "OJD"],
        "OJB": [],
        "OJC": ["OJCM"],
        "OJCM": [],
        "OJD": [],
        "OK": ["OKE", "OKF"],
        "OKE": ["OKEN"],
        "OKEN": [],
        "OKF": [],
        "OL": ["OLG", "OLH", "OLI"],
        "OLG": [],
        "OLH": ["OLHA"],
        "OLHA": [],
        "OLI": ["OLIP"],
        "OLIP": ["OLIPA"],
        "OLIPA": []
    }

    print("BUSQUEDA PRIMERO EN ANCHURA")
    print("Inicio: O   Meta: OKEN\n")

    camino = buscar(grafo, "O", "OKEN")
    if camino is None:
        print("No se encontro el camino.")
    else:
        print("\nCamino encontrado:", " -> ".join(camino))


if __name__ == "__main__":
    main()
