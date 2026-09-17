
def uhex(cadena_hex):
    if len(cadena_hex) !=1:
        return (False,"Longitud Incorrecta")
    if cadena_hex.isdigit():
        return (True,)
    if cadena_hex in ["A","B","C","D","E","F"]:
        return(True,)
    return (False,"No es valido")

def numhex(valor):
    match valor:
        case str():
            return numhex(list(valor))
        case ["#",A,B,C,D]:
            R= [uhex(A),uhex(B),uhex(C),uhex(D)]
            #[(True,),(True,),(True,),(True,)]
            
            R= [e for e in R if not e[0]]
            if not R:
                return(True,)
            return (False, R)
        case _:
            return (False, f"Error desconocido en numhex:{valor}")
        
def regs(valor):
    if valor in ["R0","R1","R2","R3"]:
        return(True,)
    return (False, f"{valor} no es un registro valido")

def opmat(valor):
    if valor in ["+","-"]:
        return(True,)
    return (False, f"{valor} no es un operador valido")

def movs (valor):
    if valor in ["arriba","abajo","izq","der"]:
        return(True,)
    return (False, f"{valor} no es un movimiento valido")

def opera(lista):
    match lista:
        case [A, B, C]:
            Oper = opmat(B)
            if len(Oper) != 1:
                return (False, [f"{lista} usa {Oper} y no es valido", Oper])
            
            # opera(A,B,C) :- regs(A),opmat(B),regs(C).
            R = [regs(A), regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)

            # opera(A,B,C) :- regs(A),opmat(B),numhex(C).
            R = [regs(A), numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)

            # opera(A,B,C) :- numhex(A),opmat(B),regs(C).
            R = [numhex(A), regs(C)]  # <-- Aquí se corrigió a numhex(A)
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)

            # opera(A,B,C) :- numhex(A),opmat(B),numhex(C).
            R = [numhex(A), numhex(C)]  # <-- Aquí se corrigió a numhex(A)
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)

            return (False, [f"{lista} no es una operacion valida"])

        
def asign(valor):
    match valor:
        case str():
            return asign([e for e in valor.split(' ') if e])
            
        # Asignación simple (3 elementos: R0 = #0001)
        case [R, "=", H]:
            RG = regs(R)
            if len(RG) != 1:
                return (False, [f"{valor} tiene un registro no valido", RG])
            Res = numhex(H)
            if len(Res) == 1:
                return (True,)
            return (False, Res)

        # Lectura de Sensor (4 elementos: R1 = sensor der)
        case [R, "=", "sensor", S]:
            RG = regs(R)
            if len(RG) != 1:
                return (False, [f"{valor} tiene un registro no valido", RG])
            Res = movs(S)
            if len(Res) == 1:
                return (True,)
            return (False, Res)
        case [R,"=",A,O,B]:
            RG = regs(R)
            if len (RG) !=1:
                return (False,[f"{valor} tiene un registro no  valido",RG])
            Res= opera([A,O,B])
            if len(Res)==1:
                return(True,)
            return(False,Res)
        case _:
            return (False,f"Error desconocido asign:{valor}")
def linea(L):
    # Palabras de control directas del archivo
    partes = [e for e in L.split(' ') if e]
    match partes:
        case ["ciclo", R] | ["Si", R]:
            return regs(R)
        case ["finciclo"] | ["FinSi"]:
            return (True,)

    if len(asign(L)) == 1:
        return (True,)
    if len(movs(L)) == 1:
        return (True,)
    return (False, f" La linea '{L}' no es valida")

def linea_s(lista):
    for L in lista:
        if len(linea(L)) !=1:
            return (False,f"Error en la linea {L} de la lista")
    return (True,)

def condicional (instruccion):
    match instruccion:
        case ["Si",re,bloque,"finciclo"]:
            if len (regs(re)) !=1:
                return(False, f"Registro {re} no valido")
            if len (linea_s(bloque)) !=1:
                return(False, f"Error bloque")
            return(True,)
        case _:
            return(False, "Estructura SI no valida")

def ciclos(instruccion):  
    match instruccion:
        case ["ciclo", re,bloque,"finciclo"]:
            if len (regs(re)) !=1:
                return(False, f"Registro {re} no valido")
            if len (linea_s(bloque)) !=1:
                return(False, f"Error bloque")
            return(True,) 
        case _:
            return(False, "Estructura ciclo no valida")
        

                

   
    
        
            
            