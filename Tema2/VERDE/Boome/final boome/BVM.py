import random
from functools import reduce
from itertools import accumulate

################## Constantes del sensor (P(D+|...), tomadas de la imagen del Excel y del video)
P_D_BOMBA = 0.9   # P(D+ | bomba)
P_D_VACIA = 0.2   # P(D+ | vacia)
UMBRAL = 0.5      # usar desactivador si P(bomba) > 50%

################## Limites del lenguaje de Boom-e
REGS = ["R0", "R1", "R2", "R3"]   # solo 4 registros
DIRS = {"arriba": (-1, 0), "abajo": (1, 0), "izq": (0, -1), "der": (0, 1)}


################## Funciones puras (estilo funcional, como anlexsyn.py)

#valida_tablero: mismo formato de respuesta que anlexsyn: (True,) o (False, motivo)
#{"mapa": [[0,0,..],[0,1,..],..], "desactivadores": 6}   1 = bomba, 0 = vacia
def valida_tablero(datos):
    match datos:
        case {"mapa": mapa} if isinstance(mapa, list) and mapa and all(isinstance(f, list) and f for f in mapa):
            if len({len(f) for f in mapa}) != 1:
                return (False, "El mapa no es rectangular")
            if any(e not in (0, 1) for f in mapa for e in f):
                return (False, "El mapa solo admite 0 (vacia) y 1 (bomba)")
            if mapa[0][0] == 1:
                return (False, "Boom-e empieza en (0,0): no puede haber una bomba ahi")
            if not any(e == 1 for f in mapa for e in f):
                return (False, "El mapa debe tener al menos una bomba")
            Des = datos.get("desactivadores", 6)
            if not isinstance(Des, int) or isinstance(Des, bool) or Des < 1:
                return (False, "'desactivadores' debe ser un entero positivo")
            return (True,)
        case _:
            return (False, "Falta 'mapa' (una lista de filas con 0 y 1)")

#espiral(r0,r1,c0,c1): recorre el borde del rectangulo y luego el interior
#derecha -> abajo -> izquierda -> arriba, cerrando hacia adentro
def espiral(r0, r1, c0, c1):
    if r0 > r1 or c0 > c1:
        return []
    arriba = [(r0, c) for c in range(c0, c1 + 1)]
    derecha = [(r, c1) for r in range(r0 + 1, r1 + 1)]
    abajo = [(r1, c) for c in range(c1 - 1, c0 - 1, -1)] if r1 > r0 else []
    izq = [(r, c0) for r in range(r1 - 1, r0, -1)] if c1 > c0 else []
    return arriba + derecha + abajo + izq + espiral(r0 + 1, r1 - 1, c0 + 1, c1 - 1)

#vecino(pos, d): casilla a la que se llega desde pos con la direccion d
def vecino(pos, d):
    x, y = pos
    dx, dy = DIRS[d]
    return (x + dx, y + dy)

#direccion(a, b): nombre del movimiento que lleva de a a su casilla vecina b
def direccion(a, b):
    match (b[0] - a[0], b[1] - a[1]):
        case (-1, 0):
            return "arriba"
        case (1, 0):
            return "abajo"
        case (0, -1):
            return "izq"
        case (0, 1):
            return "der"
        case _:
            raise ValueError(f"{a} y {b} no son casillas vecinas")

#programa(ruta): en cada paso el sensor mira la casilla destino y luego se mueve
#solo usa instrucciones del lenguaje: "R0 = sensor der" y "der"
def programa(ruta):
    match ruta:
        case [a, b, *resto]:
            d = direccion(a, b)
            return [f"R0 = sensor {d}", d] + programa([b, *resto])
        case _:
            return []

#solo numeros positivos: una resta que daria negativo no existe
def suma(a, b):
    return (True, a + b)

def resta(a, b):
    if b > a:
        return (False, f"{a} - {b} daria un numero negativo")
    return (True, a - b)

#operando: un registro o un numero hex "#" + 4 digitos (0-9, A-F); None si no es valido
def operando(valor, registros):
    match valor:
        case "R0" | "R1" | "R2" | "R3":
            return registros[REGS.index(valor)]
        case str() if valor.startswith("#") and len(valor) == 5 and all(c in "0123456789ABCDEF" for c in valor[1:]):
            return int(valor[1:], 16)
        case _:
            return None

#previo = bombas restantes / casillas sin revisar
def previo_bomba(bombas_restantes, casillas_sin_revisar):
    return bombas_restantes / casillas_sin_revisar

