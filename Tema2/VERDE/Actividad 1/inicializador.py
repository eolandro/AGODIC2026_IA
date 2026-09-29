"""
inicializador.py
-----------------
Primer script del Sistema Experto.

Responsabilidad de este archivo:
    1) Preguntar al supervisor los nombres de los animales que formarán
       parte de la base de conocimiento (mínimo 10 en total).
    2) Una vez cerrada la lista de nombres, preguntar la característica
       inicial (1 o 2 palabras) de cada animal NUEVO agregado en esta
       ejecución.
    3) Guardar (o actualizar, si ya existía) todo en un archivo YAML
       llamado "datos_iniciales.yaml".

Formato del YAML generado (una lista de pares, en el orden en que
se capturaron -- este orden es importante porque entrenador.py lo
usará para definir el peso/significancia de cada característica):

    animales:
      - nombre: Caballo
        caracteristica: Veloz
      - nombre: Gallina
        caracteristica: Pico
      ...

Reglas de negocio implementadas:
    - No se permiten animales con nombre repetido (comparando sin
      importar mayúsculas/minúsculas).
    - No se permiten características repetidas entre animales (cada
      característica inicial debe ser única en toda la tabla).
    - Solo se pregunta "¿desea terminar la lista?" cuando ya se tienen
      al menos 10 animales en total (existentes + nuevos).
    - Si el archivo YAML ya existe (reentrenamientos previos), los
      animales nuevos se AGREGAN a los ya existentes, sin borrar nada.
    - Las respuestas de tipo Sí/No deben ser estrictamente "S" o "N"
      (sin importar mayúsculas/minúsculas); cualquier otra entrada se
      vuelve a pedir.
"""

import os
import yaml

# ----------------------------------------------------------------------
# Constantes de configuración
# ----------------------------------------------------------------------
# Carpeta donde vive este script (independiente de desde dónde se ejecute)
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

RUTA_YAML = os.path.join(CARPETA_SCRIPT, "datos_iniciales.yaml")  # YAML de la base de conocimiento inicial
MINIMO_ANIMALES = 10                 # Cantidad mínima de animales exigida antes de poder terminar


# ----------------------------------------------------------------------
# Funciones de manejo de archivo YAML
# ----------------------------------------------------------------------
def cargar_datos_existentes(ruta):
    """
    Carga el YAML existente (si lo hay) y devuelve la lista de pares
    animal-característica ya guardados. Si el archivo no existe, o
    está vacío, devuelve una lista vacía.
    """
    if not os.path.exists(ruta):
        return []

    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = yaml.safe_load(archivo)

    # Si el archivo existe pero está vacío o mal formado, devolvemos lista vacía
    if not contenido or "animales" not in contenido:
        return []

    return contenido["animales"]


def guardar_datos(ruta, lista_animales):
    """
    Guarda (sobrescribiendo) la lista completa de animales en el YAML.
    Usamos allow_unicode=True para que se guarden correctamente
    caracteres como "ñ" o vocales con acento.
    sort_keys=False para respetar el orden nombre -> caracteristica.
    """
    contenido = {"animales": lista_animales}
    with open(ruta, "w", encoding="utf-8") as archivo:
        yaml.safe_dump(
            contenido,
            archivo,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )


# ----------------------------------------------------------------------
# Funciones auxiliares de validación / entrada de datos
# ----------------------------------------------------------------------
def pedir_respuesta_si_no(pregunta):
    """
    Pide al supervisor una respuesta estrictamente "S" o "N"
    (sin importar mayúsculas/minúsculas). Reintenta hasta obtener
    una respuesta válida. Devuelve True para "S" y False para "N".
    """
    while True:
        respuesta = input(pregunta).strip().upper()
        if respuesta == "S":
            return True
        if respuesta == "N":
            return False
        print('  -> Respuesta inválida. Debes escribir "S" o "N".')


