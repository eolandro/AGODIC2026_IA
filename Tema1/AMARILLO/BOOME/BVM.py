class BoomeVirtualMachine:

    def __init__(self):
        self.Registros = [0, 0, 0, 0]
        self.Instrucciones = []
        self.RIP = None
        self.Mapa = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.RBPos = [0, 0]
        self.BBPos = [4, 4]
        self.Estado = "wait"
    def loadText(self, L):
        if not L:
            return
        if not self.Estado == "wait":
            return
        self.Instrucciones = [
            a for a in L
        ]
        self.Estado = "ready"
        self.RIP = 0
    def __str__(self):
        s = f"R0:{self.Registros[0]} | "
        s += f"R1:{self.Registros[1]} | "
        s += f"R2:{self.Registros[2]} | "
        s += f"R3:{self.Registros[3]} | "
        s += "\n"
        if (
            self.Estado == "ready"
            and self.RIP is not None
            and self.RIP < len(self.Instrucciones)
        ):
            s += f"por ejecutar: {self.Instrucciones[self.RIP]}"
        s += "\n"
        CM = [fila[:] for fila in self.Mapa]
        x, y = self.RBPos
        if 0 <= x < len(CM) and 0 <= y < len(CM[x]):
            CM[x][y] = "R"
        x, y = self.BBPos
        if 0 <= x < len(CM) and 0 <= y < len(CM[x]):
            CM[x][y] = "B"
        CM = [
            [str(e) for e in fila]
            for fila in CM
        ]
        ##########
        for x in range (len(CM)):
            for y in range (len(CM[x])):
                if CM[x][y] == "1":
                    CM[x][y] = "X"
        """""
        for x in range (len(CM)):
            for y in range (len(CM[x])):
                if CM[x][y] == "1":                        
                    CM[x][y] = "0"
        """
        ########
        for fila in CM:
            s += " ".join(fila)
            s += "\n"
        s += f"Estado {self.Estado}"
        return s
    def step(self):
        if self.Estado != "ready":
            return
        if self.RIP is None or self.RIP >= len(self.Instrucciones):
            self.Estado = "done"
            return
        fetch = self.Instrucciones[self.RIP]
        if isinstance(fetch, str):
            fetch =fetch.split(" ")
            fetch = [ins for ins in fetch if ins
            ]
        """
        fetch = fetch.split(" ")
        fetch = [
            ins for ins in fetch if ins
        ]
        """
        match fetch:
            ################
            case [R, "=", Nh]:
                if R == "R0":
                    r = 0
                elif R == "R1":
                    r = 1
                elif R == "R2":
                    r = 2
                elif R == "R3":
                    r = 3
                else:
                    self.Estado = "dead"
                    return
                if Nh[0] == "#":
                    n = int(Nh[1:], 16)
                else:
                    self.Estado = "dead"
                    return
                self.Registros[r] = n

            case [R, "=", "sensor", M]:
                if R == "R0":
                    r = 0
                elif R == "R1":
                    r = 1
                elif R == "R2":
                    r = 2
                elif R == "R3":
                    r = 3
                else:
                    self.Estado = "dead"
                    return
                if M == "izq":
                    dx = 0
                    dy = -1
                elif M == "der":
                    dx = 0
                    dy = 1
                elif M == "arriba":
                    dx = -1
                    dy = 0
                elif M == "abajo":
                    dx = 1
                    dy = 0
                else:
                    self.Estado = "dead"
                    return
                nx = self.RBPos[0] + dx
                ny = self.RBPos[1] + dy
                if nx < 0 or nx >= len(self.Mapa):
                    self.Registros[r] = 1
                elif ny < 0 or ny >= len(self.Mapa[nx]):
                    self.Registros[r] = 1
                else:
                    self.Registros[r] = self.Mapa[nx][ny]
                
            case [R, "=", A, O, B]:
                if R == "R0":
                    r = 0
                elif R == "R1":
                    r = 1
                elif R == "R2":
                    r = 2
                elif R == "R3":
                    r = 3
                else:
                    self.Estado = "dead"
                    return
                if A[0] == "#":
                    a = int(A[1:], 16)
                elif A == "R0":
                    a = self.Registros[0]
                elif A == "R1":
                    a = self.Registros[1]
                elif A == "R2":
                    a = self.Registros[2]
                elif A == "R3":
                    a = self.Registros[3]
                else:
                    self.Estado = "dead"
                    return
                if B[0] == "#":
                    b = int(B[1:], 16)
                elif B == "R0":
                    b = self.Registros[0]
                elif B == "R1":
                    b = self.Registros[1]
                elif B == "R2":
                    b = self.Registros[2]
                elif B == "R3":
                    b = self.Registros[3]
                else:
                    self.Estado = "dead"
                    return
                if O == "+":
                    self.Registros[r] = a + b
                elif O == "-":
                    self.Registros[r] = a - b  
                else:
                    self.Estado = "dead"
                    return  
            ################
            case ["izq"]:
                self.RBPos[1] -= 1
                if self.RBPos[1] < 0:
                    self.Estado = "dead"
                    return
            case ["der"]:
                self.RBPos[1] += 1
                x, __ = self.RBPos
                if self.RBPos[1] >= len(self.Mapa[x]):
                    self.Estado = "dead"
                    return
            ################
            case ["abajo"]:
                self.RBPos[0] += 1
                if self.RBPos[0] >= len(self.Mapa):
                    self.Estado = "dead"
                    return
            case ["Si", R, cuerpo, "FinSi"]:
                if R == "R0":
                    r = 0
                elif R == "R1":
                    r = 1
                elif R == "R2":
                    r = 2
                elif R == "R3":
                    r = 3
                else:
                    self.Estado = "dead"
                    return
                if self.Registros[r] == 0:
                    self.RIP += 1
                    return
                if self.Registros[r] != 0:
                    for instruccion in cuerpo:
                        self.Instrucciones.insert(self.RIP + 1, instruccion)
                        
            case ["ciclos", R, cuerpo, "Finciclo"]:
                if R == "R0":
                    r = 0
                elif R == "R1":
                    r = 1 
                elif R == "R2":
                    r = 2
                elif R == "R3":
                    r = 3
                else:
                    self.Estado = "dead"
                    return
                for i in range(self.Registros[r]):
                    for instruccion in cuerpo:
                        self.Instrucciones.insert(self.RIP + 1, instruccion)
            
            case ["arriba"]:
                self.RBPos[0] -= 1
                if self.RBPos[0] < 0:
                    self.Estado = "dead"
                    return
            ###############
            case _:
                self.Estado = "dead"
                return
        ###########
        if self.Mapa[self.RBPos[0]][self.RBPos[1]] == 1:
            self.Estado = "dead"
            return
            
        if self.RBPos == self.BBPos:
            self.Estado = "win"
            return
        #############
        
        self.RIP += 1
        if self.RIP >= len(self.Instrucciones):
            self.Estado = "done"