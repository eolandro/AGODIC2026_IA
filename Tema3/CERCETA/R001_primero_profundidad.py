"""R001 - Busqueda primero en profundidad."""


def buscar(grafo, inicio, meta):
    pendientes = [[inicio]]
    visitados = []

    while pendientes:
        # La pila saca el ultimo camino agregado.
        camino = pendientes.pop()
        actual = camino[-1]

        if actual in visitados:
            continue
        visitados.append(actual)
        print("Visitando:", actual)

        if actual == meta:
            return camino

        # Se revisan los vecinos de izquierda a derecha.
        for vecino in reversed(grafo.get(actual, [])):
            if vecino not in visitados:
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

    print("BUSQUEDA PRIMERO EN PROFUNDIDAD")
    print("Inicio: O   Meta: OJCM\n")

    camino = buscar(grafo, "O", "OJCM")
    if camino is None:
        print("No se encontro el camino.")
    else:
        print("\nCamino encontrado:", " -> ".join(camino))


if __name__ == "__main__":
    main()
