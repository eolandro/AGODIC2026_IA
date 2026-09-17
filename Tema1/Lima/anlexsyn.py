# ─────────────────────────────────────────────────────────────────────────────
# anlexsyn.py  —  Analizador léxico-semántico de Boome
# Traducción directa de la gramática Prolog vista en clase
# Enfoque: Programación Lógica / Funcional
# ─────────────────────────────────────────────────────────────────────────────

# uhex(C) :- is_digit(C).
# uhex("A"). uhex("B"). ... uhex("F").
def uhex(cadena_hex):
    if len(cadena_hex) != 1:
        return (False, "Longitud incorrecta")
    if cadena_hex.isdigit():
        return (True,)
    if cadena_hex in ["A","B","C","D","E","F"]:
        return (True,)
    return (False, f"{cadena_hex} no es un dígito hexadecimal válido")

# numhex(Str) :- string_to_liststring(Str,[S,A,B,C,D]), numhex(S,A,B,C,D).
# numhex("#",A,B,C,D) :- uhex(A),uhex(B),uhex(C),uhex(D).
def numhex(valor):
    match valor:
        case str():
            return numhex(list(valor))
        case ["#", A, B, C, D]:
            invalidos = [e for e in [uhex(A),uhex(B),uhex(C),uhex(D)] if not e[0]]
            if not invalidos:
                return (True,)
            return (False, invalidos)
        case _:
            return (False, f"Error en numhex: {valor}")

# regs("R0"). regs("R1"). regs("R2"). regs("R3").
def regs(valor):
    if valor in ["R0","R1","R2","R3"]:
        return (True,)
    return (False, f"{valor} no es un registro válido")

# opmat("+"). opmat("-").
def opmat(valor):
    if valor in ["+","-"]:
        return (True,)
    return (False, f"{valor} no es un operador válido")

# movs("arriba"). movs("abajo"). movs("izq"). movs("der").
def movs(valor):
    if valor in ["arriba","abajo","izq","der"]:
        return (True,)
    return (False, f"{valor} no es un movimiento válido")

# opera(A,B,C) :- regs(A),opmat(B),regs(C).
# opera(A,B,C) :- regs(A),opmat(B),numhex(C).
# opera(A,B,C) :- numhex(A),opmat(B),regs(C).
# opera(A,B,C) :- numhex(A),opmat(B),numhex(C).
def opera(lista):
    match lista:
        case [A, B, C]:
            if opmat(B)[0] is False:
                return (False, f"{B} no es operador válido")
            combinaciones = [
                [regs(A),   regs(C)  ],
                [regs(A),   numhex(C)],
                [numhex(A), regs(C)  ],
                [numhex(A), numhex(C)],
            ]
            for par in combinaciones:
                if all(e[0] for e in par):
                    return (True,)
            return (False, f"{lista} no es una operación válida")
        case _:
            return (False, f"Error en opera: {lista}")

# asign(R,"=",Nh)       :- regs(R),numhex(Nh).
# asign(R,"=","sensor",M) :- regs(R),movs(M).
# asign(R,"=",A,O,B)    :- regs(R),opera(A,O,B).
def asign(valor):
    match valor:
        case str():
            return asign([e for e in valor.split(" ") if e])
        case [R, "=", Nh]:
            if not regs(R)[0]:
                return (False, f"{R} no es registro válido")
            if not numhex(Nh)[0]:
                return (False, f"{Nh} no es numhex válido")
            return (True,)
        case [R, "=", "sensor", M]:
            if not regs(R)[0]:
                return (False, f"{R} no es registro válido")
            if not movs(M)[0]:
                return (False, f"{M} no es movimiento válido")
            return (True,)
        case [R, "=", A, O, B]:
            if not regs(R)[0]:
                return (False, f"{R} no es registro válido")
            return opera([A, O, B])
        case _:
            return (False, f"Error en asign: {valor}")

# linea(L) :- asign(L).
# linea(L) :- movs(L).
def linea(valor):
    if asign(valor)[0]:
        return (True,)
    if isinstance(valor, str) and movs(valor)[0]:
        return (True,)
    if isinstance(valor, list):
        if condicional(valor)[0]:
            return (True,)
        if ciclos(valor)[0]:
            return (True,)
    return (False, f"{valor} no es una línea válida")

# lineas([L])    :- linea(L).
# lineas([P|R])  :- linea(P), lineas(R).
def lineas(lista):
    match lista:
        case [L]:
            R = linea(L)
            if R[0]:
                return (True,)
            return (False, R)
        case [P, *R]:
            if not linea(P)[0]:
                return (False, f"{P} no es línea válida")
            return lineas(R)
        case _:
            return (False, f"Error en lineas: {lista}")

# condicional("Si",Re,[F|R],"FinSi") :- regs(Re), lineas([F|R]).
def condicional(valor):
    match valor:
        case ["Si", Re, [F, *R], "FinSi"]:
            if not regs(Re)[0]:
                return (False, f"{Re} no es registro válido")
            if not lineas([F, *R])[0]:
                return (False, f"Cuerpo del Si contiene líneas inválidas")
            return (True,)
        case _:
            return (False, f"Error en condicional: {valor}")

# ciclos("ciclo",Re,[F|R],"finciclo") :- regs(Re), lineas([F|R]).
def ciclos(valor):
    match valor:
        case ["ciclo", Re, [F, *R], "finciclo"]:
            if not regs(Re)[0]:
                return (False, f"{Re} no es registro válido")
            if not lineas([F, *R])[0]:
                return (False, f"Cuerpo del ciclo contiene líneas inválidas")
            return (True,)
        case _:
            return (False, f"Error en ciclos: {valor}")
