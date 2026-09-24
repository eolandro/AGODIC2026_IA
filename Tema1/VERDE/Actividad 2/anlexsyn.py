def uhex(cadena_hex):
    if len(cadena_hex) != 1:
        return (False, "Longitud incorrecta")
    if cadena_hex.isdigit():
        return (True,)
    if cadena_hex in ["A", "B", "C", "D", "E", "F"]:
        return (True,)
    return(False, "No es valido")

def numhex(valor):
    match valor:
        case str():
            return numhex(list(valor))
        case ["#",A,B,C,D]:
            R = [uhex(A),uhex(B),uhex(C),uhex(D)]
            # [(True,),(True,),(True,),(True,)]
            '''
            Valido = True
            for e in R:
                if e[0] == False:
                    Valido = False
            '''
            R = [ e for e in R if not e[0]]
            if not R:
                return (True,)
            return(False, R)
        case _:
            return (False,f"Error desconocido en numhex: {valor}")

def regs(valor):
    if valor in ["R0","R1","R2","R3"]:
        return (True,)
    return (False, f"{valor} no es un registro valido")

def opmat(valor):
    if valor in ["+","-"]:
        return (True,)
    return (False, f"{valor} no es un operador valido")

def movs(valor):
    if valor in ["arriba","abajo","izq","der"]:
        return (True,)
    return (False, f"{valor} no es un movimiento valido")

#opera(A,B,C) :- regs(A), opmat(B), regs(C).
def opera(lista):
    match lista:
        case [A,B,C]:
            Oper = opmat(B)
            if len(Oper) != 1:
                return (False, [f"{lista} usa {Oper} y no es valido",Oper])
            ###opera(A,B,C) :- regs(A),opmat(B),regs(C).
            R = [regs(A),regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,)
            ###opera(A,B,C) :- regs(A),opmat(B),numhex(C).
            R = [regs(A),numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,)
            ###opera(A,B,C) :- numhex(A),opmat(B),regs(C).
            R = [numhex(A),regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,)
            ###opera(A,B,C) :- numhex(A),opmat(B),numhex(C).
            R = [numhex(A),numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,)
            return (False, f"{lista} no es una operacion valida")

#asign(R,"=",Nh) :- regs(R),numhex(Nh).
#asign(R,"=","sensor",M) :- regs(R),movs(M).
#asign(R,"=",A,O,B) :- regs(R),opera(A,O,B).
def asign(valor):
    match valor:
        case str():
            return asign([e for e in valor.split(' ') if e])
        case [R,"=",Nh]:
            RG = regs(R)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no valido",RG])
            Nu = numhex(Nh)
            if len(Nu) != 1:
                return (False,[f"{valor} tiene un valor no valido",Nu])
            return (True,)
        case [R,"=","sensor",M]:
            RG = regs(R)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no valido",RG])
            Mv = movs(M)
            if len(Mv) != 1:
                return (False,[f"{valor} tiene un movimiento no valido",Mv])
            return (True,)
        case [R,"=",A,O,B]:
            RG = regs(R)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no valido",RG])
            Res = opera([A,O,B])
            if len(Res) == 1:
                return (True,)
            return (False,Res)
        case _:
            return (False, f"Error desconocido en asign: {valor}")

#linea(L) :- asign(L).
#linea(L) :- movs(L).
#Extension: una linea tambien puede ser un bloque Si/FinSi o ciclo/finciclo
#ya armado por construirBloques, para poder validar programas con control de flujo.
def linea(valor):
    match valor:
        case str():
            Res = asign(valor)
            if len(Res) == 1:
                return (True,)
            Mov = movs(valor)
            if len(Mov) == 1:
                return (True,)
            return (False, [f"{valor} no es una linea valida", Res, Mov])
        case ["Si", *_]:
            return condicional(valor)
        case ["ciclo", *_]:
            return ciclos(valor)
        case _:
            return (False, f"Error desconocido en linea: {valor}")

