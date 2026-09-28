import os
from utilidades import cargar_json, ganancia_informacion, preguntar_si_no

DIR_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_ANIMALES = os.path.join(DIR_BASE, "animales.json")
ARCHIVO_PESOS = os.path.join(DIR_BASE, "pesos.json")


def elegir_mejor_pregunta(candidatos, preguntas_disponibles, pesos_globales):
    mejor_clave = None
    mejor_ganancia = -1.0
    for clave in preguntas_disponibles:
        g = ganancia_informacion(clave, candidatos)
        peso_global = pesos_globales.get(clave, 0.0)
        # Se compara primero por ganancia local; en empate, por peso global
        if (g > mejor_ganancia or
                (g == mejor_ganancia and peso_global > pesos_globales.get(mejor_clave, -1.0))):
            mejor_ganancia = g
            mejor_clave = clave
    return mejor_clave, mejor_ganancia


def filtrar_candidatos(candidatos, clave, respuesta):
    return {n: a for n, a in candidatos.items() if a.get(clave) == respuesta}


def resolver_empate(candidatos):
    nombres = list(candidatos.keys())
    print("\nCon las características registradas no puedo distinguir entre:")
    for i, n in enumerate(nombres, 1):
        print(f"  {i}) {n}")
    while True:
        try:
            idx = int(input("¿Cuál es? (número): ").strip())
            if 1 <= idx <= len(nombres):
                return nombres[idx - 1]
        except ValueError:
            pass
        print("  -> Opción no válida.")


def adivinar():
    datos = cargar_json(ARCHIVO_ANIMALES)
    if datos is None:
        print("ERROR: No existe 'animales.json'.")
        print("Ejecuta primero 'inicializador.py' para crear la base de conocimiento.")
        return

    if len(datos.get("animales", {})) < 2:
        print("ERROR: Se necesitan al menos 2 animales en 'animales.json'.")
        return

    pesos_data = cargar_json(ARCHIVO_PESOS)
    if pesos_data is not None:
        pesos_globales = {clave: g for clave, g in pesos_data["pesos"]}
    else:
        pesos_globales = {}  # se recalcula todo dinámicamente, sin problema

    caracteristicas = datos["caracteristicas"]
    candidatos = dict(datos["animales"])          # copia: candidatos actuales
    preguntas_disponibles = list(caracteristicas.keys())

    print("\n=== ADIVINADOR ===")
    print("Piensa un animal (de los que conoce el sistema) y responde s/n.\n")

    num_preguntas = 0

    while True:
        # Caso 1: ya se identificó un único candidato
        if len(candidatos) == 1:
            animal = next(iter(candidatos))
            correcto = preguntar_si_no(f"Creo que tu animal es: '{animal}'. ¿Acerté?")
            print(f"\n¡Listo! Preguntas realizadas: {num_preguntas}.")
            if not correcto:
                print("Vaya, no acerté. Considera agregar/corregir información "
                      "con 'inicializador.py' para mejorar al sistema.")
            else:
                print("¡Adiviné correctamente!")
            return

        # Caso 2: contradicción -> ningún animal conocido cumple las respuestas
        if len(candidatos) == 0:
            print(f"\nNo tengo ningún animal que cumpla esas características "
                  f"(después de {num_preguntas} preguntas).")
            print("Puede que sea un animal nuevo. Usa 'inicializador.py' para agregarlo.")
            return

        # Caso 3: ya no hay preguntas que sirvan para separar a los candidatos
        if not preguntas_disponibles:
            animal = resolver_empate(candidatos)
            print(f"\n¡Es '{animal}'! Preguntas realizadas: {num_preguntas}.")
            return

        # Caso general: elegir la mejor pregunta para el subconjunto actual
        clave, ganancia = elegir_mejor_pregunta(candidatos, preguntas_disponibles, pesos_globales)

        if ganancia <= 0.0:
            # Ninguna pregunta restante separa a los candidatos actuales
            animal = resolver_empate(candidatos)
            print(f"\n¡Es '{animal}'! Preguntas realizadas: {num_preguntas}.")
            return

        pregunta = caracteristicas.get(clave, f"¿{clave}?")
        respuesta = preguntar_si_no(pregunta)
        num_preguntas += 1

        candidatos = filtrar_candidatos(candidatos, clave, respuesta)
        preguntas_disponibles.remove(clave)


if __name__ == "__main__":
    adivinar()
