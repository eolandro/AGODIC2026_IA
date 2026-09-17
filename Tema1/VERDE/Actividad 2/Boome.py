import argparse
import anlexsyn
import BVM

from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("codigo", type = argparse.FileType('r'))
args = parser.parse_args()

def leerCodigo(Archivo):
    #lee el archivo fuente y limpia tabuladores (usados para indentar
    #bloques Si/ciclo) y saltos de linea
    LineasCodigo = Archivo.readlines()
    LineasCodigo = [linea.replace('\t', '').strip() for linea in LineasCodigo]
    #descartamos lineas que quedaron vacias (lineas en blanco o solo con espacios/tabs)
    LineasCodigo = [linea for linea in LineasCodigo if linea]
    return LineasCodigo

def validarCodigo(LineasCodigo):
    #arma la estructura anidada de bloques (Si/FinSi, ciclo/finciclo) y
    #valida el programa completo de forma recursiva con anlexsyn
    Bloques, _ = anlexsyn.construirBloques(LineasCodigo)
    return Bloques, anlexsyn.lineas(Bloques)

def main():
    LineasCodigo = leerCodigo(args.codigo)
    Bloques, Validacion = validarCodigo(LineasCodigo)
    print(Validacion)
    if len(Validacion) != 1:
        print('Error encontrado en el codigo fuente:')
        print(Validacion[1])
        return

    BooMe = BVM.BoomeVirtualMachine()
    BooMe.loadText(Bloques)
    print(BooMe)
    while BooMe.Estado == "ready":
        BooMe.step()
        print(BooMe)
    print("Terminado :)")

if __name__ == "__main__":
    main()