#lineas([L]) :- linea(L).
#lineas([P | R]) :- linea(P), lineas(R).
def lineas(valor):
    match valor:
        case [L]:
            Res = linea(L)
            if len(Res) == 1:
                return (True,)
            return (False, [f"{valor} no son lineas validas", Res])
        case [P, *R]:
            Res = linea(P)
            if len(Res) != 1:
                return (False, [f"{valor} no son lineas validas", Res])
            return lineas(R)
        case _:
            return (False, f"Error desconocido en lineas: {valor}")

#bloque generico: Apertura Re [F|R] Cierre :- regs(Re), lineas([F | R]).
#usado por condicional y ciclos para no repetir la misma validacion
def bloque(apertura, cierre, valor):
    match valor:
        case [A, Re, [F, *R], C] if A == apertura and C == cierre:
            RG = regs(Re)
            if len(RG) != 1:
                return (False, [f"{valor} tiene un registro no valido", RG])
            Li = lineas([F, *R])
            if len(Li) != 1:
                return (False, [f"{valor} tiene lineas no validas", Li])
            return (True,)
        case _:
            return (False, f"Error desconocido en bloque {apertura}/{cierre}: {valor}")

#condicional("Si",Re,[F|R],"FinSi") :- regs(Re), lineas([F | R]).
def condicional(valor):
    return bloque("Si", "FinSi", valor)

#ciclos("ciclo",Re,[F | R],"finciclo") :- regs(Re), lineas([F | R]).
def ciclos(valor):
    return bloque("ciclo", "finciclo", valor)

#construirBloques: a partir de la lista PLANA de lineas de texto que entrega
#Boome.py (ya sin tabuladores/saltos de linea), arma recursivamente la
#estructura anidada que esperan condicional/ciclos, es decir convierte:
#   "Si R0"
#   "izq"
#   "FinSi"
#en:
#   ["Si", "R0", ["izq"], "FinSi"]
#Devuelve (bloques_construidos, lineas_restantes_sin_consumir).
#"cierre" es None a nivel de programa (no se espera ningun cierre especifico)
#y toma el valor "FinSi"/"finciclo" cuando se esta armando el cuerpo de un bloque.
#Las palabras clave se reconocen SIN importar mayusculas/minusculas (Ciclo,
#CICLO, finCiclo, si, SI, etc. son equivalentes), pero siempre se construyen
#en su forma canonica ("Si"/"FinSi"/"ciclo"/"finciclo") para que coincida
#con lo que espera bloque()/condicional()/ciclos().
def construirBloques(lineas, cierre=None):
    match lineas:
        case []:
            #si esperabamos un cierre ("FinSi"/"finciclo") y el archivo se
            #acabo antes de encontrarlo, dejamos una marca que hara fallar
            #la validacion en linea()/asign()/movs() con un mensaje claro.
            if cierre is not None:
                return ([f"<se esperaba {cierre} y no se encontro>"], [])
            return ([], [])
        case [linea, *resto] if cierre is not None and linea.lower() == cierre.lower():
            return ([], resto)
        case [linea, *resto]:
            partes = [t for t in linea.split(' ') if t]
            match partes:
                case [Apertura, Re] if Apertura.lower() == "si":
                    Cuerpo, Resto = construirBloques(resto, "FinSi")
                    Siguientes, Final = construirBloques(Resto, cierre)
                    return ([["Si", Re, Cuerpo, "FinSi"], *Siguientes], Final)
                case [Apertura, Re] if Apertura.lower() == "ciclo":
                    Cuerpo, Resto = construirBloques(resto, "finciclo")
                    Siguientes, Final = construirBloques(Resto, cierre)
                    return ([["ciclo", Re, Cuerpo, "finciclo"], *Siguientes], Final)
                case _:
                    Siguientes, Final = construirBloques(resto, cierre)
                    return ([linea, *Siguientes], Final)