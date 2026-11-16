class BoomeVirtualMachine:
    def __init__(self, Mapa, RBPos, BBPos):
        # Mapa: matriz de simbolos "0", "X", "R", "B" (el original, no se modifica)
        self.Mapa = [fila[::] for fila in Mapa]
        self.Instrucciones = []
        self.RIP = None
        self.RBPos = list(RBPos)
        self.BBPos = list(BBPos)
        self.Rastro = []        # casillas por donde ha pasado Boome
        self.Estado = "wait"

    def loadText(self, L):
        if not L:
            return
        if not self.Estado == 'wait':
            return
        self.Instrucciones = [
            a for a in L
        ]
        self.Estado = "ready"
        self.RIP = 0

    def __str__(self):
        CM = [fila[::] for fila in self.Mapa]
        for x, y in self.Rastro:
            if CM[x][y] == '0':
                CM[x][y] = '*'
        return '\n'.join(' '.join(fila) for fila in CM)

    def step(self):
        if self.Estado != 'ready':
            return
        fetch = self.Instrucciones[self.RIP]
        fetch = fetch.split(" ")
        fetch = [ins for ins in fetch if ins]
        match fetch:
            case ['arriba']: #decode
                self.RBPos[0] -= 1 #execute
            case ['abajo']:
                self.RBPos[0] += 1
            case ['izq']:
                self.RBPos[1] -= 1
            case ['der']:
                self.RBPos[1] += 1

        self.Rastro.append(tuple(self.RBPos))
        self.RIP += 1
        if self.RIP >= len(self.Instrucciones):
            self.Estado = "done"
