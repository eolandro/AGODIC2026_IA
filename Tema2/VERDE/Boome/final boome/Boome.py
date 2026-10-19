import argparse
import json
import BVM

from pathlib import Path

#sin argumento se usa tablero.json junto a este archivo (sirve al ejecutar con "Run" del editor)
parser = argparse.ArgumentParser()
parser.add_argument("tablero", nargs = "?", type = argparse.FileType('r'),
                    default = str(Path(__file__).with_name("tablero.json")))
args = parser.parse_args()

def main():
    try:
        Tablero = json.load(args.tablero)
    except json.JSONDecodeError as e:
        print(f'El tablero no es un JSON valido: {e}')
        return
    Valido = BVM.valida_tablero(Tablero)
    if len(Valido) != 1:
        print(f'Error en el tablero: {Valido[1]}')
        return
    BooMe = BVM.BoomeVirtualMachine(Tablero)
    filas, cols = len(BooMe.Mapa), len(BooMe.Mapa[0])
    #espiral desde (0,0) convertida en instrucciones del lenguaje (sensor + movimiento)
    BooMe.loadText(BVM.programa(BVM.espiral(0, filas - 1, 0, cols - 1)))
    print(BooMe)
    print()
    while BooMe.Estado == "ready":
        BooMe.step()
        #se imprime al terminar cada casilla (despues de moverse) o si la ejecucion se detiene
        if BooMe.Ultima in BVM.DIRS or BooMe.Estado != "ready":
            print(BooMe)
            print()
    print("Terminado")

if __name__ == "__main__":
    main()