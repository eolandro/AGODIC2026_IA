# ─────────────────────────────────────────────────────────────────────────────
# BVM.py  —  Boome Virtual Machine
# Máquina virtual que ejecuta el lenguaje Boome
# Enfoque: Programación Orientada a Objetos
# ─────────────────────────────────────────────────────────────────────────────

class BoomeVirtualMachine:

    # ── Símbolos para la representación en consola ───────────────────────────
    SIM_BOOME   = "R"
    SIM_BOMBA   = "B"
    SIM_OBST    = "1"
    SIM_LIBRE   = "0"
    SIM_BOOME_B = "X"   # Boome sobre la bomba

    def __init__(self):
        # Registros R0..R3
        self.Registros   = [0, 0, 0, 0]
        self.Instrucciones = []
        self.RIP         = None

        # Mapa: 0 = libre, 1 = obstáculo
        self.Mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.RBPos  = [0, 0]   # posición de Boome  [fila, columna]
        self.BBPos  = [5, 9]   # posición de la bomba
        self.Estado = "wait"   # wait | ready | done | dead
        self.Flujo  = None
        self.Actual = None

    # ── Generador de flujo (maneja Si y ciclo recursivamente) ────────────────
    def flujo(self, lineas):
        for L in lineas:
            if isinstance(L, list):
                match L:
                    case ["Si", Re, sub, "FinSi"]:
                        if self.Registros[int(Re[1])] != 0:
                            yield from self.flujo(sub)
                    case ["ciclo", Re, sub, "finciclo"]:
                        while self.Registros[int(Re[1])] != 0:
                            yield from self.flujo(sub)
            else:
                yield L

    # ── Carga el programa en la VM ────────────────────────────────────────────
    def loadText(self, L):
        if not L or self.Estado != "wait":
            return
        self.Instrucciones = list(L)
        self.Flujo  = self.flujo(self.Instrucciones)
        self.Actual = next(self.Flujo, None)
        self.RIP    = 0
        self.Estado = "ready" if self.Actual is not None else "done"

    # ── R003: Representación en consola ──────────────────────────────────────
    def __str__(self):
        lineas = []

        # ── Registros
        regs = " | ".join(f"R{i}: {self.Registros[i]:>4}" for i in range(4))
        lineas.append("┌─ Registros " + "─" * 30 + "┐")
        lineas.append(f"│  {regs}  │")
        lineas.append("└" + "─" * 43 + "┘")

        # ── Instrucción actual
        if self.Estado == "ready" and self.Actual:
            lineas.append(f"Por ejecutar: {self.Actual}")
        lineas.append("")

        # ── Mapa con Boome, bomba y obstáculos
        lineas.append("┌─ Mapa " + "─" * 36 + "┐")
        for f, fila in enumerate(self.Mapa):
            fila_str = "│ "
            for c, celda in enumerate(fila):
                pos = [f, c]
                if pos == self.RBPos and pos == self.BBPos:
                    fila_str += self.SIM_BOOME_B
                elif pos == self.RBPos:
                    fila_str += self.SIM_BOOME
                elif pos == self.BBPos:
                    fila_str += self.SIM_BOMBA
                elif celda == 1:
                    fila_str += self.SIM_OBST
                else:
                    fila_str += self.SIM_LIBRE
            fila_str += " │"
            lineas.append(fila_str)
        lineas.append("└" + "─" * 43 + "┘")

        # ── Estado
        estados = {
            "wait" : "Esperando programa",
            "ready": "En ejecucion",
            "done" : "Programa finalizado",
            "dead" : "Boome ha muerto",
        }
        lineas.append(f"Estado: {estados.get(self.Estado, self.Estado)}")
        lineas.append(f"Posición Boome: {self.RBPos}   Bomba: {self.BBPos}")

        return "\n".join(lineas)

    # ── R004: Ejecución de un paso sin romper la VM ───────────────────────────
    def step(self):
        if self.Estado != "ready":
            return

        instruccion = self.Actual
        tokens = [t for t in instruccion.split(" ") if t]

        match tokens:

            # movimientos
            case ["izq"]:
                self.RBPos[1] -= 1
                if self.RBPos[1] < 0:
                    self.Estado = "dead"
                    return

            case ["der"]:
                self.RBPos[1] += 1
                if self.RBPos[1] >= len(self.Mapa[self.RBPos[0]]):
                    self.Estado = "dead"
                    return

            case ["arriba"]:
                self.RBPos[0] -= 1
                if self.RBPos[0] < 0:
                    self.Estado = "dead"
                    return

            case ["abajo"]:
                self.RBPos[0] += 1
                if self.RBPos[0] >= len(self.Mapa):
                    self.Estado = "dead"
                    return

            # asign(R,"=",Nh) :- regs(R),numhex(Nh).
            case [R, "=", Nh] if Nh.startswith("#"):
                self.Registros[int(R[1])] = int(Nh[1:], 16)

            # asign(R,"=","sensor",M) :- regs(R),movs(M).
            case [R, "=", "sensor", M]:
                direcciones = {
                    "izq":    ( 0, -1),
                    "der":    ( 0,  1),
                    "arriba": (-1,  0),
                    "abajo":  ( 1,  0),
                }
                dx, dy = direcciones[M]
                nx = self.RBPos[0] + dx
                ny = self.RBPos[1] + dy
                fuera = nx < 0 or nx >= len(self.Mapa) or ny < 0 or ny >= len(self.Mapa[0])
                self.Registros[int(R[1])] = 1 if fuera else self.Mapa[nx][ny]

            # asign(R,"=",A,O,B) :- regs(R),opera(A,O,B).
            case [R, "=", A, O, B]:
                ValA = int(A[1:], 16) if A.startswith("#") else self.Registros[int(A[1])]
                ValB = int(B[1:], 16) if B.startswith("#") else self.Registros[int(B[1])]
                match O:
                    case "+": self.Registros[int(R[1])] = ValA + ValB
                    case "-": self.Registros[int(R[1])] = ValA - ValB

            case _:
                print(f"[BVM] Instrucción no reconocida: {tokens}")

        # verificar colisión con obstáculo
        fx, fy = self.RBPos
        if self.Mapa[fx][fy] == 1:
            self.Estado = "dead"
            return

        # verificar si llegó a la bomba
        if self.RBPos == self.BBPos:
            self.Estado = "dead"
            return

        # avanzar al siguiente paso del generador
        self.RIP   += 1
        self.Actual = next(self.Flujo, None)
        if self.Actual is None:
            self.Estado = "done"
