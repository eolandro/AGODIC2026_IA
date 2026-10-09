import json
import math
from pathlib import Path

ARCHIVO_DATOS = Path("datos_animales.json")
ARCHIVO_MODELO = Path("modelo_entrenado.json")


def entropia(animales):
    """
    Calcula la entropía considerando cada animal como una clase.
    """

    total = len(animales)

    if total == 0:
        return 0.0

    probabilidad = 1 / total

    return -total * probabilidad * math.log2(probabilidad)


def entropia_binaria(animales, atributo):
    """
    Calcula la entropía de una pregunta binaria.
    """

    if not animales:
        return 0.0

    positivos = [
        animal for animal in animales
        if animal["atributos"].get(atributo, False)
    ]

    negativos = [
        animal for animal in animales
        if not animal["atributos"].get(atributo, False)
    ]

    total = len(animales)
    resultado = 0.0

    for grupo in [positivos, negativos]:
        if len(grupo) == 0:
            continue

        proporcion = len(grupo) / total
        resultado += proporcion * entropia(grupo)

    return resultado


def ganancia_informacion(animales, atributo):
    """
    Ganancia = entropía actual - entropía resultante.
    """

    return entropia(animales) - entropia_binaria(animales, atributo)


def calcular_preguntas(animales, caracteristicas):
    resultados = []

    for caracteristica in caracteristicas:
        clave = caracteristica["clave"]

        ganancia = ganancia_informacion(animales, clave)

        positivos = sum(
            1 for animal in animales
            if animal["atributos"].get(clave, False)
        )

        negativos = len(animales) - positivos

        resultados.append({
            "clave": clave,
            "descripcion": caracteristica["descripcion"],
            "peso": caracteristica["peso"],
            "ganancia": round(ganancia, 6),
            "positivos": positivos,
            "negativos": negativos
        })

    resultados.sort(
        key=lambda pregunta: pregunta["ganancia"],
        reverse=True
    )

    return resultados


def construir_arbol(animales, caracteristicas, usadas=None):
    """
    Construye recursivamente un árbol de decisión.
    """

    if usadas is None:
        usadas = []

    if len(animales) == 1:
        return {
            "tipo": "animal",
            "animal": animales[0]["nombre"]
        }

    if len(animales) == 0:
        return {
            "tipo": "sin_resultado"
        }

    disponibles = [
        caracteristica
        for caracteristica in caracteristicas
        if caracteristica["clave"] not in usadas
    ]

    if not disponibles:
        return {
            "tipo": "empate",
            "animales": [animal["nombre"] for animal in animales]
        }

    preguntas = calcular_preguntas(animales, disponibles)
    mejor = preguntas[0]

    clave = mejor["clave"]

    positivos = [
        animal for animal in animales
        if animal["atributos"].get(clave, False)
    ]

    negativos = [
        animal for animal in animales
        if not animal["atributos"].get(clave, False)
    ]

    nuevas_usadas = usadas + [clave]

    return {
        "tipo": "pregunta",
        "clave": clave,
        "descripcion": mejor["descripcion"],
        "ganancia": mejor["ganancia"],
        "si": construir_arbol(
            positivos,
            caracteristicas,
            nuevas_usadas
        ),
        "no": construir_arbol(
            negativos,
            caracteristicas,
            nuevas_usadas
        )
    }


def imprimir_ranking(preguntas):
    print("\nRanking de preguntas:")
    print("-" * 75)
    print(
        f"{'Pregunta':30} "
        f"{'Sí':>5} "
        f"{'No':>5} "
        f"{'Ganancia':>12}"
    )
    print("-" * 75)

    for pregunta in preguntas:
        print(
            f"{pregunta['descripcion']:30} "
            f"{pregunta['positivos']:>5} "
            f"{pregunta['negativos']:>5} "
            f"{pregunta['ganancia']:>12.6f}"
        )


def main():
    if not ARCHIVO_DATOS.exists():
        print("Error: primero ejecuta inicializador.py")
        return

    datos = json.loads(
        ARCHIVO_DATOS.read_text(encoding="utf-8")
    )

    animales = datos["animales"]
    caracteristicas = datos["caracteristicas"]

    entropia_inicial = entropia(animales)
    ranking = calcular_preguntas(animales, caracteristicas)
    arbol = construir_arbol(animales, caracteristicas)

    modelo = {
        "entropia_inicial": round(entropia_inicial, 6),
        "ranking_inicial": ranking,
        "arbol": arbol
    }

    ARCHIVO_MODELO.write_text(
        json.dumps(modelo, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Entropía inicial: {entropia_inicial:.6f}")
    imprimir_ranking(ranking)
    print(f"\nModelo guardado en: {ARCHIVO_MODELO}")


if __name__ == "__main__":
    main()