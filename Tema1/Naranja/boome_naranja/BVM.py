class BoomeVirtualMachine:
    NOMBRES_REGISTROS = {"R0": 0, "R1": 1, "R2": 2, "R3": 3}

    DELTA = {
        "arriba": (-1, 0),
        "abajo": (1, 0),
        "izq": (0, -1),
        "der": (0, 1),
    }

    def __init__(self):
        self.Registros = [0, 0, 0, 0]
        self.Instrucciones = []
        self.RIP = None
        
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
        self.Estado = "\nwait"
        self.ModoInteractivo = False
        self._fin_de = {}     
        self._inicio_de = {}   

    def loadText(self, L):
        if not L:
            return
        if not self.Estado == "\nwait":
            return
        self.Instrucciones = [
            a for a in L
        ]
        self.Estado = "\nready"
        self.RIP = 0
        self._recalcular_bloques()

    def iniciarInteractivo(self):
        if self.Estado != "\nwait":
            return
        self.ModoInteractivo = True
        self.Estado = "\nready"
        self.RIP = 0

    def agregarInstruccion(self, texto):
        self.Instrucciones.append(texto)
        self._recalcular_bloques()

    def _recalcular_bloques(self):
        self._fin_de = {}
        self._inicio_de = {}
        pila = []
        for i, texto in enumerate(self.Instrucciones):
            tokens = [t for t in texto.split(" ") if t]
            if tokens[:1] in (["Si"], ["ciclo"]):
                pila.append(i)
            elif tokens in (["FinSi"], ["finciclo"]) and pila:
                inicio = pila.pop()
                self._fin_de[inicio] = i
                self._inicio_de[i] = inicio

    def _hex_a_entero(self, literal):
        return int(literal[1:], 16)

    def _entero_a_hex(self, valor):
        valor &= 0xFFFF
        return f"#{valor:04X}"

    def _valor_de(self, token):
        if token in self.NOMBRES_REGISTROS:
            return self.Registros[self.NOMBRES_REGISTROS[token]]
        return self._hex_a_entero(token)

    def _dentro_del_mapa(self, x, y):
        return 0 <= x < len(self.Mapa) and 0 <= y < len(self.Mapa[0])

    def _hay_peligro(self, x, y):
        if not self._dentro_del_mapa(x, y):
            return True
        return self.Mapa[x][y] == 1

    def _revisar_posicion(self):
        x, y = self.RBPos
        if self._hay_peligro(x, y):
            self.Estado = "\ndead"
            return
        if self.RBPos == self.BBPos:
            self.Estado = "\nwin"

    def _marcar_fin_si_corresponde(self):
        if not self.ModoInteractivo and self.RIP >= len(self.Instrucciones):
            self.Estado = "\ndone"

    def __str__(self):
        S = f'R0 {self._entero_a_hex(self.Registros[0])} |'
        S += f'R1 {self._entero_a_hex(self.Registros[1])} |'
        S += f'R2 {self._entero_a_hex(self.Registros[2])} |'
        S += f'R3 {self._entero_a_hex(self.Registros[3])} |'
        S += "\n"
        if self.Estado == "\nready":
            S += f'Por ejecutar: {self.Instrucciones[self.RIP:]}'
        S += "\n"

        CM = [
            ['.' if celda == 0 else str(celda) for celda in fila]
            for fila in self.Mapa
        ]

        bx, by = self.BBPos
        if self._dentro_del_mapa(bx, by):
            CM[bx][by] = 'B'

        x, y = self.RBPos
        if self._dentro_del_mapa(x, y):
            CM[x][y] = 'R'

        for fila in CM:
            S += ' '.join(fila)
            S += "\n"

        S += f'Estado: {self.Estado}'
        return S


    def step(self):
        if self.Estado != "\nready":
            return
        if self.RIP >= len(self.Instrucciones):
            return  

        fetch = self.Instrucciones[self.RIP]
        tokens = [ins for ins in fetch.split(" ") if ins]

        match tokens:
            case ['izq'] | ['der'] | ['arriba'] | ['abajo']:  # decode
                dx, dy = self.DELTA[tokens[0]]
                self.RBPos[0] += dx  # execute
                self.RBPos[1] += dy
                self._revisar_posicion()
                if self.Estado != "\nready":
                    return
                self.RIP += 1

            case [R, "=", "sensor", D] if R in self.NOMBRES_REGISTROS:
                dx, dy = self.DELTA[D]
                x, y = self.RBPos
                peligro = self._hay_peligro(x + dx, y + dy)
                self.Registros[self.NOMBRES_REGISTROS[R]] = 1 if peligro else 0
                self.RIP += 1

            case [R, "=", A, Op, B] if (
                R in self.NOMBRES_REGISTROS and Op in ("+", "-")
            ):
                va = self._valor_de(A)
                vb = self._valor_de(B)
                resultado = va + vb if Op == "+" else va - vb
                self.Registros[self.NOMBRES_REGISTROS[R]] = resultado & 0xFFFF
                self.RIP += 1

            case [R, "=", V] if R in self.NOMBRES_REGISTROS:
                self.Registros[self.NOMBRES_REGISTROS[R]] = (
                    self._valor_de(V) & 0xFFFF
                )
                self.RIP += 1

            case ["Si", R] if R in self.NOMBRES_REGISTROS:
                cierre = self._fin_de.get(self.RIP, len(self.Instrucciones) - 1)
                if self.Registros[self.NOMBRES_REGISTROS[R]] != 0:
                    self.RIP += 1        
                else:
                    self.RIP = cierre + 1   

            case ["FinSi"]:
                self.RIP += 1  

            case ["ciclo", R] if R in self.NOMBRES_REGISTROS:
                cierre = self._fin_de.get(self.RIP, len(self.Instrucciones) - 1)
                if self.Registros[self.NOMBRES_REGISTROS[R]] != 0:
                    self.RIP += 1          
                else:
                    self.RIP = cierre + 1  

            case ["finciclo"]:
                self.RIP = self._inicio_de.get(self.RIP, self.RIP + 1)

            case _:
                self.Estado = "\ndead"
                return

        self._marcar_fin_si_corresponde()
