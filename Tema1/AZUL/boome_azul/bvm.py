class BoomeVirtualMachine:
    def __init__(self):
        ####################### R0,R1,R2,R3
        self.Registros = [0,0,0,0]   # registros de la VM
        self.Instrucciones = []      # lista de instrucciones cargadas
        self.RIP = None              # puntero de instrucción
        #######################
        self.Mapa = [                # mapa de entorno (matriz)
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
        self.RBPos = [0,0]           # posición del robot
        self.BBPos = [4,4]           # posición del objetivo
        self.Estado = "wait"         # estado inicial

    def loadText(self, L):
        """
        Carga instrucciones en la máquina virtual.
        - Solo si está en estado 'wait'.
        """
        if not L:
            return
        if not self.Estado == 'wait':
            return
        self.Instrucciones = [a for a in L]
        self.Estado = "ready"
        self.RIP = 0

    def __str__(self):
        """
        Representación textual del estado actual de la VM.
        Incluye registros, instrucción por ejecutar y mapa.
        """
        S = f'R0: {self.Registros[0]} |'
        S += f'R1: {self.Registros[1]} |'
        S += f'R2: {self.Registros[2]}'
        S += f'R3: {self.Registros[3]}'
        S += "\n"
        if self.Estado == "ready":
            S += f"Por ejecutar {self.Instrucciones[self.RIP]}"
            S += "\n"
        CM = [fila[:] for fila in self.Mapa]
        if self.Estado in ["ready","wait","done"]:
            x,y = self.RBPos
            CM[x][y] = 'R'
            x,y = self.BBPos
            CM[x][y] = 'B'
        CM = [[str(e) for e in fila] for fila in CM]
        for fila in CM:
            S += " ".join(fila)
            S += "\n"
        S += f"Estado {self.Estado}"
        return S

    def step(self):
        """
        Ejecuta un paso de la máquina virtual.
        - Decodifica y ejecuta la instrucción actual.
        - Actualiza RIP y estado.
        """
        if self.Estado != "ready":
            return
        fetch = self.Instrucciones[self.RIP]
        fetch = fetch.split(" ")
        fetch = [ins for ins in fetch if ins]
        match fetch:
            case ['izq']:  # decode
                self.RBPos[1] -= 1   # execute
                if self.RBPos[1] < 0:
                    self.Estado = "dead"
                    return
            case ['der']:  # decode
                self.RBPos[1] += 1   # execute
                x, _ = self.RBPos
                if self.RBPos[1] >= len(self.Mapa[x]):
                    self.Estado = "dead"
                    return
        self.RIP += 1
        if self.RIP >= len(self.Instrucciones):
            self.Estado = "done"


class BoomeVirtualMachineCompleta(BoomeVirtualMachine):
    DIRECCIONES = {
        "arriba": (-1, 0), "abajo": (1, 0),
        "izq": (0, -1), "der": (0, 1)
    }

    def __init__(self):
        super().__init__()
    
        self.Mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.RBPos = [0, 0]
        self.BBPos = [7, 7]
        self.Error = None
        self.Pasos = 0

    def loadText(self, L):
        if not L or self.Estado != "wait":
            return (False, "No fue posible cargar el programa")
        self.Instrucciones = list(L)
        self.Estado = "ready"
        self.RIP = 0
        return (True,)

    def indice(self, registro):
        return int(registro[1])

    def valor(self, dato):
        if dato.startswith("R"):
            return self.Registros[self.indice(dato)]
        return int(dato[1:], 16)

    def bloqueado(self, direccion):
        dx, dy = self.DIRECCIONES[direccion]
        x = self.RBPos[0] + dx
        y = self.RBPos[1] + dy
        if not (0 <= x < len(self.Mapa) and 0 <= y < len(self.Mapa[x])):
            return True
        return self.Mapa[x][y] == 1

    def mover(self, direccion):
        if self.bloqueado(direccion):
            raise RuntimeError(f"movimiento {direccion} bloqueado")
        dx, dy = self.DIRECCIONES[direccion]
        self.RBPos[0] += dx
        self.RBPos[1] += dy
        if self.RBPos == self.BBPos:
            self.Estado = "success"

    def ejecutar_bloque(self, instrucciones, limite):
        for instruccion in instrucciones:
            if self.Estado != "ready":
                return
            self.Pasos += 1
            if self.Pasos > limite:
                raise RuntimeError("se alcanzo el limite seguro de instrucciones")

            match instruccion:
                case ("mover", direccion, linea):
                    self.mover(direccion)
                case ("asignar", destino, fuente, linea):
                    self.Registros[self.indice(destino)] = self.valor(fuente)
                case ("operar", destino, A, operador, B, linea):
                    a, b = self.valor(A), self.valor(B)
                    resultado = a + b if operador == "+" else a - b
                    self.Registros[self.indice(destino)] = resultado & 0xFFFF
                case ("sensor", destino, direccion, linea):
                    # #FFFF = bloqueado; #0000 = libre.
                    self.Registros[self.indice(destino)] = (
                        0xFFFF if self.bloqueado(direccion) else 0
                    )
                case ("si", registro, cuerpo, linea):
                    if self.valor(registro) != 0:
                        self.ejecutar_bloque(cuerpo, limite)
                case ("ciclo", registro, cuerpo, linea):
                    repeticiones = self.valor(registro)
                    for _ in range(repeticiones):
                        self.ejecutar_bloque(cuerpo, limite)
                        if self.Estado != "ready":
                            break

    def step(self, limite=10000):
        if self.Estado != "ready":
            return
        instruccion = self.Instrucciones[self.RIP]
        try:
            self.ejecutar_bloque([instruccion], limite)
            self.RIP += 1
            if self.Estado == "ready" and self.RIP >= len(self.Instrucciones):
                self.Estado = "done"
        except (RuntimeError, ValueError, IndexError) as error:
            self.Estado = "dead"
            self.Error = str(error)

    def run(self):
        while self.Estado == "ready":
            self.step()
        return self.Estado

    def __str__(self):
        texto = " | ".join(
            f"R{i}: #{valor & 0xFFFF:04X}"
            for i, valor in enumerate(self.Registros)
        ) + "\n"
        copia = [["X" if e == 1 else "." for e in fila] for fila in self.Mapa]
        bx, by = self.BBPos
        copia[bx][by] = "B"
        rx, ry = self.RBPos
        copia[rx][ry] = "*" if self.RBPos == self.BBPos else "R"
        texto += "\n".join(" ".join(fila) for fila in copia)
        obstaculos = [
            (x, y) for x, fila in enumerate(self.Mapa)
            for y, celda in enumerate(fila) if celda == 1
        ]
        texto += f"\nPosicion de Boome: {tuple(self.RBPos)}"
        texto += f"\nObstaculos: {obstaculos}"
        texto += f"\nEstado: {self.Estado}"
        if self.Error:
            texto += f"\nError controlado: {self.Error}"
        return texto
