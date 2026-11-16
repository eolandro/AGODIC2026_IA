import argparse
import json
import sys
import anlexsyn
import astar
import BVM

parser = argparse.ArgumentParser()
parser.add_argument("tablero", help="archivo JSON con el tablero 10x10")
args = parser.parse_args()

#cargar(Ruta) :- abre el archivo y lo lee como JSON; cualquier fallo es un error legible
def cargar(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            return (True, json.load(archivo))
    except OSError as e:
        return (False, [f"No pude abrir '{ruta}': {e.strerror}"])
    except ValueError as e:
        return (False, [f"'{ruta}' no es un JSON valido: {e}"])

def error(mensajes):
    print('Error:')
    for m in mensajes:
        print(f' - {m}')
    return 1

def main():
    Cargado = cargar(args.tablero)
    if not Cargado[0]:
        return error(Cargado[1])

    Valido = anlexsyn.tablero(Cargado[1])
    if not Valido[0]:
        return error(Valido[1])
    Tablero = [[str(e) for e in fila] for fila in Cargado[1]]

    [Inicio] = astar.buscar_simbolo(Tablero, "R")
    [Meta] = astar.buscar_simbolo(Tablero, "B")

    Camino = astar.buscar(Tablero, Inicio, Meta)
    if not Camino[0]:
        return error([Camino[1]])
    Instrucciones = Camino[1]

    Valido = anlexsyn.lineas(Instrucciones)
    if not Valido[0]:
        return error([f"El camino generado no es valido: {Valido[1]}"])

    BooMe = BVM.BoomeVirtualMachine(Tablero, Inicio, Meta)
    BooMe.loadText(Instrucciones)
    while BooMe.Estado == "ready":
        BooMe.step()
    print(BooMe)
    return 0

if __name__ == "__main__":
    sys.exit(main())
