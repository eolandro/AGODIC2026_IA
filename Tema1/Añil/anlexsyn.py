def uhex (cadena_hex):
    if len(cadena_hex) !=1:
        return (False,"Longitud incorrecta")
    if cadena_hex.isdigit():
        return (True,)
        #return Tuple(True)
    if cadena_hex in ["A","B","C","D","E","F"]:
        return (True,)
    return (False,"No es válido")

def numhex(valor):
    match valor:
        case str():
            return numhex(list(valor))
        case ["#",A,B,C,D]:
            R = [uhex(A),uhex(B),uhex(C),uhex(D)]
            #[(True,), (True,), (True,), (True,)]
            """
            Valido = True
            for e in R:
                if e[0] == False:
                    Valido = False
            """
            R = [e for e in R if not e[0]]
            if not R:
                return (True,)
            return (False,R)
        case _:
            return (False,f"Error desconocido en NumHex: {valor}")

def regs(valor):
    if valor in ["R0","R1","R2","R3"]:
        return (True,)
    return (False,f"{valor} no es un registro válido")

def opmat(valor):
    if valor in ["+","-"]:
        return (True,)
    return (False,f"{valor} no es un operador válido")

def movs(valor):
    if valor in ["arriba","abajo","izq","der"]:
        return (True,)
    return (False,f"{valor} no es un movimiento válido")

def opera(lista):
    match lista:
        case [A,B,C]:
            Oper = opmat(B)
            if len(Oper) != 1:
                return (False,[f"{lista} usa {Oper} y no es válido",Oper])
            #opera(A,B,C) :- regs(A),opmat(B),regs(C).
            R = [regs(A),regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,)
            #opera(A,B,C) :- regs(A),opmat(B),numhex(C).
            R = [regs(A),numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,)         
            #opera(A,B,C) :- numhex(A),opmat(B),regs(C).
            R = [numhex(A),regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,) 
            #opera(A,B,C) :- numhex(A),opmat(B),numhex(C).
            R = [numhex(A),numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,) 
            return (False,[f"{lista} no es una operación válida"])

def asign(valor):
    match valor:
        case str():
            return asign([e for e in valor.split(' ') if e])
        #asign(R,"=",Nh) :- regs(R),numhex(Nh).
        case [R,"=",Nh]:
            RG = regs(R)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no válido",RG])
            NH = numhex(Nh)
            if len(NH) != 1:
                return (False,[f"{valor} tiene un numhex no válido",NH])
            return (True,)
        #asign(R,"=","sensor",M) :- regs(R),movs(M).
        case [R,"=","sensor",M]:
            RG = regs(R)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no válido",RG])
            MV = movs(M)
            if len(MV) != 1:
                return (False,[f"{valor} tiene un movimiento no válido",MV])
            return (True,)
        #asign(R,"=",A,O,B) :- regs(R),opera(A,O,B).
        case [R,"=",A,O,B]:
            RG = regs(R)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no válido",RG])
            Res = opera([A,O,B])
            if len(Res) == 1:
                return (True,)
            return (False,Res)
        case _:
            return (False,f"Error desconocido en asign: {valor}")

#linea(L) :- asign(L).
#linea(L) :- movs(L).
#linea(L) :- asign(L).
#linea(L) :- movs(L).
def linea(valor):
    L1 = asign(valor)
    if len(L1) == 1:
        return (True,)
    L2 = movs(valor)
    if len(L2) == 1:
        return (True,)
    if isinstance(valor,list):
        L3 = condicional(valor)
        if len(L3) == 1:
            return (True,)
        L4 = ciclos(valor)
        if len(L4) == 1:
            return (True,)
        return (False,[f"{valor} no es una línea válida",L1,L2,L3,L4])
    return (False,[f"{valor} no es una línea válida",L1,L2])

#lineas([L]) :- linea(L).
#lineas([P | R]) :- linea(P), lineas(R).
def lineas(lista):
    match lista:
        case [L]:
            R = linea(L)
            if len(R) == 1:
                return (True,)
            return (False,R)
        case [P,*R]:
            RP = linea(P)
            if len(RP) != 1:
                return (False,[f"{P} no es una línea válida",RP])
            return lineas(R)
        case _:
            return (False,f"Error desconocido en lineas: {lista}")

#condicional("Si",Re,[F|R],"FinSi") :- regs(Re), lineas([F | R]).
def condicional(valor):
    match valor:
        case ["Si",Re,[F,*R],"FinSi"]:
            RG = regs(Re)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no válido",RG])
            L = lineas([F,*R])
            if len(L) != 1:
                return (False,[f"{valor} tiene líneas no válidas",L])
            return (True,)
        case _:
            return (False,f"Error desconocido en condicional: {valor}")

#ciclos("ciclo",Re,[F | R],"finciclo") :- regs(Re), lineas([F | R]).
def ciclos(valor):
    match valor:
        case ["ciclo",Re,[F,*R],"finciclo"]:
            RG = regs(Re)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no válido",RG])
            L = lineas([F,*R])
            if len(L) != 1:
                return (False,[f"{valor} tiene líneas no válidas",L])
            return (True,)
        case _:
            return (False,f"Error desconocido en ciclos: {valor}")