def uhex(cadena_hex):
    if len(cadena_hex) != 1:
        return (False,"Longitud incorrecta")
    if cadena_hex.isdigit():
        return (True,)
    if cadena_hex in ["A","B","C","D","E","F"]:
        return (True,)
    return (False,"No es valido")

def numhex(valor):
    match valor:
        case str():
            return numhex(list(valor))
        case ["#",A,B,C,D]:
            R = [uhex(A),uhex(B),uhex(C),uhex(D)]
            R = [e for e in R if not e[0]]
            if not R:
                return (True,)
            return (False,R)
        case _:
            return (False,f"Error desconocido en numhex: {valor}")

def regs(valor):
    if valor in ["R0","R1","R2","R3"]:
        return (True,)
    return (False,f"{valor} no es un registro valido")

def opmat(valor):
    if valor in ["+","-"]:
        return (True,)
    return (False,f"{valor} no es un operador valido")

def movs(valor):
    if valor in ["arriba","abajo","izq","der"]:
        return (True,)
    return (False,f"{valor} no es un movimiento valido")

#opera(A,B,C) - regs(A),opmat(B),regs(C).
#opera(A,B,C) - regs(A),opmat(B),numhex(C).
#opera(A,B,C) - numhex(A),opmat(B),regs(C).
#opera(A,B,C) :- numhex(A),opmat(B),numhex(C)

def opera(lista):
    match lista:
        case [A,B,C]:
            Oper = opmat(B)
            if len(Oper) != 1:
                print(f"lista usa {Oper} y no es válido",Oper)
                return (False,[lista])
            R = [regs(A),regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,)
            ##opera(A,B,C) :- regs(A),opmat(B),numhex(C)
            R = [regs(A),numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,)
            ##opera(A,B,C) :- numhex(A),opmat(B),regs(C).
            R = [numhex(A), regs(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,)
            ###opera(A,B,C) = numhex(A), opmat(B), numhex(C)
            R = [numhex(A), numhex(C)]
            N = [len(e) for e in R]
            match N:
                case [1,1]:
                    return (True,)
            return (False,[f"{lista} no es una operacion valida"])

def asign(valor):
    match valor:
        case str():
            return asign([e for e in valor.split('.') if e])
        case ["R","A",0,B]:
            RG = regs(R)



def operando(valor):
    """Valida que un operando sea un registro o un hexadecimal."""
    if regs(valor)[0] or numhex(valor)[0]:
        return (True,)
    return (False, f"{valor} no es un operando valido")


def asign_completa(tokens, linea):
    """Complementa la función asign con todas las formas observadas."""
    match tokens:
        case [destino, "=", "sensor", direccion]:
            if regs(destino)[0] and movs(direccion)[0]:
                return (True, ("sensor", destino, direccion, linea))
        case [destino, "=", fuente]:
            if regs(destino)[0] and operando(fuente)[0]:
                return (True, ("asignar", destino, fuente, linea))
        case [destino, "=", A, operador, B]:
            if regs(destino)[0] and opera([A, operador, B])[0]:
                return (True, ("operar", destino, A, operador, B, linea))
    return (False, f"Linea {linea}: asignacion invalida")


def limpiar_linea(texto):
    texto = texto.strip()
    while texto.startswith("→"):
        texto = texto[1:].lstrip()
    return texto


def analizar_programa(codigo):
    """Realiza el analisis lexico, sintactico y semantico."""
    if isinstance(codigo, str):
        codigo = codigo.splitlines()
    lineas = [(limpiar_linea(t), n) for n, t in enumerate(codigo, 1)]
    lineas = [(t, n) for t, n in lineas if t]

    def bloque(posicion, cierre=None):
        instrucciones = []
        while posicion < len(lineas):
            texto, numero = lineas[posicion]
            tokens = texto.split()

            if texto in ["FinSi", "finciclo"]:
                if texto == cierre:
                    return (True, instrucciones, posicion + 1)
                return (False, f"Linea {numero}: cierre inesperado {texto}", posicion)

            match tokens:
                case ["Si", registro]:
                    if not regs(registro)[0]:
                        return (False, f"Linea {numero}: registro invalido", posicion)
                    resultado = bloque(posicion + 1, "FinSi")
                    if not resultado[0]:
                        return resultado
                    instrucciones.append(("si", registro, resultado[1], numero))
                    posicion = resultado[2]
                    continue
                case ["ciclo", registro]:
                    if not regs(registro)[0]:
                        return (False, f"Linea {numero}: registro invalido", posicion)
                    resultado = bloque(posicion + 1, "finciclo")
                    if not resultado[0]:
                        return resultado
                    instrucciones.append(("ciclo", registro, resultado[1], numero))
                    posicion = resultado[2]
                    continue
                case [direccion] if movs(direccion)[0]:
                    instrucciones.append(("mover", direccion, numero))
                case _ if "=" in tokens:
                    resultado = asign_completa(tokens, numero)
                    if not resultado[0]:
                        return (False, resultado[1], posicion)
                    instrucciones.append(resultado[1])
                case _:
                    return (False, f"Linea {numero}: instruccion desconocida", posicion)
            posicion += 1

        if cierre:
            return (False, f"Falta el cierre {cierre}", posicion)
        return (True, instrucciones, posicion)

    resultado = bloque(0)
    return (resultado[0], resultado[1])


def analizar_archivo(nombre):
    try:
        with open(nombre, "r", encoding="utf-8") as archivo:
            return analizar_programa(archivo.readlines())
    except OSError as error:
        return (False, f"No se pudo leer {nombre}: {error}")