#P(Boom|D+) = P(D+|Boom)*P(Boom) / (P(D+|Boom)*P(Boom) + P(D+|vacia)*P(vacia))
def bayes(p):
    num = P_D_BOMBA * p
    return num / (num + P_D_VACIA * (1 - p))

#el sensor: True = D+, False = D-. Boom-e solo ve esto, nunca hay_bomba
def lectura(hay_bomba, azar):
    return azar.random() < (P_D_BOMBA if hay_bomba else P_D_VACIA)

#chequeos: hasta 3 lecturas; si las 2 primeras son negativas se corta (no hay 3ra)
def chequeos(hay_bomba, azar, lecturas=()):
    match lecturas:
        case (False, False):
            return lecturas
        case (_, _, _):
            return lecturas
        case _:
            return chequeos(hay_bomba, azar, lecturas + (lectura(hay_bomba, azar),))

#solo los positivos actualizan; cada posterior es el previo del siguiente
def posterior(previo, lecturas):
    return reduce(lambda p, d: bayes(p) if d else p, lecturas, previo)

#trayectoria: P(bomba) despues de cada tirada (la ultima es el posterior final)
#ej: (D+, D-, D+) -> [p1, p1, p3]
def trayectoria(previo, lecturas):
    return list(accumulate(lecturas, lambda p, d: bayes(p) if d else p, initial=previo))[1:]


