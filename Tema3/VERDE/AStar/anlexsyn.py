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

def asign(valor):
    match valor:
        case str():
            return asign([e for e in valor.split(' ') if e])
        case [R,"=",A,0,B]:
            RG = regs(R)
            if len(RG) != 1:
                return (False,[f"{valor} tiene un registro no valido",RG])
            Res = opera(A,0,B)
            if len(Res) == 1:
                return (True,)
            return (False,Res)
        case _:
            return (False, f"Error desconocido en asign: {valor}")

#linea(L) :- asign(L).
#linea(L) :- movs(L).
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

############ Tablero (A*) ############
TAM = 10

#simbolo(0). simbolo("0"). simbolo("X"). simbolo("R"). simbolo("B").
#en el JSON el vacio se acepta como 0 (numero) o "0" (texto)
def simbolo(valor):
    match valor:
        case 0 if type(valor) is int:
            return (True,)
        case "0" | "X" | "R" | "B":
            return (True,)
        case _:
            return (False, f"{valor!r} no es un simbolo valido (usa 0, X, R o B)")

#fila([S1,...,S10]) :- simbolo(S1), ..., simbolo(S10).
def fila(valor):
    match valor:
        case list() if len(valor) == TAM:
            R = [simbolo(e) for e in valor]
            return (True,) if all(e[0] for e in R) else (False, [e[1] for e in R if not e[0]])
        case list():
            return (False, [f"debe tener {TAM} columnas y tiene {len(valor)}"])
        case _:
            return (False, ["no es una lista de simbolos"])

#piezas(Tablero) :- exactamente un "R" y exactamente un "B".
def piezas(valor):
    planos = [str(e) for f in valor for e in f]
    R = [(s, planos.count(s)) for s in ["R", "B"]]
    R = [f"debe haber exactamente 1 {'robot (R)' if s == 'R' else 'bomba (B)'} y hay {n}"
         for s, n in R if n != 1]
    if not R:
        return (True,)
    return (False, R)

#tablero([F1,...,F10]) :- fila(F1), ..., fila(F10), piezas(Tablero).
def tablero(valor):
    match valor:
        case list() if len(valor) == TAM:
            R = [(i + 1, fila(f)) for i, f in enumerate(valor)]
            R = [f"Fila {i}: {m}" for i, r in R if not r[0] for m in r[1]]
            if R:
                return (False, R)
            return piezas(valor)
        case list():
            return (False, [f"El tablero debe tener {TAM} filas y tiene {len(valor)}"])
        case _:
            return (False, ["El tablero debe ser una matriz (lista de listas)"])
