"""Analizador léxico, sintáctico y semántico de Boome."""

REGISTROS = {"R0", "R1", "R2", "R3"}
DIRECCIONES = {"arriba", "abajo", "izq", "der"}
OPERADORES = {"+", "-"}


def ok():
    return (True,)


def fallo(mensaje):
    return (False, mensaje)


def es_registro(texto):
    return texto in REGISTROS


def es_hex(texto):
    return (
        isinstance(texto, str)
        and len(texto) == 5
        and texto[0] == "#"
        and all(digito in "0123456789ABCDEF" for digito in texto[1:])
    )


def es_valor(texto):
    return es_registro(texto) or es_hex(texto)


def opera(izquierda, operador, derecha):
    if operador not in OPERADORES:
        return fallo(f"Operador no válido: {operador}")
    if not es_valor(izquierda):
        return fallo(f"Operando izquierdo no válido: {izquierda}")
    if not es_valor(derecha):
        return fallo(f"Operando derecho no válido: {derecha}")
    return ok()


def asignacion(partes):
    if len(partes) < 3 or partes[1] != "=":
        return fallo("La instrucción no tiene formato de asignación")

    destino = partes[0]
    if not es_registro(destino):
        return fallo(f"Registro destino no válido: {destino}")

    if len(partes) == 3:
        if es_valor(partes[2]):
            return ok()
        return fallo(f"Valor no válido: {partes[2]}")

    if len(partes) == 4 and partes[2] == "sensor":
        if partes[3] in DIRECCIONES:
            return ok()
        return fallo(f"Dirección del sensor no válida: {partes[3]}")

    if len(partes) == 5:
        return opera(partes[2], partes[3], partes[4])

    return fallo("Cantidad incorrecta de elementos en la asignación")


def linea(texto):
    if not isinstance(texto, str):
        return fallo("La instrucción debe ser una cadena")

    partes = texto.split()
    if len(partes) == 1 and partes[0] in DIRECCIONES:
        return ok()

    if len(partes) == 2 and partes[0] in {"Si", "ciclo"}:
        if es_registro(partes[1]):
            return ok()
        return fallo(f"Registro de control no válido: {partes[1]}")

    if len(partes) == 1 and partes[0] in {"FinSi", "finciclo"}:
        return ok()

    return asignacion(partes)


def bloque(elemento):
    if not isinstance(elemento, list) or len(elemento) != 4:
        return fallo(f"Bloque mal formado: {elemento}")

    inicio, registro, cuerpo, final = elemento
    cierre_correcto = "FinSi" if inicio == "Si" else "finciclo"

    if inicio not in {"Si", "ciclo"}:
        return fallo(f"Inicio de bloque no válido: {inicio}")
    if final != cierre_correcto:
        return fallo(f"Se esperaba {cierre_correcto}, se encontró {final}")
    if not es_registro(registro):
        return fallo(f"Registro de bloque no válido: {registro}")

    return lineas(cuerpo)


def lineas(programa):
    if not isinstance(programa, list):
        return fallo("El programa debe ser una lista")

    for numero, elemento in enumerate(programa, start=1):
        validacion = bloque(elemento) if isinstance(elemento, list) else linea(elemento)
        if not validacion[0]:
            return fallo(f"Error en el elemento {numero}: {validacion[1]}")

    return ok()
