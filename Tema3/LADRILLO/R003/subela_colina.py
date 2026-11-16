import json
import os
import random  

def cargar_grafo(nombre_archivo="sc.json"):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

grafo = cargar_grafo()

def obtener_vecinos(nodo):
    vecinos = []
    for origen, destino, peso in grafo:
        if origen == nodo:
            vecinos.append((destino, peso))
        elif destino == nodo:
            vecinos.append((origen, peso))
    return vecinos

def obtener_peso(elemento):
    """Retorna el peso del camino para ordenar la lista."""
    return elemento[1]

def _escalada(raiz, objetivo, limite, menor_peso=True):
    if not grafo:
        print("El grafo no está disponible.")
        return False

    actual = raiz
    camino = [actual]
    cache_anteriores = []  # Máximo 3 nodos anteriores
    pasos = 0

    print(f"\n--- Inicio del Recorrido ---")
    print(f"Paso 0 | Nodo actual: '{actual}' | Caché anteriores: {cache_anteriores}")

    while pasos < limite:
        if actual == objetivo:
            print(f"\n¡Éxito! Nodo '{objetivo}' encontrado en {pasos} pasos.")
            print(f"Ruta completa: {' -> '.join(camino)}")
            print(f"Caché final de anteriores: {cache_anteriores}\n")
            return True

        vecinos = obtener_vecinos(actual)
        
        candidatos = [v for v in vecinos if v[0] not in cache_anteriores]

        if not candidatos:
            print(f"\nCamino bloqueado en '{actual}': Todos los vecinos {vecinos} están en el Caché anterior {cache_anteriores}.")
            break

        candidatos.sort(key=obtener_peso, reverse=not menor_peso)

        mejor_peso = candidatos[0][1]
        empates = [c for c in candidatos if c[1] == mejor_peso]

        if len(empates) > 1:
            # Si hay 2 o más opciones con el mismo peso, se elige una al azar
            opcion_elegida = random.choice(empates)
            print(f"  [DECISIÓN RANDOM]: Empate en '{actual}' con peso {mejor_peso} entre {[e[0] for e in empates]}. Se eligió al azar '{opcion_elegida[0]}'.")
        else:
            opcion_elegida = candidatos[0]

        siguiente_nodo, peso = opcion_elegida

        # Actualizar el Caché anterior
        cache_anteriores.append(actual)
        if len(cache_anteriores) > 3:
            cache_anteriores.pop(0)

        # Avanzar al siguiente nodo
        actual = siguiente_nodo
        camino.append(actual)
        pasos += 1

        print(f"Paso {pasos} | Salto a: '{actual}' (Peso: {peso}) | Caché anteriores: {cache_anteriores}")

    print(f"\nNo se alcanzó el objetivo '{objetivo}' dentro del límite de {limite} pasos.")
    print(f"Ruta explorada: {' -> '.join(camino)}\n")
    return False


def EC(raiz, objetivo, limite=50):
    """Estrategia Corta (EC): Elige el camino de menor peso."""
    print("\n================ Estrategia Corta (EC) ================")
    return _escalada(raiz, objetivo, limite, menor_peso=True)

def EL(raiz, objetivo, limite=50):
    """Estrategia Larga (EL): Elige el camino de mayor peso."""
    print("\n================ Estrategia Larga (EL) ================")
    return _escalada(raiz, objetivo, limite, menor_peso=False)


print("********************** SUBIR LA COLINA **********************")
print("Ejemplos de comandos:")
print(" Estrategia corta -> EC('Ñ', 'A', 50)")
print(" Estrategia Larga -> EL('P', 'U', 50)")
print("Escribe 'q' para salir.\n")

while True:
    comando = input("Ingrese búsqueda: ")
    if comando.lower() == 'q':
        print("Programa finalizado.")
        break
    try:
        eval(comando)
    except Exception as e:
        print(f"Error de sintaxis: {e}\n")