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

    def loadText(self, L):
        if not L or self.Estado != "wait":
            return
        self.Instrucciones = [a for a in L]
        self.Estado = "ready"
        self.RIP = 0

    def __str__(self):
        S =  f'R0: {self.Registros[0]} | '
        S += f'R1: {self.Registros[1]} | '
        S += f'R2: {self.Registros[2]} | '
        S += f'R3: {self.Registros[3]}\n'

        if self.Estado == "ready" and self.RIP < len(self.Instrucciones):
            S += f"Por ejecutar: {self.Instrucciones[self.RIP]}\n"

        CM = [fila[::] for fila in self.Mapa]
        if self.Estado in ["ready", "wait", "done"]:
            x, y = self.RBPos
            CM[x][y] = 'R'
        x, y = self.BBPos
        CM[x][y] = 'B'

        for fila in CM:
            S += ' '.join([str(e) for e in fila]) + "\n"
        S += f"Estado: {self.Estado}"
        return S

    def step(self):
        if self.Estado != "ready":
            return

        fetch = [ins for ins in self.Instrucciones[self.RIP].split(" ") if ins]

      
        def get_val(v):
            if v.startswith("R"): return self.Registros[int(v[1])]
            if v.startswith("#"): return int(v[1:], 16)
            return int(v)

        def reg_i(r): return int(r[1])

        match fetch:
            case ['izq']:
                self.RBPos[1] -= 1
                if self.RBPos[1] < 0: self.Estado = "dead"
            case ['der']:
                self.RBPos[1] += 1
                if self.RBPos[1] >= len(self.Mapa[0]): self.Estado = "dead"
            case ['arriba']:
                self.RBPos[0] -= 1
                if self.RBPos[0] < 0: self.Estado = "dead"
            case ['abajo']:
                self.RBPos[0] += 1
                if self.RBPos[0] >= len(self.Mapa): self.Estado = "dead"


            case [R, '=', val] if R.startswith("R"):
                self.Registros[reg_i(R)] = get_val(val)


            case [R, '=', 'sensor', M] if R.startswith("R"):
                x, y = self.RBPos
                dx, dy = {'arriba':(-1,0), 'abajo':(1,0), 'izq':(0,-1), 'der':(0,1)}[M]
                nx, ny = x + dx, y + dy
                if 0 <= nx < 5 and 0 <= ny < 5 and self.Mapa[nx][ny] != 1:
                    self.Registros[reg_i(R)] = 1
                else:
                    self.Registros[reg_i(R)] = 0


            case [R, '=', A, op, B] if R.startswith("R"):
                res = get_val(A) + get_val(B) if op == '+' else get_val(A) - get_val(B)
                self.Registros[reg_i(R)] = res


            case ['Si', R]:
                if get_val(R) == 0:
                    n = 1
                    while n > 0 and self.RIP < len(self.Instrucciones) - 1:
                        self.RIP += 1
                        p = self.Instrucciones[self.RIP].split()
                        if p and p[0] == 'Si': n += 1
                        elif p and p[0] == 'FinSi': n -= 1

            case ['FinSi']:
                pass


            case ['ciclo', R]:
                if get_val(R) == 0:
                    n = 1
                    while n > 0 and self.RIP < len(self.Instrucciones) - 1:
                        self.RIP += 1
                        p = self.Instrucciones[self.RIP].split()
                        if p and p[0] == 'ciclo': n += 1
                        elif p and p[0] == 'finciclo': n -= 1

            case ['finciclo']:
                n = 1
                while n > 0 and self.RIP > 0:
                    self.RIP -= 1
                    p = self.Instrucciones[self.RIP].split()
                    if p and p[0] == 'finciclo': n += 1
                    elif p and p[0] == 'ciclo': n -= 1
                self.RIP -= 1  

        self.RIP += 1
        if self.RBPos == self.BBPos:
            self.Estado = "done"
        elif self.RIP >= len(self.Instrucciones):
            self.Estado = "done"