def pedir_nombre_animal(nombres_existentes):
    """
    Pide el nombre de un nuevo animal, validando que:
        - No esté vacío.
        - No exista ya en la lista (comparación sin distinguir
          mayúsculas/minúsculas).
    nombres_existentes: set con los nombres ya usados en minúsculas,
    para poder comparar de forma normalizada.
    """
    while True:
        nombre = input("Nombre del animal: ").strip()

        if not nombre:
            print("  -> El nombre no puede estar vacío.")
            continue

        if nombre.casefold() in nombres_existentes:
            print(f'  -> El animal "{nombre}" ya existe en la lista. Intenta con otro.')
            continue

        return nombre


def pedir_caracteristica(animal, caracteristicas_existentes):
    """
    Pide la característica inicial de un animal, validando que:
        - No esté vacía.
        - Tenga 1 o 2 palabras (según lo especificado: "Rápido",
          "Dientes Grandes", etc).
        - No se repita respecto a las características ya usadas por
          otros animales (comparación sin distinguir mayúsculas/minúsculas).
    caracteristicas_existentes: set con las características ya usadas,
    en minúsculas, para comparar de forma normalizada.
    """
    while True:
        caracteristica = input(f'Característica de "{animal}": ').strip()

        if not caracteristica:
            print("  -> La característica no puede estar vacía.")
            continue

        cantidad_palabras = len(caracteristica.split())
        if cantidad_palabras not in (1, 2):
            print("  -> La característica debe tener 1 o 2 palabras.")
            continue

        if caracteristica.casefold() in caracteristicas_existentes:
            print(f'  -> La característica "{caracteristica}" ya está en uso. Debe ser única.')
            continue

        return caracteristica


# ----------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------
def main():
    print("=== Inicializador del Sistema Experto ===\n")

    # 1) Cargamos lo que ya existiera de ejecuciones anteriores
    animales_existentes = cargar_datos_existentes(RUTA_YAML)

    # Sets de apoyo para validar duplicados en O(1), normalizados en minúsculas
    nombres_usados = {a["nombre"].casefold() for a in animales_existentes}
    caracteristicas_usadas = {a["caracteristica"].casefold() for a in animales_existentes}

    total_actual = len(animales_existentes)
    if total_actual > 0:
        print(f"Se encontraron {total_actual} animal(es) ya registrados en '{RUTA_YAML}'.")
        print("Los nuevos animales se agregarán a esta lista.\n")

    # ------------------------------------------------------------------
    # FASE 1: captura de nombres de animales nuevos
    # ------------------------------------------------------------------
    nombres_nuevos = []  # Solo los nombres agregados en ESTA ejecución, en orden de captura

    while True:
        nombre = pedir_nombre_animal(nombres_usados)
        nombres_nuevos.append(nombre)
        nombres_usados.add(nombre.casefold())
        total_actual += 1

        # Solo preguntamos si desea terminar cuando ya se alcanzó el mínimo global
        if total_actual >= MINIMO_ANIMALES:
            desea_terminar = pedir_respuesta_si_no(
                "¿Desea terminar la lista de animales? (S/N): "
            )
            if desea_terminar:
                break
        else:
            faltan = MINIMO_ANIMALES - total_actual
            print(f"  (Aún deben agregarse al menos {faltan} animal(es) más antes de poder terminar)")

    # ------------------------------------------------------------------
    # FASE 2: captura de la característica inicial de cada animal nuevo
    # ------------------------------------------------------------------
    print("\n--- Ahora indica la característica inicial de cada animal nuevo ---\n")

    animales_nuevos = []  # Lista de dicts {"nombre": ..., "caracteristica": ...}
    for nombre in nombres_nuevos:
        caracteristica = pedir_caracteristica(nombre, caracteristicas_usadas)
        caracteristicas_usadas.add(caracteristica.casefold())
        animales_nuevos.append({"nombre": nombre, "caracteristica": caracteristica})

    # ------------------------------------------------------------------
    # FASE 3: fusionar con lo existente y guardar
    # ------------------------------------------------------------------
    lista_final = animales_existentes + animales_nuevos
    guardar_datos(RUTA_YAML, lista_final)

    print(f"\nListo. Se guardaron {len(animales_nuevos)} animal(es) nuevo(s).")
    print(f"Total de animales en '{RUTA_YAML}': {len(lista_final)}.")


if __name__ == "__main__":
    main()