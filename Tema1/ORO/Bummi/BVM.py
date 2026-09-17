class BoomeVirtualMachine:

    def __init__(self):
        self.Registros = [0, 0, 0, 0]
        self.Instrucciones = []

        self.Mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.RBPos = [0, 0]
        self.BBPos = [3, 5]

        self.Estado = "wait"
        self.RIP = 0

    def loadText(self, L):
        if not L:
            return

        if self.Estado != "wait":
            return

        self.Instrucciones = [a for a in L]
        self.Estado = "ready"
        self.RIP = 0

    def __str__(self):
        S = ""

        S += f"R0: {self.Registros[0]} | "
        S += f"R1: {self.Registros[1]} | "
        S += f"R2: {self.Registros[2]} | "
        S += f"R3: {self.Registros[3]} | "

        S += "\n"

        if self.Estado == "ready" and self.RIP < len(self.Instrucciones):
            S += f"Por ejecutar: {self.Instrucciones[self.RIP]}"
        else:
            S += "Sin instrucciones por ejecutar"

        S += "\n"

        CM = [fila[::] for fila in self.Mapa]

        x, y = self.RBPos
        CM[x][y] = "R"

        x, y = self.BBPos
        CM[x][y] = "B"

        CM = [[str(e) for e in fila] for fila in CM]

        for fila in CM:
            S += " ".join(fila)
            S += "\n"

        S += f"Estado: {self.Estado}"

        return S

    def step(self):
        if self.Estado != "ready":
            return

        fetch = self.Instrucciones[self.RIP]
        fetch = fetch.split(" ")
        fetch = [ins for ins in fetch if ins]

        match fetch:

            case ["izq"]:
                if self.RBPos[1] - 1 < 0:
                    self.Estado = "dead"
                    return

                x = self.RBPos[0]
                y = self.RBPos[1] - 1

                if self.Mapa[x][y] != 1:
                    self.RBPos[1] -= 1

            case ["der"]:
                x = self.RBPos[0]

                if self.RBPos[1] + 1 >= len(self.Mapa[x]):
                    self.Estado = "dead"
                    return

                y = self.RBPos[1] + 1

                if self.Mapa[x][y] != 1:
                    self.RBPos[1] += 1

            case ["arriba"]:
                if self.RBPos[0] - 1 < 0:
                    self.Estado = "dead"
                    return

                x = self.RBPos[0] - 1
                y = self.RBPos[1]

                if self.Mapa[x][y] != 1:
                    self.RBPos[0] -= 1

            case ["abajo"]:
                if self.RBPos[0] + 1 >= len(self.Mapa):
                    self.Estado = "dead"
                    return

                x = self.RBPos[0] + 1
                y = self.RBPos[1]

                if self.Mapa[x][y] != 1:
                    self.RBPos[0] += 1

        self.RIP += 1

        if self.RIP >= len(self.Instrucciones):
            self.Estado = "done"
