
def uhex(cadena_hex):
    """Valida UN solo dígito hexadecimal ('0'-'9' o 'A'-'F')."""
    if len(cadena_hex) != 1:
        return (False, "Longitud incorrecta")
    if cadena_hex.isdigit():
        return (True, )
    if cadena_hex in ["A", "B", "C", "D", "E", "F"]:
        return (True, )
    return (False, "No es valido")


def numhex(valor):
    """Valida un número hexadecimal completo, con forma '#XXXX'
    (numeral seguido de 4 dígitos hex). Usa uhex() para revisar
    cada uno de los 4 dígitos por separado."""
    match valor:
        case str():
            # Si llega como texto "#0001", lo separamos en caracteres
            return numhex(list(valor))
        case ["#", A, B, C, D]:
            R = [uhex(A), uhex(B), uhex(C), uhex(D)]
            R = [e for e in R if not e[0]]      # nos quedamos solo con los que fallaron
            if not R:
                return (True,)                   # ningún dígito falló -> válido
            return (False, R)
        case _:
            return (False, f"Error desconocido en numhex: {valor}")


def regs(valor):
    """Valida que 'valor' sea uno de los 4 registros permitidos."""
    if valor in ["R0", "R1", "R2", "R3"]:
        return (True,)
    return (False, f"{valor} no es un registro valido")


def opmat(valor):
    """Valida que 'valor' sea un operador aritmético permitido (+ o -)."""
    if valor in ["+", "-"]:
        return (True,)
    return (False, f"{valor} no es un operador valido")


def movs(valor):
    """Valida que 'valor' sea uno de los 4 movimientos permitidos."""
    if valor in ["arriba", "abajo", "izq", "der"]:
        return (True,)
    return (False, f"{valor} no es un movimiento valido")


def opera(lista):
    """Valida una operación 'A OP B', donde A y B pueden ser CADA UNO
    un registro o un número hexadecimal"""
    match lista:
        case [A, B, C]:
            Oper = opmat(B)
            if len(Oper) != 1:
                return (False, [f"{lista} usa {Oper} y no es valido", Oper])

            # Intento 1: A y C son registros
            R = [regs(A), regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)
            # Intento 2: A es registro, C es hexadecimal
            R = [regs(A), numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)
            # Intento 3: A es hexadecimal, C es registro
            R = [numhex(A), regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)
            # Intento 4: A y C son hexadecimales
            R = [numhex(A), numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1, 1]:
                    return (True,)
            return (False, [f"{lista} no es una operacion valida"])
        case _:
            return (False, [f"{lista} no tiene la forma A OP B"])
def asign(valor):
    """Valida una instrucción de asignación complet"""
    if isinstance(valor, str):
        elementos = [e for e in valor.split(" ") if e]
        return asign(elementos)

    match valor:
        case [R, "=", Nh] if isinstance(Nh, str) and Nh.startswith("#"):
            resultado_registro = regs(R)
            if not resultado_registro[0]:
                return (False, f"{R} no es un registro válido")

            resultado_numero = numhex(Nh)
            if not resultado_numero[0]:
                return (False, f"{Nh} no es un hexadecimal válido")

            return (True,)

        case [R, "=", "sensor", M]:
            resultado_registro = regs(R)
            if not resultado_registro[0]:
                return (False, f"{R} no es un registro válido")

            resultado_movimiento = movs(M)
            if not resultado_movimiento[0]:
                return (False, f"{M} no es un movimiento válido")

            return (True,)

        case [R, "=", A, operador, B]:
            resultado_registro = regs(R)
            if not resultado_registro[0]:
                return (False, f"{R} no es un registro válido")

            resultado_operacion = opera([A, operador, B])
            if resultado_operacion[0]:
                return (True,)

            return resultado_operacion

        case _:
            return (False, f"Error desconocido en asign: {valor}")


def condicional(valor):
    """Valida un bloque 'Si'. Regla de Prolog que representa:
    condicional("Si",Re,[F|R],"FinSi") :- regs(Re), lineas([F | R])."""
    match valor:
        case ["Si", Re, Sub, "FinSi"]:
            resultado_registro = regs(Re)
            if not resultado_registro[0]:
                return (False, f"{Re} no es un registro válido")

            resultado_lineas = lineas(Sub)   # valida recursivamente lo de adentro del bloque
            if not resultado_lineas[0]:
                return (False, resultado_lineas)

            return (True,)
        case _:
            return (False, f"{valor} no tiene la forma de un Si")


def ciclos(valor):
    """Valida un bloque 'ciclo'. Regla de Prolog que representa"""
    match valor:
        case ["ciclo", Re, Sub, "finciclo"]:
            resultado_registro = regs(Re)
            if not resultado_registro[0]:
                return (False, f"{Re} no es un registro válido")

            resultado_lineas = lineas(Sub)
            if not resultado_lineas[0]:
                return (False, resultado_lineas)

            return (True,)
        case _:
            return (False, f"{valor} no tiene la forma de un ciclo")


def linea(valor):
    """Valida UNA sola línea/elemento, que puede ser:
    - una lista -> es un bloque anidado ["Si", ...] o ["ciclo", ...],
      se valida con condicional() o ciclos().
    - un string -> es una instrucción simple (movimiento o asignación),
      se valida con movs() o asign()."""
    if isinstance(valor, list):
        resultado_condicional = condicional(valor)
        if resultado_condicional[0]:
            return (True,)

        resultado_ciclo = ciclos(valor)
        if resultado_ciclo[0]:
            return (True,)

        return (
            False,
            [f"{valor} no es un bloque válido", resultado_condicional, resultado_ciclo]
        )

    resultado_movimiento = movs(valor)
    if resultado_movimiento[0]:
        return (True,)

    resultado_asignacion = asign(valor)
    if resultado_asignacion[0]:
        return (True,)

    return (
        False,
        f"{valor} no es una instrucción válida"
    )
def lineas(lista):
    """Valida una lista completa de líneas, una por una, de forma
    recursiva Se detiene en cuanto encuentra la primera línea inválida."""
    match lista:
        case []:
            return (True,)
        case [L, *R]:
            resultado = linea(L)
            if not resultado[0]:
                return (False, [f"{L} no es válida", resultado])
            return lineas(R)
        case _:
            return (False, f"Error desconocido en lineas: {lista}")