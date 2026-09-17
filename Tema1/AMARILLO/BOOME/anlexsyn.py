def uhex(cadena_hex):
    if len(cadena_hex) != 1:
        return (False, "Longitud incorrecta")
    if cadena_hex.isdigit():
        return (True,)
    if cadena_hex in ["A", "B", "C", "D", "E", "F"]:
        return (True,)
    return (False, "No es valido")

def numhex(valor):
    match valor:
        case str():
            return numhex(list(valor))
        case ["#", A, B, C, D]:
            R = [uhex(A), uhex(B), uhex(C), uhex(D)]
            R = [e for e in R if not e[0]]
            if not R:
                return (True,)
            return (False, R)
        case _:
            return (False, f"Error desconocido en numhex: {valor}")

def regs(valor):
    if valor in ["R0", "R1", "R2", "R3"]:
        return (True,)
    return (False, f"{valor} no es un registro valido")

def opmat(valor):
    if valor in ["+", "-"]:
        return (True,)
    return (False, f"{valor} no es un operador valido")

def movs(valor):
    if valor in ["arriba", "abajo", "izq", "der"]:
        return (True,)
    return (False, f"{valor} no es un movimiento valido")
# opera(A,B,C) :- regs(A), opmat(B), regs(C).
# opera(A,B,C) :- regs(A), opmat(B), numhex(C).
# opera(A,B,C) :- numhex(A), opmat(B), regs(C).
# opera(A,B,C) :- numhex(A), opmat(B), numhex(C).

def opera(lista):
    match lista:
        case [A, B, C]:
            Oper = opmat(B)
            if len(Oper) != 1:
                return (
                    False,
                    [f"{lista} usa {Oper} y no es valido", Oper]
                )
            # opera(A,B,C) :- regs(A), opmat(B), regs(C).
            R = [regs(A), regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)
            # opera(A,B,C) :- regs(A), opmat(B), numhex(C).
            R = [regs(A), numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)
            # opera(A,B,C) :- numhex(A), opmat(B), regs(C).
            R = [numhex(A), regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)
            # opera(A,B,C) :- numhex(A), opmat(B), numhex(C).
            R = [numhex(A), numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)
            return (
                False,
                [f"{lista} no es una operacion valida"]
            )
        case _:
            return (
                False,
                [f"{lista} no es una operacion valida"]
            )

def asign(valor):
    match valor:
        case str():
            return asign([
                e for e in valor.split(" ") if e
            ])
        ##########
        case [Registro, "=", Nh]:
            RG = regs(Registro)
            if len(RG) != 1:
                return (False, [f"{valor} tiene un registro no valido", RG])
            NH = numhex(Nh)
            if len(NH) != 1:
                return (False, [f"{valor} tiene un numero hexadecimal no valido", NH])
            return (True,)

        case [Registro, "=", "sensor", M]:
            RG = regs(Registro)
            if len(RG) != 1:
                return (False, [f"{valor} tiene un registro no valido", RG])
            MV = movs(M)
            if len(MV) != 1:
                return (False, [f"{valor} tiene un movimiento no valido", MV])
            return (True,)
        ##########
        case [R, "=", A, O, B]:
            RG = regs(R)
            if len(RG) != 1:
                return (
                    False,
                    [
                        f"{valor} tiene un registro no valido",
                        RG
                    ]
                )
            Res = opera([A, O, B])
            if len(Res) == 1:
                return (True,)
            return (False, Res)
        case _:
            return (
                False,
                f"Error desconocido en asign: {valor}"
            )
        
def linea(valor):
    if asign(valor)[0]:
        return (True,)
    if isinstance(valor, str) and movs(valor)[0]:
        return (True,)
    if isinstance(valor, list) and condicional(valor)[0]:
        return (True,)
    if isinstance(valor, list) and ciclos(valor)[0]:
        return (True,)
    return (False, f"{valor} no es una linea valida")

def condicional(valor):
    match valor:
        case ["Si", R, cuerpo, "FinSi"]:
            RG = regs(R)
            if len(RG) != 1:
                return (False, f"{R} no es un registro valido")
            for instruccion in cuerpo:
                if not linea(instruccion)[0]:
                    return (False, f"{instruccion} no es una linea valida")
            return (True,)
        case _:
            return (False, f"{valor} no es un condicional valido")
        
def ciclos(valor):
    match valor:
        case ["ciclos", R, cuerpo, "Finciclo"]:
            RG = regs(R)

            if len(RG) != 1:
                return (False, f"{R} no es un registro valido")

            for instruccion in cuerpo:
                if not linea(instruccion)[0]:
                    return (False, f"{instruccion} no es una linea valida")

            return (True,)

        case _:
            return (False, f"{valor} no es un ciclo valido")