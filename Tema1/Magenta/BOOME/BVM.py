"""Máquina virtual de Boome."""

DIRECCIONES = {
    "arriba": (-1, 0),
    "abajo": (1, 0),
    "izq": (0, -1),
    "der": (0, 1),
}


class BoomeVirtualMachine:
    def __init__(self):
        self.Registros = [0, 0, 0, 0]
        self.Instrucciones = []
        self.RIP = 0
        self.Mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.RBPos = [0, 0]
        self.BBPos = [5, 7]
        self.Estado = "wait"
        self._flujo = None
        self.Actual = None
        self.Pasos = 0
        self.MaxPasos = 10000

    def LoadText(self, programa):
        if self.Estado != "wait":
            return
        self.Instrucciones = list(programa)
        self._flujo = self._ejecutar_bloques(self.Instrucciones)
        self.Actual = next(self._flujo, None)
        self.RIP = 0
        self.Estado = "ready" if self.Actual is not None else "done"

    def _ejecutar_bloques(self, elementos):
        for elemento in elementos:
            if isinstance(elemento, list):
                tipo, registro, cuerpo, _ = elemento
                if tipo == "Si":
                    if self._leer_registro(registro) != 0:
                        yield from self._ejecutar_bloques(cuerpo)
                else:
                    while self._leer_registro(registro) != 0:
                        yield from self._ejecutar_bloques(cuerpo)
            else:
                yield elemento

    def step(self):
        if self.Estado != "ready":
            return

        instrucciones = self.Actual.split()
        self._decodificar(instrucciones)

        if self.Estado != "ready":
            return

        self.Pasos += 1
        if self.Pasos > self.MaxPasos:
            self.Estado = "dead"
            return

        self.RIP += 1
        self.Actual = next(self._flujo, None)
        if self.Actual is None:
            self.Estado = "done"

    def _decodificar(self, partes):
        if len(partes) == 1 and partes[0] in DIRECCIONES:
            self._mover(partes[0])
            return

        if len(partes) == 4 and partes[1] == "=" and partes[2] == "sensor":
            destino, direccion = partes[0], partes[3]
            dx, dy = DIRECCIONES[direccion]
            x, y = self.RBPos
            valor = 1 if self._hay_obstaculo(x + dx, y + dy) else 0
            self._escribir_registro(destino, valor)
            return

        if len(partes) == 3 and partes[1] == "=":
            self._escribir_registro(partes[0], self._resolver(partes[2]))
            return

        if len(partes) == 5 and partes[1] == "=":
            izquierda = self._resolver(partes[2])
            derecha = self._resolver(partes[4])
            if partes[3] == "+":
                valor = izquierda + derecha
            else:
                valor = izquierda - derecha
            self._escribir_registro(partes[0], valor)

    def _mover(self, direccion):
        dx, dy = DIRECCIONES[direccion]
        x, y = self.RBPos
        nuevo = [x + dx, y + dy]

        if self._hay_obstaculo(*nuevo):
            self.Estado = "dead"
            return

        self.RBPos = nuevo
        if self.RBPos == self.BBPos:
            self.Estado = "boom"

    def _hay_obstaculo(self, x, y):
        fuera = not (0 <= x < len(self.Mapa) and 0 <= y < len(self.Mapa[0]))
        if fuera:
            return True
        return self.Mapa[x][y] == 1 or [x, y] == self.BBPos

    def _leer_registro(self, nombre):
        return self.Registros[int(nombre[1])]

    def _escribir_registro(self, nombre, valor):
        self.Registros[int(nombre[1])] = valor

    def _resolver(self, operando):
        if operando.startswith("R"):
            return self._leer_registro(operando)
        return int(operando[1:], 16)

    def __str__(self):
        tablero = [fila[:] for fila in self.Mapa]
        rx, ry = self.RBPos
        bx, by = self.BBPos
        tablero[rx][ry] = "R"
        tablero[bx][by] = "B"
        mapa = "\n".join(" ".join(str(celda) for celda in fila) for fila in tablero)
        siguiente = self.Actual if self.Estado == "ready" else "-"
        return (
            f"R0:{self.Registros[0]} | R1:{self.Registros[1]} | "
            f"R2:{self.Registros[2]} | R3:{self.Registros[3]}\n"
            f"RIP:{self.RIP} | Próxima: {siguiente}\n"
            f"{mapa}\nEstado: {self.Estado}"
        )
