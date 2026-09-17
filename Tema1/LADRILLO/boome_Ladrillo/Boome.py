

import argparse 
from pathlib import Path #Necesitamos archivos
#parametros generales para niestra app
import anlexsyn
import BVM

parser = argparse.ArgumentParser()
parser.add_argument ("Codigo", type = argparse.FileType('r'))

args = parser.parse_args()


def main():
    LineasCodigo = args.Codigo.readlines()
    LineasCodigo = [linea.strip() for linea in LineasCodigo if linea.strip()]
    LineasValidas = [anlexsyn.linea(linea)[0] for linea in LineasCodigo]
    
    print(LineasValidas)
    if not all(LineasValidas):
        print('Error encontrado en:')
        return
    BooMe = BVM.BoomeVirtualMachine()
    BooMe.loadText(LineasCodigo)
    print(BooMe)
    
    while BooMe.Estado == "ready":
        BooMe.step()
        print(BooMe)
    print("Terminado")


if __name__ == "__main__":
    main() 


