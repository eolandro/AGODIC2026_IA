# ----------R003 Subir la colina con estrategia corta y estrategia larga
import json
# Leemos el archivo con los caminos [nodo, nodo, peso]
archivo = open("colina.json", encoding="utf-8")
caminos = json.load(archivo)
archivo.close()
# Armamos el grafo: cada nodo tiene su lista de [vecino, peso]
grafo = {}
for c in caminos:
    a = c[0]
    b = c[1]
    peso = c[2]
    if a not in grafo:
        grafo[a] = []
    if b not in grafo:
        grafo[b] = []
    grafo[a].append([b, peso])
    grafo[b].append([a, peso])

# Regresa la lista de vecinos de un nodo
def obtener_vecinos(nodo):
    return grafo[nodo]

# Subir la colina estrategia puede ser "corta" o "larga"
def subir_colina(raiz, buscado, estrategia, limite):
    if raiz not in grafo:
        print("La raiz", raiz, "no existe en el grafo")
        return False

    actual = raiz
    cache = []
    recorrido = [actual]
    costo = 0
    paso = 0

    print()
    print("Subir la colina - estrategia", estrategia, "- de", raiz, "a", buscado,
        "- limite", limite, "pasos")
    print()
    print("Paso".ljust(6) + "Actual".ljust(8) + "Vecinos (peso)".ljust(26) + "Elige".ljust(10) + "Cache")
    print("-" * 80)

    while paso < limite:
        paso = paso + 1

        if actual == buscado:
            print(str(paso).ljust(6) + actual.ljust(8) + "-".ljust(26) + "Llegue".ljust(10) + ", ".join(cache))
            print("-" * 80)
            print("Recorrido:", " -> ".join(recorrido))
            print("Costo total:", costo)
            return True

        # Solo podemos ir a los vecinos que no estan en el cache
        vecinos = obtener_vecinos(actual)
        opciones = []
        for v in vecinos:
            if v[0] not in cache:
                opciones.append(v)

        # Texto de los vecinos para la tabla, ejemplo: O(10) P(11)*
        # el * indica que ese vecino esta en el cache
        texto = ""
        for v in vecinos:
            if v[0] in cache:
                texto = texto + v[0] + "(" + str(v[1]) + ")* "
            else:
                texto = texto + v[0] + "(" + str(v[1]) + ") "

        if len(opciones) == 0:
            print(str(paso).ljust(6) + actual.ljust(8) + texto.ljust(26) + "Atorado".ljust(10) + ", ".join(cache))
            print("-" * 80)
            print("No hay caminos disponibles, el algoritmo se atoro")
            print("Recorrido:", " -> ".join(recorrido))
            return False

        # Buscamos el camino mas corto o el mas largo
        mejor = opciones[0]
        for v in opciones:
            if estrategia == "corta" and v[1] < mejor[1]:
                mejor = v
            if estrategia == "larga" and v[1] > mejor[1]:
                mejor = v

        # Guardamos el nodo anterior en el cache (maximo 3)
        cache.append(actual)
        if len(cache) > 3:
            descartado = cache.pop(0)   # se descarta el mas viejo
            print("      (se descarta", descartado, "del cache)")

        print(str(paso).ljust(6) + actual.ljust(8) + texto.ljust(26)
            + (mejor[0] + "(" + str(mejor[1]) + ")").ljust(10) + ", ".join(cache))

        actual = mejor[0]
        recorrido.append(actual)
        costo = costo + mejor[1]

    print("-" * 80)
    print("Recorrido:", " -> ".join(recorrido))
    if actual == buscado:
        print("Costo total:", costo)
        return True
    print("Se alcanzo el limite de", limite, "pasos sin encontrar", buscado)
    return False


# Estrategia corta
def corta(raiz, buscado, limite=20):
    return subir_colina(raiz, buscado, "corta", limite)


# Estrategia larga 
def larga(raiz, buscado, limite=20):
    return subir_colina(raiz, buscado, "larga", limite)


print("==============================================")
print("      SUBIR LA COLINA  EQUIPO NARANJA ")
print("==============================================")
print("Nodos:", ", ".join(grafo))
print("Escribe la estrategia con la raiz y el elemento a buscar")
print("entre comillas y en MAYUSCULAS")
print('Ejemplo:  corta("Ñ","A")   o   larga("Ñ","A")')
print('Para cambiar el limite de pasos:  corta("Ñ","A",5)')
print("Escribe S para salir")
print("En la tabla, * indica un vecino que esta en el cache")

# REPL
while True:
    command = input(">")
    if command == "S":
        break
    T = eval(command)
    print(T)

