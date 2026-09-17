REGISTROS = ["R0", "R1", "R2", "R3"]
OPERADORES = ["+", "-"]
DIRECCIONES = ["arriba", "abajo", "izq", "der"]


def uhex(caracter):
    if len(caracter) != 1:
        return (False, "Longitud incorrecta")
    if caracter.isdigit():
        return (True,)
    if caracter in ["A", "B", "C", "D", "E", "F"]:
        return (True,)
    return (False, f"'{caracter}' no es un dígito hexadecimal válido")


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
            return (False, f"'{valor}' no tiene la forma #HHHH")


def regs(valor):
    if valor in REGISTROS:
        return (True,)
    return (False, f"'{valor}' no es un registro válido")


def opmat(valor):
    if valor in OPERADORES:
        return (True,)
    return (False, f"'{valor}' no es un operador válido")


def movs(valor):
    if valor in DIRECCIONES:
        return (True,)
    return (False, f"'{valor}' no es un movimiento válido")


def _valorable(valor):
    R = regs(valor)
    return R if R[0] else numhex(valor)


def opera(tokens):
    match tokens:
        case [A, Op, B]:
            OP = opmat(Op)
            if not OP[0]:
                return (False, [f"{tokens} usa un operador inválido", OP])
            VA = _valorable(A)
            VB = _valorable(B)
            if VA[0] and VB[0]:
                return (True,)
            return (False, [f"{tokens} no es una operación válida", VA, VB])
        case _:
            return (False, f"{tokens} no es una operación válida")


def asign(tokens):
    match tokens:
        case [R, "=", Nh]:
            RG = regs(R)
            if not RG[0]:
                return (False, [f"{tokens} usa un registro inválido", RG])
            NH = numhex(Nh)
            if not NH[0]:
                return (False, [f"{tokens} no es un valor hexadecimal válido", NH])
            return (True,)
        case [R, "=", "sensor", M]:
            RG = regs(R)
            if not RG[0]:
                return (False, [f"{tokens} usa un registro inválido", RG])
            MV = movs(M)
            if not MV[0]:
                return (False, [f"{tokens} usa una dirección inválida", MV])
            return (True,)
        case [R, "=", A, Op, B]:
            RG = regs(R)
            if not RG[0]:
                return (False, [f"{tokens} usa un registro inválido", RG])
            OP = opera([A, Op, B])
            if not OP[0]:
                return (False, OP)
            return (True,)
        case _:
            return (False, f"{tokens} no es una asignación válida")


def linea(tokens):
    A = asign(tokens)
    if A[0]:
        return A
    if len(tokens) == 1:
        return movs(tokens[0])
    return (False, f"{tokens} no es una línea válida")


def lineas(lista_de_tokens):
    if not lista_de_tokens:
        return (False, "el cuerpo no puede estar vacío")
    for tokens in lista_de_tokens:
        R = linea(tokens)
        if not R[0]:
            return (False, [f"{tokens} no es una línea válida dentro del bloque", R])
    return (True,)


def condicional(registro, cuerpo_tokens):
    RG = regs(registro)
    if not RG[0]:
        return (False, [f"'{registro}' no es un registro válido para 'Si'", RG])
    return lineas(cuerpo_tokens)


def ciclos(registro, cuerpo_tokens):
    RG = regs(registro)
    if not RG[0]:
        return (False, [f"'{registro}' no es un registro válido para 'ciclo'", RG])
    return lineas(cuerpo_tokens)

def _tokenizar(texto):
    return [t for t in texto.split(" ") if t]


def _buscar_cierre(lineas_texto, inicio, cierre):
    for j in range(inicio + 1, len(lineas_texto)):
        tokens = _tokenizar(lineas_texto[j])
        if tokens == [cierre]:
            return j
        if tokens[:1] in (["Si"], ["ciclo"]):
            return None
    return None


def programa(lineas_texto):
    errores = []
    i = 0
    n = len(lineas_texto)

    while i < n:
        texto = lineas_texto[i]
        tokens = _tokenizar(texto)

        if tokens[:1] == ["Si"] or tokens[:1] == ["ciclo"]:
            apertura = tokens[0]
            cierre = "FinSi" if apertura == "Si" else "finciclo"

            if len(tokens) != 2:
                errores.append((i + 1, texto, f"'{apertura}' debe ir seguido de un solo registro"))
                i += 1
                continue

            j = _buscar_cierre(lineas_texto, i, cierre)
            if j is None:
                errores.append((
                    i + 1, texto,
                    f"'{apertura}' no tiene su '{cierre}' correspondiente "
                    f"(o contiene un bloque anidado, lo cual no está permitido)"
                ))
                i += 1
                continue

            cuerpo = [_tokenizar(t) for t in lineas_texto[i + 1:j]]
            validador = condicional if apertura == "Si" else ciclos
            R = validador(tokens[1], cuerpo)
            if not R[0]:
                errores.append((i + 1, texto, R[1]))

            i = j + 1
            continue

        if tokens in (["FinSi"], ["finciclo"]):
            errores.append((i + 1, texto, f"'{texto}' no tiene una apertura correspondiente"))
            i += 1
            continue

        R = linea(tokens)
        if not R[0]:
            errores.append((i + 1, texto, R[1]))
        i += 1

    if errores:
        return (False, errores)
    return (True,)
