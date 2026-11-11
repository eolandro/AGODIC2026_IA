import json
# ---------- Leer el arbol del archivo ----------
archivo = open("rel.json")
relaciones = json.load(archivo)
archivo.close()

# Armamos el arbol: cada nodo tiene su lista de hijos
arbol = {}
for par in relaciones:
    padre = par[0]
    hijo = par[1]
    if padre not in arbol:
        arbol[padre] = []
    if hijo not in arbol:
        arbol[hijo] = []
    arbol[padre].append(hijo)
# ---------- Metodo para obtener los hijos ----------
def obtener_hijos(nodo):
    return arbol[nodo]

# ----------R001  Primero en anchura  -------------------------------------------
def anchura(raiz, buscado):
    if raiz not in arbol:
        print("La raiz no existe")
        return False
    print("Paso".ljust(6) + "Raiz".ljust(8) + "Hijos agregados".ljust(24) + "Cola")
    print("-" * 70)
    cola = [raiz]
    recorrido = []
    paso = 0
    while len(cola) > 0:
        raiz = cola.pop(0)          # sacamos el PRIMERO de la cola
        recorrido.append(raiz)
        paso = paso + 1
        if raiz == buscado:         # revisamos si es el buscado
            print(str(paso).ljust(6) + raiz.ljust(8) + "Encontrado!")
            print("Recorrido:", recorrido)
            return True
        hijos = obtener_hijos(raiz)
        for hijo in hijos:
            cola.append(hijo)       # los hijos van al FINAL de la cola
        print(str(paso).ljust(6) + raiz.ljust(8) + str(hijos).ljust(24) + str(cola))
    print("Recorrido:", recorrido)
    return False

# ---------- R002  Primero en profundidad ----------

def profundidad(raiz, buscado):
    if raiz not in arbol:
        print("La raiz no existe")
        return False
    print("Paso".ljust(6) + "Raiz".ljust(8) + "Hijos agregados".ljust(24) + "Pila")
    print("-" * 70)
    pila = [raiz]
    recorrido = []
    paso = 0
    while len(pila) > 0:
        raiz = pila.pop()           # sacamos el ULTIMO de la pila
        recorrido.append(raiz)
        paso = paso + 1
        if raiz == buscado:         # revisamos si es el buscado
            print(str(paso).ljust(6) + raiz.ljust(8) + "Encontrado!")
            print("Recorrido:", recorrido)
            return True
        hijos = obtener_hijos(raiz)
        for hijo in hijos:
            pila.append(hijo)       # los hijos van arriba de la pila

        print(str(paso).ljust(6) + raiz.ljust(8) + str(hijos).ljust(24) + str(pila))

    print("Recorrido:", recorrido)
    return False
print("===============================================================")
print("   BUSQUEDA LOCAL EN ANCHURA Y EN PROFUNDIDAD  EQUIPO NARANJA")
print("===============================================================")
print("Arbol (padre -> hijos):")
for nodo in arbol:
    if len(arbol[nodo]) > 0:
        print("  ", nodo, "->", ", ".join(arbol[nodo]))
print("\n Nodos que puedes usar:", ", ".join(arbol))
print("Escribe la funcion con la raiz y el elemento a buscar")
print('Ejemplo:  anchura("O","OKEN")   o   profundidad("O","OKEN")')
print("Escribe S para salir")

while True:
    command = input(">")
    if command == "S":
        break
    T = eval(command)
    print(T)
    
