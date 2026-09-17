class BoomeVirtualMachine:
    def __init__(self):
        ################## R0, R1, R2, R3
        self.Registros = [0,0,0,0]
        self.RegMap = {"R0":0, "R1":1, "R2":2, "R3":3}
        self.Instrucciones = []
        self.RIP = None
        #####################
        self.Mapa = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,1,0],
            [0,0,1,0,0,0,0,1,0,0],
            [0,0,1,0,0,0,0,1,0,0],
            [0,1,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0],
        ]
        self.RBPos = [0,0]
        self.BBPos = [3,5]
        self.Estado = "wait"
        #direcciones de movimiento: (delta fila, delta columna)
        self.Direcciones = {
            "arriba": (-1,0),
            "abajo":  (1,0),
            "izq":    (0,-1),
            "der":    (0,1),
        }
        #orden en el que Boome prueba direcciones al toparse con algo:
        #gira en sentido horario (der -> abajo -> izq -> arriba -> der)
        self.OrdenDirecciones = ["der","abajo","izq","arriba"]

    def loadText(self, L):
        if not L:
            return
        if not self.Estado == 'wait':
            return
        #compilamos la estructura de bloques (Si/FinSi, ciclo/finciclo) en
        #una lista lineal de instrucciones con saltos, para que RIP pueda
        #controlar el flujo. Si L no trae bloques (solo strings), el
        #resultado es equivalente a la lista original.
        self.Instrucciones = self.compilar(L)
        self.Estado = "ready"
        self.RIP = 0

    #compilar: aplana recursivamente la estructura anidada que entrega
    #anlexsyn.construirBloques en una lista de:
    #   - strings: instrucciones tal cual (izq/der/arriba/abajo, asignaciones)
    #   - tuplas de control: ("JMPF", Registro, salto) / ("JMP", salto)
    #Convencion adoptada (la gramatica no la especifica): un bloque Si/ciclo
    #se ejecuta/repite mientras el registro indicado sea DISTINTO de 0. Esto
    #calza naturalmente con "R = sensor M", que deja 0/1 en el registro.
    #Los saltos son relativos (se suman a RIP), no absolutos, para que un
    #bloque compilado se pueda insertar en cualquier punto del programa.
    def compilar(self, bloques):
        Plano = []
        for elemento in bloques:
            match elemento:
                case ["Si", Re, Cuerpo, "FinSi"]:
                    CuerpoPlano = self.compilar(Cuerpo)
                    N = len(CuerpoPlano)
                    #si Re == 0: salta el propio JMPF (1) + todo el cuerpo (N)
                    Plano.append(("JMPF", Re, N + 1))
                    Plano += CuerpoPlano
                case ["ciclo", Re, Cuerpo, "finciclo"]:
                    CuerpoPlano = self.compilar(Cuerpo)
                    N = len(CuerpoPlano)
                    #si Re == 0: sale del ciclo saltando JMPF(1)+cuerpo(N)+JMP(1)
                    Plano.append(("JMPF", Re, N + 2))
                    Plano += CuerpoPlano
                    #al terminar el cuerpo, regresa a re-evaluar el JMPF
                    Plano.append(("JMP", -(N + 1)))
                case _:
                    Plano.append(elemento)
        return Plano

    def __str__(self):
        S  = f'R0: {self.Registros[0]} |'
        S += f'R1: {self.Registros[1]} |'
        S += f'R2: {self.Registros[2]} |'
        S += f'R3: {self.Registros[3]} |'
        S += "\n"
        if self.Estado == 'ready':
            Instruccion = self.Instrucciones[self.RIP]
            if isinstance(Instruccion, tuple):
                Instruccion = f"(salto interno: {Instruccion})"
            S += f"Por ejecutar: {Instruccion}"
            S += "\n"
        CM = [fila[::] for fila in self.Mapa]
        x,y = self.RBPos
        CM[x][y] = 'R'
        x,y = self.BBPos
        CM[x][y] = 'B'
        CM = [
            [
                str(e) for e in fila
            ] for fila in CM
        ]
        for fila in CM:
            S += ' '.join(fila)
            S += "\n"

        S += f"Estado: {self.Estado}"
        return S

    def step(self):
        if self.Estado != 'ready':
            return
        Instruccion = self.Instrucciones[self.RIP]
        if isinstance(Instruccion, tuple):
            self.ejecutarSalto(Instruccion)
            return
        fetch = Instruccion.split(" ")
        fetch = [ins for ins in fetch if ins]
        match fetch:
            case ['izq'] | ['der'] | ['arriba'] | ['abajo']: #decode
                self.mover(fetch[0]) #execute
                return
            case [R,"=","sensor",M]:
                self.leerSensor(R,M)
            case [R,"=",A,O,B]:
                self.operar(R,A,O,B)
            case [R,"=",Nh]:
                self.asignarValor(R,Nh)
            case _:
                #instruccion no reconocida por la VM (no deberia ocurrir si
                #el programa ya paso la validacion de anlexsyn)
                self.Estado = "dead"
                return

        self.RIP += 1
        if self.RIP >= len(self.Instrucciones):
            self.Estado = "done"

    #ejecuta el movimiento de Boome: si la direccion pedida esta bloqueada
    #(orilla del mapa, obstaculo o la bomba), Boome NO muere: gira en
    #sentido horario (der->abajo->izq->arriba) hasta encontrar una casilla
    #libre y se mueve ahi. Si las 4 direcciones estan bloqueadas, se queda
    #en su lugar (caso extremo, poco probable con el mapa actual).
    def mover(self, direccion):
        Direccion = direccion
        for _ in range(4):
            if self.puedeAvanzar(Direccion):
                dx,dy = self.Direcciones[Direccion]
                x,y = self.RBPos
                self.RBPos = [x+dx, y+dy]
                break
            Direccion = self.siguienteDireccion(Direccion)

        self.RIP += 1
        if self.RIP >= len(self.Instrucciones):
            self.Estado = "done"

    #revisa si la casilla en esa direccion es transitable: dentro del mapa,
    #sin obstaculo (1) y sin ser la bomba
    def puedeAvanzar(self, direccion):
        dx,dy = self.Direcciones[direccion]
        x,y = self.RBPos
        nx,ny = x+dx, y+dy
        if nx < 0 or nx >= len(self.Mapa) or ny < 0 or ny >= len(self.Mapa[nx]):
            return False
        if self.Mapa[nx][ny] == 1:
            return False
        if [nx,ny] == self.BBPos:
            return False
        return True

    #siguiente direccion en sentido horario
    def siguienteDireccion(self, direccion):
        idx = self.OrdenDirecciones.index(direccion)
        return self.OrdenDirecciones[(idx+1) % len(self.OrdenDirecciones)]

    #lee el sensor en una direccion relativa a Boome: 1 si hay algo que
    #bloquea (obstaculo, bomba o el borde del mapa), 0 si esta libre
    def leerSensor(self, R, M):
        dx,dy = self.Direcciones[M]
        x,y = self.RBPos
        nx,ny = x+dx, y+dy
        if nx < 0 or nx >= len(self.Mapa) or ny < 0 or ny >= len(self.Mapa[nx]):
            self.Registros[self.RegMap[R]] = 1
        elif [nx,ny] == self.BBPos:
            self.Registros[self.RegMap[R]] = 1
        else:
            self.Registros[self.RegMap[R]] = self.Mapa[nx][ny]

    #resuelve el valor de un operando: un registro o un literal numhex "#..."
    def valorDe(self, Operando):
        if Operando in self.RegMap:
            return self.Registros[self.RegMap[Operando]]
        return int(Operando[1:], 16)

    #ejecuta R = A O B (suma o resta)
    def operar(self, R, A, O, B):
        VA = self.valorDe(A)
        VB = self.valorDe(B)
        if O == "+":
            self.Registros[self.RegMap[R]] = VA + VB
        elif O == "-":
            self.Registros[self.RegMap[R]] = VA - VB

    #ejecuta R = #XXXX
    def asignarValor(self, R, Nh):
        self.Registros[self.RegMap[R]] = int(Nh[1:], 16)

    #ejecuta las instrucciones de control (JMPF/JMP) generadas por compilar()
    def ejecutarSalto(self, instruccion):
        match instruccion:
            case ("JMPF", Re, Salto):
                if self.Registros[self.RegMap[Re]] == 0:
                    self.RIP += Salto
                else:
                    self.RIP += 1
            case ("JMP", Salto):
                self.RIP += Salto
        if self.RIP >= len(self.Instrucciones):
            self.Estado = "done"
        elif self.RIP < 0:
            self.Estado = "dead"