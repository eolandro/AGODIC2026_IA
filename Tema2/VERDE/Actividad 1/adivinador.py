
"""
adivinador.py
-------------
Tercer y último script del Sistema Experto.

Responsabilidad de este archivo:
    1) Leer "datos_entrenados.yaml" (generado por entrenador.py), que
       contiene la lista de características (en orden de
       significancia) y, por cada animal, sus respuestas booleanas y
       su peso.
    2) Mostrar al usuario la lista numerada de animales disponibles.
    3) Adivinar el animal en el que está pensando el usuario, usando
       un algoritmo dinámico tipo "divide y vencerás": en cada paso
       se elige, de las características AÚN NO preguntadas, la que
       divide de forma más pareja al grupo de animales candidatos
       restantes (minimizando la diferencia entre cuántos la cumplen
       y cuántos no). Esto minimiza la cantidad de preguntas
       necesarias para llegar a un solo candidato.
    4) Caso especial: si en algún momento quedan exactamente 2
       animales candidatos, ya no existe ninguna característica
       entrenada que los distinga (por eso terminaron con el mismo
       peso). En ese caso se pregunta directamente:
           "Tu animal es: {primer candidato de la lista}?"
       Si responde "S", el animal es ese primer candidato; si
       responde "N", el animal es el segundo candidato.
    5) Una vez identificado un único animal, se imprime el resultado:
       "¡Tu animal es: {nombre}!"

La pregunta genérica usada durante el proceso tiene el formato:
    f"Tu animal cumple con: {caracteristica}?"
"""

import os
import sys
import yaml

# ----------------------------------------------------------------------
# Constantes de configuración
# ----------------------------------------------------------------------
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS_ENTRENADOS = os.path.join(CARPETA_SCRIPT, "datos_entrenados.yaml")


# ----------------------------------------------------------------------
# Carga de datos
# ----------------------------------------------------------------------
def cargar_datos_entrenados(ruta):
    """
    Lee "datos_entrenados.yaml" generado por entrenador.py.
    Devuelve una tupla (caracteristicas, animales), donde:
        - caracteristicas: lista de strings, en orden de significancia.
        - animales: lista de dicts {"nombre":..., "respuestas":[...], "peso": int}.
    Si el archivo no existe o está vacío, termina el programa con un
    mensaje claro.
    """
    if not os.path.exists(ruta):
        print(f'No se encontró el archivo "{ruta}".')
        print("Ejecuta primero inicializador.py y luego entrenador.py.")
        sys.exit(1)

    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = yaml.safe_load(archivo)

    if not contenido or not contenido.get("animales") or not contenido.get("caracteristicas"):
        print(f'El archivo "{ruta}" está vacío o mal formado.')
        sys.exit(1)

    return contenido["caracteristicas"], contenido["animales"]


# ----------------------------------------------------------------------
# Entrada de datos
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


# ----------------------------------------------------------------------
# Lógica de adivinanza
# ----------------------------------------------------------------------
def mostrar_lista_animales(animales):
    """
    Imprime la lista numerada de animales disponibles, en el mismo
    orden en que están guardados en datos_entrenados.yaml.
    """
    print("Animales disponibles:")
    for numero, animal in enumerate(animales, start=1):
        print(f"  {numero}. {animal['nombre']}")
    print()


def elegir_mejor_caracteristica(candidatos, caracteristicas, indices_preguntados):
    """
    Entre las características que aún NO se han preguntado, elige la
    que divide de forma más pareja al grupo de candidatos actuales
    (minimiza la diferencia entre cuántos la cumplen y cuántos no).
    En caso de empate entre varias igual de parejas, se toma la
    primera en el orden de la lista (la de mayor peso/bit).

    Devuelve el índice de la característica elegida, o None si ya no
    quedan características sin preguntar.
    """
    mejor_indice = None
    mejor_diferencia = None

    for indice, _caracteristica in enumerate(caracteristicas):
        if indice in indices_preguntados:
            continue

        cantidad_cumple = sum(1 for animal in candidatos if animal["respuestas"][indice])
        cantidad_no_cumple = len(candidatos) - cantidad_cumple
        diferencia = abs(cantidad_cumple - cantidad_no_cumple)

        if mejor_diferencia is None or diferencia < mejor_diferencia:
            mejor_diferencia = diferencia
            mejor_indice = indice

    return mejor_indice


def resolver_empate_final(primer_candidato, segundo_candidato):
    """
    Caso especial: quedan exactamente 2 candidatos con las mismas
    respuestas registradas (mismo peso), por lo que ninguna
    característica entrenada los distingue. Se pregunta directamente
    por el primero de la lista; si el usuario confirma, ese es el
    animal, si no, es el otro.
    """
    pregunta = f"Tu animal es: {primer_candidato['nombre']}? (S/N): "
    if pedir_respuesta_si_no(pregunta):
        return primer_candidato
    return segundo_candidato


def adivinar_animal(animales, caracteristicas):
    """
    Ejecuta el algoritmo de adivinanza dinámico (divide y vencerás)
    hasta identificar un único animal candidato. Devuelve el dict del
    animal adivinado.
    """
    candidatos = list(animales)          # Copia; se irá filtrando
    indices_preguntados = set()          # Características ya usadas en esta partida

    while len(candidatos) > 1:
        if len(candidatos) == 2:
            return resolver_empate_final(candidatos[0], candidatos[1])

        indice = elegir_mejor_caracteristica(candidatos, caracteristicas, indices_preguntados)

        if indice is None:
            # No deberían quedar más de 2 candidatos sin preguntas
            # disponibles (el entrenador garantiza como máximo 2
            # animales por peso), pero por seguridad avisamos y
            # detenemos aquí en lugar de fallar.
            print("No hay más características para seguir distinguiendo entre los candidatos.")
            print("Animales posibles: " + ", ".join(a["nombre"] for a in candidatos))
            sys.exit(0)

        indices_preguntados.add(indice)
        caracteristica = caracteristicas[indice]
        respuesta = pedir_respuesta_si_no(f"Tu animal cumple con: {caracteristica}? (S/N): ")

        nuevos_candidatos = [
            animal for animal in candidatos if animal["respuestas"][indice] == respuesta
        ]

        if not nuevos_candidatos:
            # Las respuestas del usuario no coinciden con ningún
            # animal de la base de conocimiento.
            print("No se encontró ningún animal que coincida con tus respuestas.")
            sys.exit(0)

        candidatos = nuevos_candidatos

    return candidatos[0]


# ----------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------
def main():
    print("=== Adivinador del Sistema Experto ===\n")

    caracteristicas, animales = cargar_datos_entrenados(RUTA_DATOS_ENTRENADOS)

    mostrar_lista_animales(animales)

    print("Piensa en uno de los animales de la lista y responde con S/N.\n")

    animal_adivinado = adivinar_animal(animales, caracteristicas)

    print(f"\n¡Tu animal es: {animal_adivinado['nombre']}!")


if __name__ == "__main__":
    main()
