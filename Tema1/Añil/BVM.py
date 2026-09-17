class BoomeVirtualMachine:
    def __init__(self):
        ################[R0, R1, R2, R3]
        self.Registros = [ 0, 0, 0, 0 ]
        self.Instrucciones = []
        self.RIP = None
        ################
        self.Mapa = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,1,0],
            [0,0,1,0,0,0,0,1,0,0],
            [0,0,1,0,0,0,0,1,0,0],
            [0,1,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0]
        ]
        self.RBPos = [0,0]
        self.BBPos = [3,5]
        self.Estado = "wait"

    #condicional("Si",Re,[F|R],"FinSi") :- regs(Re), lineas([F | R]).
    #ciclos("ciclo",Re,[F | R],"finciclo") :- regs(Re), lineas([F | R]).
    def flujo(self, Lineas):
        for L in Lineas:
            if isinstance(L, list):
                match L:
                    case ["Si",Re,Sub,"FinSi"]:              #decode
                        if self.Registros[int(Re[1])] != 0:   #execute
                            yield from self.flujo(Sub)
                    case ["ciclo",Re,Sub,"finciclo"]:        #decode
                        while self.Registros[int(Re[1])] != 0: #execute
                            yield from self.flujo(Sub)
            else:
                yield L

    def loadText(self, L):
        if not L:
            return
        if not self.Estado == "wait":
            return
        self.Instrucciones = [
            a for a in L
        ]
        self.Flujo = self.flujo(self.Instrucciones)
        self.Actual = next(self.Flujo, None)
        self.RIP = 0
        self.Estado = "ready" if self.Actual is not None else "done"

    def __str__(self):
        S =  f'R0: {self.Registros[0]} |'
        S += f'R1: {self.Registros[1]} |'
        S += f'R2: {self.Registros[2]} |'
        S += f'R3: {self.Registros[3]} |'
        S += "\n"
        if self.Estado == "ready":
            S += f"Por ejecutar: {self.Actual}"
        S += "\n"
        CM = [fila [::] for fila in self.Mapa]
        if self.Estado in ["ready","wait","done"]:
            x,y = self.RBPos
            CM[x][y] = 'R'
        x,y = self.BBPos
        CM[x][y] = 'B'
        CM = [ [str(e) for e in fila] for fila in CM ]

        for fila in CM:
            S += ' '.join(fila)
            S += "\n"

        S += f"Estado: {self.Estado}"
        return S

    def step(self):
        if self.Estado != "ready":
            return
        fetch = self.Actual
        fetch = fetch.split(" ")
        fetch = [ins for ins in fetch if ins]
        match fetch:
            case ['izq']:   #decode
                self.RBPos[1] -= 1  #execute
                if self.RBPos[1] < 0:
                    self.Estado = "dead"
                    return
            case ['der']:   #decode
                self.RBPos[1] += 1  #execute
                x,_ = self.RBPos
                if self.RBPos[1] >= len(self.Mapa[x]):
                    self.Estado = "dead"
                    return
            case ['arriba']:   #decode
                self.RBPos[0] -= 1  #execute
                if self.RBPos[0] < 0:
                    self.Estado = "dead"
                    return
            case ['abajo']:   #decode
                self.RBPos[0] += 1  #execute
                if self.RBPos[0] >= len(self.Mapa):
                    self.Estado = "dead"
                    return
            #asign(R,"=",Nh) :- regs(R),numhex(Nh).
            case [R,"=",Nh] if Nh.startswith("#"):   #decode
                IndReg = int(R[1])                       #execute
                self.Registros[IndReg] = int(Nh[1:], 16)
            #asign(R,"=","sensor",M) :- regs(R),movs(M).
            case [R,"=","sensor",M]:              #decode
                IndReg = int(R[1])                    #execute
                Dir = {"izq":(0,-1),"der":(0,1),"arriba":(-1,0),"abajo":(1,0)}
                dx,dy = Dir[M]
                x = self.RBPos[0] + dx
                y = self.RBPos[1] + dy
                if x < 0 or x >= len(self.Mapa) or y < 0 or y >= len(self.Mapa[0]):
                    self.Registros[IndReg] = 1
                else:
                    self.Registros[IndReg] = self.Mapa[x][y]
            #asign(R,"=",A,O,B) :- regs(R),opera(A,O,B).
            case [R,"=",A,O,B]:                   #decode
                IndReg = int(R[1])                    #execute
                if A.startswith("#"):
                    ValorA = int(A[1:], 16)
                else:
                    ValorA = self.Registros[int(A[1])]
                if B.startswith("#"):
                    ValorB = int(B[1:], 16)
                else:
                    ValorB = self.Registros[int(B[1])]
                if O == "+":
                    self.Registros[IndReg] = ValorA + ValorB
                elif O == "-":
                    self.Registros[IndReg] = ValorA - ValorB
        if self.RBPos == self.BBPos:   #BoomMe llego a la Bomba
            self.Estado = "dead"
            return
        self.RIP += 1
        self.Actual = next(self.Flujo, None)
        if self.Actual is None:
            self.Estado = "done"