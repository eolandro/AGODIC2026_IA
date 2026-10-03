class GrafoFiguras:
    def __init__(self, nodos, transiciones):
        self.nodos = {n[0]: n[1] for n in nodos}

        self.trans = {}
        for origen, respuesta, destino in transiciones:
            if origen not in self.trans:
                self.trans[origen] = {}
            self.trans[origen][str(respuesta).lower()] = destino

    def identificar(self, inicio=0):
        nodo_actual = inicio
        historial = []

        while True:
            texto = self.nodos[nodo_actual]
            historial.append(f"Nodo {nodo_actual}: {texto}")

            # Si el nodo contiene una pregunta
            if "?" in texto:
                respuesta = input(f"{texto}\n> ").strip().lower()

                if nodo_actual not in self.trans or respuesta not in self.trans[nodo_actual]:
                    print("Respuesta no válida. Intenta de nuevo.")
                    break

                nodo_actual = self.trans[nodo_actual][respuesta]
            else:
                print(f"\nFigura identificada: {texto}")
                break

        return historial


nodos = [
    [0, "¿Cuántos lados tiene la figura?\nOpciones: 0, 3, 4, 5, 6, 7 u 8"],
    [1, "¿Radio constante? (si/no)"],
    [2, "¿Todos sus lados son iguales? (si/no)"],
    [3, "¿Tienen ángulos de 90 grados? (si/no)"],
    [4, "Pentágono"],
    [5, "Hexágono"],
    [6, "Heptágono"],
    [7, "Octágono"],
    [8, "Círculo"],
    [9, "Elipse"],
    [10, "Triángulo Equilátero"],
    [11, "Triángulo Isósceles"],
    [12, "Triángulo Escaleno"],
    [13, "Cuadrado"],
    [14, "Rectángulo"],
    [15, "Cuadrilátero no regular"],
    [16, "¿Todos sus lados son iguales? (si/no)"],
    [17, "¿Tiene dos lados iguales? (si/no)"]
]

transiciones = [
    [0, "0", 1],
    [0, "3", 2],
    [0, "4", 16],
    [0, "5", 4],
    [0, "6", 5],
    [0, "7", 6],
    [0, "8", 7],

    [1, "si", 8],
    [1, "no", 9],

    [2, "si", 10],
    [2, "no", 17],
    [17, "si", 11],
    [17, "no", 12],

    [16, "si", 13],
    [16, "no", 3],
    [3, "si", 14],
    [3, "no", 15]
]


if __name__ == "__main__":
    grafo = GrafoFiguras(nodos, transiciones)

    print("=== Identificador de Figuras Geométricas ===\n")
    grafo.identificar()