class BoomeVirtualMachine:
    def __init__(self, tablero):
        ################## R0, R1, R2, R3
        # R0: D+ de la ultima casilla revisada (0 a 3)
        # R1: tiradas hechas en esa casilla (2 o 3)
        # R2: desactivadores restantes
        # R3: bombas desactivadas
        self.Registros = [0, 0, tablero.get("desactivadores", 6), 0]
        self.Instrucciones = []   # instrucciones del lenguaje: "R0 = sensor der", "der", ...
        self.RIP = None
        #####################
        self.Mapa = [[0 for _ in fila] for fila in tablero["mapa"]]
        self.RBPos = (0,0)
        # las bombas salen del tablero (1 = bomba); Boom-e no las conoce
        self.BBPos = [
            (x, y) for x, fila in enumerate(tablero["mapa"])
            for y, e in enumerate(fila) if e == 1
        ]
        self.Desactivadas = []        # bombas desactivadas con exito
        self.Revisadas = [(0,0)]      # casilla de inicio ya cuenta como visitada
        self.Armado = None            # casilla donde se uso el desactivador (para el siguiente movimiento)
        self.Ultima = None            # ultima instruccion ejecutada
        self.Lecturas = ()            # ultimas lecturas (True = D+)
        self.Previo = None            # previo de la ultima casilla revisada
        self.Trayectoria = []         # P(bomba) tras cada tirada de la ultima casilla
        self.Prob = None              # ultimo posterior de bomba
        self.Accion = None            # que hizo Boom-e con esa casilla
        self.Azar = random.SystemRandom()   # basado en os.urandom
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

    def dentro(self, pos):
        x, y = pos
        return 0 <= x < len(self.Mapa) and 0 <= y < len(self.Mapa[0])

    def __str__(self):
        total = len(self.Mapa) * len(self.Mapa[0])
        revisadas = len(self.Revisadas)
        S  = f'R0: {self.Registros[0]} |'
        S += f'R1: {self.Registros[1]} |'
        S += f'R2: {self.Registros[2]} |'
        S += f'R3: {self.Registros[3]} |'
        S += "\n"
        S += f'Revisadas: {revisadas} | Por revisar: {total - revisadas} |'
        S += f' Bombas desactivadas: {len(self.Desactivadas)} |'
        S += f' Bombas restantes: {len(self.BBPos) - len(self.Desactivadas)} |'
        S += f' Desactivadores: {self.Registros[2]}'
        S += "\n"
        S += f'Posicion: {self.RBPos}'
        if self.Prob is not None:
            S += f' | Previo: {self.Previo:.2%} | P(bomba) final: {self.Prob:.2%}'
        S += "\n"
        #resultado de cada tirada; en cada D+ se muestra el calculo de Bayes
        antes = [self.Previo] + self.Trayectoria
        for i, (d, a, p) in enumerate(zip(self.Lecturas, antes, self.Trayectoria), 1):
            if d:
                S += (f'  Tirada {i}: D+ -> {P_D_BOMBA}*{a:.4f} / '
                      f'({P_D_BOMBA}*{a:.4f} + {P_D_VACIA}*{1 - a:.4f}) = {p:.2%}\n')
            else:
                S += f'  Tirada {i}: D- -> sin cambio, P(bomba) = {p:.2%}\n'
        if self.Prob is not None and len(self.Lecturas) == 2:
            S += '  Sin 3ra tirada (2 negativos seguidos)\n'
        if self.Accion:
            S += f'  {self.Accion}\n'
        if self.Estado == 'ready':
            S += f"Por ejecutar {self.Instrucciones[self.RIP]}"
            S += "\n"
        CM = [fila[::] for fila in self.Mapa]
        for x,y in self.Revisadas:
            CM[x][y] = 1
        for x,y in self.BBPos:
            CM[x][y] = 'D' if (x,y) in self.Desactivadas else 'B'
        x,y = self.RBPos
        CM[x][y] = 'X' if self.Estado == 'dead' else 'R'
        CM = [
            [
                str(e) for e in fila
            ] for fila in CM
        ]
        for fila in CM:
            S += ' '.join(fila)
            S += "\n"

        S += f"Estado {self.Estado}"
        return S

    #R = sensor d: revisa la casilla vecina antes de moverse (2 o 3 tiradas con Bayes)
    #R recibe los D+ obtenidos; si P(bomba) > 50% se gasta un desactivador en esa casilla
    def sensor(self, R, d):
        destino = vecino(self.RBPos, d)
        if not self.dentro(destino):
            self.Estado = "dead"
            return
        total = len(self.Mapa) * len(self.Mapa[0])
        previo = previo_bomba(
            len(self.BBPos) - len(self.Desactivadas),
            max(1, total - len(self.Revisadas)))
        hay_bomba = destino in self.BBPos      # solo lo usa el sensor, Boom-e no lo ve
        self.Lecturas = chequeos(hay_bomba, self.Azar)
        self.Previo = previo
        self.Trayectoria = trayectoria(previo, self.Lecturas)
        self.Prob = posterior(previo, self.Lecturas)
        self.Registros[1] = len(self.Lecturas)
        self.Registros[R] = sum(self.Lecturas)
        if self.Prob > UMBRAL and self.Registros[2] > 0:
            match resta(self.Registros[2], 1):
                case (True, v):
                    self.Registros[2] = v
                    self.Armado = destino
            self.Accion = 'Desactivador usado'
        elif self.Prob > UMBRAL:
            self.Accion = 'P > 50% pero sin desactivadores: avanza igual'
        else:
            self.Accion = 'P <= 50%: avanza sin desactivador'

    #d: se mueve a la casilla vecina; pisar una bomba sin desactivador es morir
    def mover(self, d):
        destino = vecino(self.RBPos, d)
        if not self.dentro(destino):
            self.Estado = "dead"
            return
        self.RBPos = destino
        if destino not in self.Revisadas:
            self.Revisadas.append(destino)
        if destino in self.BBPos and destino not in self.Desactivadas:
            if self.Armado != destino:
                self.Estado = "dead"
                return
            self.Desactivadas.append(destino)
            self.Registros[3] = suma(self.Registros[3], 1)[1]
        self.Armado = None
        if len(self.Desactivadas) == len(self.BBPos):
            self.Estado = "done"

    #R = A + B / R = A - B (solo positivos, sin multiplicar ni dividir)
    def opera(self, R, A, O, B):
        VA, VB = operando(A, self.Registros), operando(B, self.Registros)
        if VA is None or VB is None:
            self.Estado = "error"
            return
        match (suma if O == "+" else resta)(VA, VB):
            case (True, v):
                self.Registros[R] = v
            case _:
                self.Estado = "error"

    def step(self):
        if self.Estado != 'ready':
            return
        fetch = self.Instrucciones[self.RIP]
        self.Ultima = fetch
        decode = [ins for ins in fetch.split(" ") if ins]
        match decode:
            case ["arriba" | "abajo" | "izq" | "der" as d]:
                self.mover(d) #execute
            case [R, "=", "sensor", d] if R in REGS and d in DIRS:
                self.sensor(REGS.index(R), d)
            case [R, "=", Nh] if R in REGS and operando(Nh, self.Registros) is not None and Nh.startswith("#"):
                self.Registros[REGS.index(R)] = operando(Nh, self.Registros)
            case [R, "=", A, ("+" | "-") as O, B] if R in REGS:
                self.opera(REGS.index(R), A, O, B)
            case _:
                self.Estado = "error"
        if self.Estado != 'ready':
            return

        self.RIP += 1
        if self.RIP >= len(self.Instrucciones):
            self.Estado = "done"
