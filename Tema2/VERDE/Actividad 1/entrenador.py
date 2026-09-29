"""
entrenador.py
-------------
Segundo script del Sistema Experto.

Responsabilidad de este archivo:
    1) Leer la lista de animales y características desde
       "datos_iniciales.yaml" (generado por inicializador.py).
    2) Preguntar, para CADA animal, si cumple con CADA característica
       de la tabla (matriz animal x característica), usando el
       formato genérico: f"{animal} cumple con: {caracteristica}?"
    3) Convertir las respuestas de cada animal (Sí/No) en un número
       binario -> decimal, que será su "peso". La característica
       capturada primero en inicializador.py es el bit MÁS
       significativo; la última es el bit MENOS significativo.
    4) Si 3 o más animales terminan con el mismo peso, pedir al
       supervisor una característica nueva (que cumpla solo UNO de
       los animales empatados), preguntarla a TODOS los animales,
       agregarla como bit menos significativo, y recalcular los
       pesos de TODOS. Esto se repite hasta que ningún grupo de
       animales con el mismo peso tenga 3 o más integrantes.
    5) Guardar el resultado final (características, respuestas y
       pesos) en "datos_entrenados.yaml". Este archivo es
       independiente de "datos_iniciales.yaml" para no modificarlo;
       adivinador.py solo necesitará leer "datos_entrenados.yaml".

Cada vez que se ejecuta este script, la matriz y los pesos se
reconstruyen desde cero a partir de "datos_iniciales.yaml" (no se
reutiliza un entrenamiento anterior).

Formato de "datos_entrenados.yaml" generado:

    caracteristicas:            # orden de más -> menos significativo
      - Veloz
      - Pico
      - ...                     # incluye las agregadas por desempate, al final
    animales:
      - nombre: Caballo
        respuestas: [true, false, ...]   # una por característica, mismo orden
        peso: 6
      - nombre: Gallina
        respuestas: [false, true, ...]
        peso: 2
"""

import os
import sys
import yaml

# ----------------------------------------------------------------------
# Constantes de configuración
# ----------------------------------------------------------------------
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS_INICIALES = os.path.join(CARPETA_SCRIPT, "datos_iniciales.yaml")
RUTA_DATOS_ENTRENADOS = os.path.join(CARPETA_SCRIPT, "datos_entrenados.yaml")

TAMANO_MAXIMO_EMPATE = 2   # Como máximo se toleran 2 animales con el mismo peso


# ----------------------------------------------------------------------
# Carga / guardado de YAML
# ----------------------------------------------------------------------
def cargar_datos_iniciales(ruta):
    """
    Lee "datos_iniciales.yaml" generado por inicializador.py.
    Devuelve una lista de dicts {"nombre": ..., "caracteristica": ...}.
    Si el archivo no existe o está vacío, termina el programa con un
    mensaje claro (no tiene sentido entrenar sin datos).
    """
    if not os.path.exists(ruta):
        print(f'No se encontró el archivo "{ruta}".')
        print("Ejecuta primero inicializador.py para generar la base de conocimiento.")
        sys.exit(1)

    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = yaml.safe_load(archivo)

    if not contenido or not contenido.get("animales"):
        print(f'El archivo "{ruta}" está vacío o mal formado.')
        sys.exit(1)

    return contenido["animales"]


def guardar_datos_entrenados(ruta, caracteristicas, animales_entrenados):
    """
    Guarda el resultado final del entrenamiento: la lista de
    características (en orden de significancia) y, por cada animal,
    sus respuestas booleanas y su peso decimal.
    """
    contenido = {
        "caracteristicas": caracteristicas,
        "animales": animales_entrenados,
    }
    with open(ruta, "w", encoding="utf-8") as archivo:
        yaml.safe_dump(
            contenido,
            archivo,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )


# ----------------------------------------------------------------------
# Entrada de datos / validaciones
# ----------------------------------------------------------------------
def pedir_respuesta_si_no(pregunta):
    """
    Pide una respuesta estrictamente "S" o "N" (sin distinguir
    mayúsculas/minúsculas). Reintenta hasta obtener una respuesta
    válida. Devuelve True para "S" y False para "N".
    """
    while True:
        respuesta = input(pregunta).strip().upper()
        if respuesta == "S":
            return True
        if respuesta == "N":
            return False
        print('  -> Respuesta inválida. Debes escribir "S" o "N".')


def pedir_caracteristica_nueva(caracteristicas_usadas):
    """
    Pide al supervisor una característica nueva para resolver un
    empate. Debe cumplir las mismas reglas que las características
    iniciales: 1 o 2 palabras, y ser única en toda la tabla (no
    repetir ninguna característica ya usada, inicial o de desempate).
    """
    while True:
        caracteristica = input("Nueva característica de desempate: ").strip()

        if not caracteristica:
            print("  -> La característica no puede estar vacía.")
            continue

        cantidad_palabras = len(caracteristica.split())
        if cantidad_palabras not in (1, 2):
            print("  -> La característica debe tener 1 o 2 palabras.")
            continue

        if caracteristica.casefold() in caracteristicas_usadas:
            print(f'  -> La característica "{caracteristica}" ya está en uso. Debe ser única.')
            continue

        return caracteristica


