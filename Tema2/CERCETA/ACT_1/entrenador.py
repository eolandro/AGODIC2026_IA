import json
from math import log2

ARCHIVO_ANIMALES = "animales.json"
ARCHIVO_PESOS = "pesos.json"


def cargar_animales(archivo=ARCHIVO_ANIMALES):
    """Carga la tabla de animales generada por inicializador.py."""
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_pesos(archivo=ARCHIVO_PESOS):
    """Carga la tabla de pesos generada por entrenador.py, si existe."""
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def obtener_preguntas(animales):
    """Devuelve las características (preguntas) disponibles en la tabla."""
    if not animales:
        return []
    return [clave for clave in animales[0] if clave != "animal"]


def filtrar(animales, caracteristica, respuesta):
    """Conserva los animales cuya respuesta coincide con la dada."""
    return [
        animal for animal in animales
        if animal[caracteristica].upper() == respuesta.upper()
    ]


def entropia(si, no):
    """Entropía (bits de información) de una pregunta.

    Es máxima (1.0) cuando la pregunta divide al grupo exactamente a la
    mitad (la más útil para discriminar), y 0.0 cuando todos los animales
    responden igual (no aporta ninguna información).
    """
    total = si + no
    if total == 0 or si == 0 or no == 0:
        return 0.0

    p_si = si / total
    p_no = no / total
    return -(p_si * log2(p_si) + p_no * log2(p_no))


def calcular_entropias(animales, preguntas):
    """Entropía global de cada característica sobre TODOS los animales."""
    entropias = {}
    for pregunta in preguntas:
        si = sum(1 for a in animales if a[pregunta].upper() == "S")
        no = len(animales) - si
        entropias[pregunta] = entropia(si, no)
    return entropias


def ordenar_preguntas(animales, preguntas):
    """Ordena las preguntas de la más a la menos informativa.

    En empate de entropía se usa el nombre para un orden estable.
    """
    entropias = calcular_entropias(animales, preguntas)
    return sorted(preguntas, key=lambda p: (-entropias[p], p))


def calcular_pesos(preguntas_ordenadas):
    """Asigna a cada característica un peso binario (potencia de 2).

    La característica más informativa recibe el bit más significativo,
    igual que en la tabla del pizarrón (leal=bit alto ... lentitud=bit bajo).
    """
    n = len(preguntas_ordenadas)
    return {
        pregunta: 2 ** (n - 1 - indice)
        for indice, pregunta in enumerate(preguntas_ordenadas)
    }


def calcular_valores(animales, preguntas_ordenadas, pesos):
    """Representación binaria y valor decimal de cada animal (tabla de pesos)."""
    resultados = []

    for animal in animales:
        binario = "".join(
            "1" if animal[pregunta].upper() == "S" else "0"
            for pregunta in preguntas_ordenadas
        )
        valor = sum(
            pesos[pregunta]
            for pregunta in preguntas_ordenadas
            if animal[pregunta].upper() == "S"
        )
        resultados.append({
            "animal": animal["animal"],
            "binario": binario,
            "valor": valor,
        })

    resultados.sort(key=lambda r: r["valor"], reverse=True)
    return resultados


def mejor_pregunta(animales, preguntas_disponibles, orden=None):
    """Elige, entre las preguntas aún no realizadas, la que mejor divide
    (de forma más equilibrada) a los animales que quedan como candidatos.

    Esto minimiza el número de preguntas necesarias para adivinar (se
    recalcula en cada paso porque el mejor corte depende de quién queda).

    Si hay empate entre varias preguntas igual de buenas para el grupo
    actual, se usa `orden` (el ranking global calculado por entrenador.py)
    para preferir la que en general es más informativa.
    """
    if not animales or not preguntas_disponibles:
        return None

    candidatas = []
    for pregunta in preguntas_disponibles:
        si = sum(1 for a in animales if a[pregunta].upper() == "S")
        no = len(animales) - si
        e = entropia(si, no)
        if e > 0:
            candidatas.append((e, pregunta))

    if not candidatas:
        return None

    mejor_entropia = max(e for e, _ in candidatas)
    empatadas = [p for e, p in candidatas if e == mejor_entropia]

    if len(empatadas) == 1 or not orden:
        return empatadas[0]

    empatadas.sort(key=lambda p: orden.index(p) if p in orden else len(orden))
    return empatadas[0]


def entrenar():
    """Genera pesos.json a partir de animales.json (etapa 2 del sistema)."""
    animales = cargar_animales()

    if not animales:
        print("No hay animales registrados. Ejecuta inicializador.py primero.")
        return

    preguntas = obtener_preguntas(animales)
    orden = ordenar_preguntas(animales, preguntas)
    pesos = calcular_pesos(orden)
    valores = calcular_valores(animales, orden, pesos)

    datos = {
        "orden_preguntas": orden,
        "pesos": pesos,
        "animales": valores,
    }

    with open(ARCHIVO_PESOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    print("\n=== ENTRENADOR ===")
    print(f"Se entrenó con {len(animales)} animales y {len(preguntas)} características.\n")

    print("Orden de las preguntas (de más a menos informativa):")
    for pregunta in orden:
        print(f"  {pregunta:<12} peso={pesos[pregunta]}")

    ancho = max(len("Animal"), max(len(v["animal"]) for v in valores))
    print("\nTabla de pesos por animal:")
    print(f"  {'Animal'.ljust(ancho)}  {'Binario'.ljust(len(orden))}  Valor")
    for v in valores:
        print(f"  {v['animal'].ljust(ancho)}  {v['binario']}  {v['valor']}")

    print(f"\nGuardado en: {ARCHIVO_PESOS}")


if __name__ == "__main__":
    entrenar()
