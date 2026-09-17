def uhex(cadena_hex):
    if len(cadena_hex) != 1:
        return (False, "Longitud incorrecta")
    if cadena_hex.isdigit():
        return (True, )
    if cadena_hex in ["A", "B", "C", "D", "E", "F"]:
        return (True, )
    return (False, "No es valido")

def numhex(valor):
    match valor:
        case str():
            return numhex(list(valor))
        case ["#",A,B,C,D]:
            R = [uhex(A),uhex(B),uhex(C),uhex(D)]
            """
            #   [(True), (True), (True), (True)]
            #Forma uno de hacerlo 
            Valido == True
            for e in R:
                if e[0] == False:
                    Valido = False 
             """
            # Solucion 
            R = [ e for e in R if not e[0]]
            if not R: 
                return  (True, )
            return (False,R)
        case _:
            return (False,f"Eror desconocido en numhex: {valor}")

        #import anlexsyn 
        #anlexsyn.numher('0000')
        
def regs (valor):
    if valor in ["R0","R1", "R2", "R3"]:
        return (True, )
    return (False, f"{valor} no es un registro valido")

def opmat(valor):
    if valor in ["+", "-"]:
        return (True, )
    return (False, f"{valor} no es un operador valido")

def movs(valor):
    if valor in ["arriba", "abajo", "izq", "der"]:
        return (True, )
    return (False, f"{valor} no es un movimiento valido")

def opera(lista):
    match lista:
        case [A, B, C]:
            Oper = opmat(B)
            if len(Oper) != 1:
                return (False, [f"{lista} usa {Oper} y no es valido",Oper])
            R = [regs(A), regs(C)]
            N  = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True, )
            R = [regs(A), numhex(C)]
            N = [len(e) for e in R ]
            match N:
                case [1, 1]:
                    return (True, )
            R = [numhex(A), regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True, )
            R = [numhex(A), numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True, )

            return (False,[f"{lista} no es una operación valida"])
        
def asign(valor):
    match valor:
        case str():
            return asign([e for e in valor.split(' ') if e])

        # asign(R,"=",Nh) :- regs(R),numhex(Nh).
        case [R, "=", Nh]:
            RG = regs(R)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no valido",RG])
            Res = numhex(Nh)
            if len(Res) == 1:
                return (True, )
            return (False,Res)

        # asign(R,"=","sensor",M) :- regs(R),movs(M).
        case [R, "=", "sensor", M]:
            RG = regs(R)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no valido",RG])
            Res = movs(M)
            if len(Res) == 1:
                return (True, )
            return (False,Res)

        # asign(R,"=",A,O,B) :- regs(R),opera(A,O,B).
        case [R, "=", A, O, B]:
            RG = regs(R)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no valido",RG])
            Res = opera([A, O, B])
            if len(Res) == 1:
                return (True, )
            return (False,Res)
        case _:
            return (False,f"Error desconocido en asign: {valor}")
        
"""
linea(L) :- asign(L).
linea(L) :- movs(L).
linea(L) :- movs(L).
"""

def control(valor):
    if isinstance(valor, str):
        partes = valor.split()
        if len(partes) == 1 and partes[0] in ["FinSi", "finciclo"]:
            return (True, )
        if len(partes) == 2 and partes[0] in ["Si", "ciclo"]:
            if len(regs(partes[1])) == 1:
                return (True, )
    return (False, f"{valor} no es una instrucción de control valida")

def linea(valor):
    Res = control(valor)
    if len(Res) == 1:
        return (True, )
    Res = asign(valor)
    if len(Res) == 1:
        return (True, )
    Res = movs(valor)
    if len(Res) == 1:
        return (True, )
    return (False, f"{valor} no es una linea valida")
    
"""
lineas([L]) :- linea(L).
lineas([P | R]) :- linea(P), lineas(R).
"""

def lineas(valor):
    match valor:
        case [L]:
            Res = linea(L)
            if len(Res) == 1:
                return (True, )
            return (False, Res)
        case [P, *R]:
            Res = linea(P)
            if len(Res) != 1:
                return (False, Res)
            return lineas(R)
        case _:
            return (False, "Lista de lineas no valida")

"""
condicional("Si",Re,[F|R],"FinSi") :- regs(Re), lineas([F | R]).
"""

def condicional(valor):
    match valor:
        case ["Si", Re, [F, *R], "FinSi"]:
            RG = regs(Re)
            if len(RG) != 1:
                return (False, RG)
            Res = lineas([F, *R])
            if len(Res) == 1:
                return (True, )
            return (False, Res)
        case _:
            return (False, "Condicional no valido")

"""
# ciclos("ciclo",Re,[F | R],"finciclo") :- regs(Re), lineas([F | R]).
"""

def ciclos(valor):
    match valor:
        case ["ciclo", Re, [F, *R], "finciclo"]:
            RG = regs(Re)

            if len(RG) != 1:
                return (False, RG)

            Res = lineas([F, *R])

            if len(Res) == 1:
                return (True, )

            return (False, Res)

        case _:
            return (False, "Ciclo no valido")