# ----------------------------------------------------------------------
# Lógica de entrenamiento
# ----------------------------------------------------------------------
def calcular_peso(respuestas):
    """
    Convierte una lista de booleanos (respuestas) en un entero
    decimal, tratando el primer elemento como el bit más
    significativo y el último como el bit menos significativo.
    Ejemplo: [True, False, True] -> "101" -> 5
    """
    peso = 0
    for respuesta in respuestas:
        peso = (peso << 1) | (1 if respuesta else 0)
    return peso


def recalcular_pesos(animales_entrenados):
    """
    Recalcula el peso de TODOS los animales a partir de su lista
    actual de respuestas. Se llama después de agregar cualquier
    característica nueva (aunque un animal responda "No" a la nueva
    característica, su peso cambia de posición al crecer la cantidad
    de bits, por eso se recalculan todos).
    """
    for animal in animales_entrenados:
        animal["peso"] = calcular_peso(animal["respuestas"])


def construir_matriz_inicial(animales_iniciales, caracteristicas):
    """
    Pregunta, para cada animal, si cumple con cada característica de
    la lista (matriz completa animal x característica). Devuelve la
    lista de animales entrenados: [{"nombre":..., "respuestas":[...]}]
    (los pesos se calculan aparte, con recalcular_pesos).
    """
    animales_entrenados = []
    nombres = [a["nombre"] for a in animales_iniciales]
    total_preguntas = len(nombres) * len(caracteristicas)
    numero_pregunta = 0

    print(f"\nSe realizarán {total_preguntas} preguntas para construir la matriz inicial.\n")

    for nombre in nombres:
        respuestas = []
        for caracteristica in caracteristicas:
            numero_pregunta += 1
            pregunta = f"[{numero_pregunta}/{total_preguntas}] {nombre} cumple con: {caracteristica}? (S/N): "
            respuestas.append(pedir_respuesta_si_no(pregunta))
        animales_entrenados.append({"nombre": nombre, "respuestas": respuestas})

    return animales_entrenados


def encontrar_grupo_empatado(animales_entrenados):
    """
    Busca si existe algún grupo de animales con el mismo peso y
    tamaño mayor al máximo tolerado (2). Si lo encuentra, devuelve
    la lista de nombres de ese grupo; si no hay ningún empate de ese
    tamaño, devuelve None.
    """
    pesos_a_nombres = {}
    for animal in animales_entrenados:
        pesos_a_nombres.setdefault(animal["peso"], []).append(animal["nombre"])

    for peso, nombres in pesos_a_nombres.items():
        if len(nombres) > TAMANO_MAXIMO_EMPATE:
            return peso, nombres

    return None, None


def resolver_empates(animales_entrenados, caracteristicas):
    """
    Mientras exista algún grupo de 3+ animales con el mismo peso,
    pide al supervisor una característica nueva (que cumpla solo uno
    de los animales del grupo empatado), la pregunta a TODOS los
    animales, la agrega como bit menos significativo, y recalcula
    los pesos de todos. Se repite hasta que no queden grupos de 3+
    animales empatados.
    """
    caracteristicas_usadas = {c.casefold() for c in caracteristicas}

    while True:
        peso_empatado, nombres_empatados = encontrar_grupo_empatado(animales_entrenados)
        if nombres_empatados is None:
            break  # Ya no hay grupos con 3 o más animales del mismo peso

        print(f"\nLos siguientes animales quedaron con el mismo peso ({peso_empatado}):")
        print(f"  {', '.join(nombres_empatados)}")
        print("Agrega una característica nueva que sea cumplida por SOLO UNO de estos animales.")

        caracteristica_nueva = pedir_caracteristica_nueva(caracteristicas_usadas)
        caracteristicas_usadas.add(caracteristica_nueva.casefold())
        caracteristicas.append(caracteristica_nueva)

        # Se pregunta a TODOS los animales, no solo a los empatados,
        # para mantener la matriz completa y consistente.
        for animal in animales_entrenados:
            pregunta = f'{animal["nombre"]} cumple con: {caracteristica_nueva}? (S/N): '
            respuesta = pedir_respuesta_si_no(pregunta)
            animal["respuestas"].append(respuesta)

        recalcular_pesos(animales_entrenados)


# ----------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------
def main():
    print("=== Entrenador del Sistema Experto ===")

    # 1) Cargar animales y características iniciales
    animales_iniciales = cargar_datos_iniciales(RUTA_DATOS_INICIALES)
    caracteristicas = [a["caracteristica"] for a in animales_iniciales]

    # 2) Construir la matriz completa animal x característica
    animales_entrenados = construir_matriz_inicial(animales_iniciales, caracteristicas)

    # 3) Calcular el peso inicial de cada animal
    recalcular_pesos(animales_entrenados)

    # 4) Resolver empates de 3 o más animales agregando características nuevas
    resolver_empates(animales_entrenados, caracteristicas)

    # 5) Guardar el resultado final
    guardar_datos_entrenados(RUTA_DATOS_ENTRENADOS, caracteristicas, animales_entrenados)

    print(f"\nEntrenamiento completado. Se usaron {len(caracteristicas)} característica(s) en total.")
    print("Pesos finales:")
    for animal in sorted(animales_entrenados, key=lambda a: a["peso"], reverse=True):
        print(f'  {animal["nombre"]}: {animal["peso"]}')
    print(f'\nResultado guardado en "{RUTA_DATOS_ENTRENADOS}".')


if __name__ == "__main__":
    main()
