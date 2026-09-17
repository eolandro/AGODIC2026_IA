class BoomeVirtualMachine:

    def __init__(self):# necesitamos inicializar memoria de un clase con init qu es constructor
        ##################r0,r1,r2,r3
        self.Registros = [0, 0, 0, 0]
        self.Instrucciones = []
        self.RIP= None   #intruccion pointer no debe estar en ningun lugar 
        
        self.Mapa =[
            #0  1  2  3  4  5
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#0
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],#1
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],#2
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],#3 
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],#4
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #5
              
        ]
        self.RBPos =[0,0] #robot boomi posicion 
        self.BBPos =[3,5] #bomba posicion 
        self.Estado ="wait"
        
    def loadText(self,L):#txt igual a cargar intruccion  tiene lista compoparametro 
        if not L:
            return
        if not self.Estado =="wait":
            return
        self.Instrucciones =[
            a for a in L
        ]
        self.Estado ="ready"
        self.RIP= 0
        
    def __str__(self):
        S =  f'R0:{self.Registros[0]} |'
        S += f'R1:{self.Registros[1]} |'
        S += f'R2:{self.Registros[2]} |'
        S += f'R3:{self.Registros[3]} |'
        S += "\n"
        if self.Estado == "ready" and self.RIP < len(self.Instrucciones):
            S += f"Por ejecutar:{self.Instrucciones[self.RIP]}"     
        S += "\n"
        
        CM = [fila[::] for fila in self.Mapa]
        if self.Estado in ["ready", "wait", "done"]:
            x, y = self.RBPos
            CM[x][y] = 'R'
        x, y = self.BBPos
        CM[x][y] = 'B'
        CM = [[str(e) for e in fila] for fila in CM]
        
        for fila in CM:
            S += ' '.join(fila)
            S += "\n"
        S += f"Estado {self.Estado}"
        return S
            
    def step (self):
        if self.Estado !="ready":
            return
        # --- PROTECCIÓN OBLIGATORIA AL INICIO DE STEP ---
        if self.RIP >= len(self.Instrucciones):
            self.Estado = "done"
            return
        fetch = self.Instrucciones [self.RIP]
        fetch = fetch.split(" ")
        fetch = [ins for ins in fetch if ins]
        match fetch:
            
            case ['izq']:
                self.RBPos[1] -=1 #Execute
                if self.RBPos[1] < 0:
                    self.Estado ="dead"
                    return
            case ['der']:
                self.RBPos[1] +=1 #Execute
                x,_=self.RBPos
                if self.RBPos[1] >= len(self.Mapa[x]):
                    self.Estado ="dead"
                    return
            case ['arriba']:
                self.RBPos[0] -= 1  # Fila arriba
                if self.RBPos[0] < 0:
                    self.Estado = "dead"
                    return

            case ['abajo']:
                self.RBPos[0] += 1  # Fila abajo
                if self.RBPos[0] >= len(self.Mapa):
                    self.Estado = "dead"
                    
# --- CONTROL DE FLUJO: CICLOS PLANOS ---
            case ["ciclo", R] if R in ["R0", "R1", "R2", "R3"]:
                pos = int(R[1])
                if self.Registros[pos] == 0:
                    nivel = 1
                    while nivel > 0 and self.RIP < len(self.Instrucciones) - 1:
                        self.RIP += 1
                        sig = [ins for ins in self.Instrucciones[self.RIP].split(" ") if ins]
                        if sig and sig[0].lower() == "ciclo":
                            nivel += 1
                        elif sig and sig[0].lower() == "finciclo":
                            nivel -= 1
                    self.RIP += 1
                    return

            case ["finciclo"]:
                nivel = 1
                temp_rip = self.RIP
                while nivel > 0 and temp_rip > 0:
                    temp_rip -= 1
                    prev = [ins for ins in self.Instrucciones[temp_rip].split(" ") if ins]
                    if prev and prev[0].lower() == "finciclo":
                        nivel += 1
                    elif prev and prev[0].lower() == "ciclo":
                        nivel -= 1
                self.RIP = temp_rip
                return

            # --- CONTROL DE FLUJO: CONDICIONALES PLANOS ---
            case ["Si", R] if R in ["R0", "R1", "R2", "R3"]:
                pos = int(R[1])
                if self.Registros[pos] == 0:
                    nivel = 1
                    while nivel > 0 and self.RIP < len(self.Instrucciones) - 1:
                        self.RIP += 1
                        sig = [ins for ins in self.Instrucciones[self.RIP].split(" ") if ins]
                        if sig and sig[0].lower() == "si":
                            nivel += 1
                        elif sig and sig[0].lower() == "finsi":
                            nivel -= 1
                    self.RIP += 1
                    return

            case ["FinSi"]:
                self.RIP += 1
                if self.RIP >= len(self.Instrucciones):
                    self.Estado = "done"
                return

            # --- ASIGNACIÓN HEXADECIMAL DIRECTO (Estructura del Profe) ---
            case [R, "=", Nh] if R in ["R0", "R1", "R2", "R3"] and Nh[0] == "#":
                posicion = int(R[1])
                self.Registros[posicion] = int(Nh[1:], 16)

            # --- ASIGNACIÓN CON SENSOR (Estructura del Profe) ---
            case [R, "=", "sensor", Mov] if R in ["R0", "R1", "R2", "R3"]:
                posicion = int(R[1])
                x, y = self.RBPos[0], self.RBPos[1]

                if Mov == "arriba": x -= 1
                if Mov == "abajo":  x += 1
                if Mov == "izq":    y -= 1
                if Mov == "der":    y += 1

                if 0 <= x < len(self.Mapa) and 0 <= y < len(self.Mapa[0]):
                    self.Registros[posicion] = self.Mapa[x][y]
                else:
                    self.Registros[posicion] = 1

            # --- ASIGNACIÓN CON OPERACIONES (Estructura del Profe) ---
            case [R, "=", A, O, B] if R in ["R0", "R1", "R2", "R3"] and O in ["+", "-"]:
                posicion = int(R[1])
                valA = self.Registros[int(A[1])] if A in ["R0", "R1", "R2", "R3"] else int(A[1:], 16)
                valB = self.Registros[int(B[1])] if B in ["R0", "R1", "R2", "R3"] else int(B[1:], 16)

                if O == "+":
                    self.Registros[posicion] = (valA + valB)%2
                if O == "-":
                    self.Registros[posicion] = (valA - valB)%2

        # Comprobar si chocó con un obstáculo del mapa (1) o con la bomba
        x, y = self.RBPos
        if self.Mapa[x][y] == 1 or self.RBPos == self.BBPos:
            self.Estado = "dead"
            return

        self.RIP += 1
        if self.RIP >= len(self.Instrucciones):
            self.Estado = "done"



        