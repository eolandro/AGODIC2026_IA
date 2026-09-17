import argparse
import BVM
import anlexsyn
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("código", type=argparse.FileType('r'))
args = parser.parse_args()

def armarBloques(Lineas):
    def armar(Indice):
        Bloque = []
        while Indice < len(Lineas):
            Linea = Lineas[Indice]
            Partes = Linea.split()
            match Partes:
                case [Apertura,Re] if Apertura.lower() == "ciclo":
                    Sub,Indice = armar(Indice + 1)
                    Bloque.append(["ciclo",Re,Sub,"finciclo"])
                    Indice += 1
                case [Cierre] if Cierre.lower() == "finciclo":
                    return Bloque,Indice
                case [Apertura,Re] if Apertura.lower() == "si":
                    Sub,Indice = armar(Indice + 1)
                    Bloque.append(["Si",Re,Sub,"FinSi"])
                    Indice += 1
                case [Cierre] if Cierre.lower() == "finsi":
                    return Bloque,Indice
                case _:
                    Bloque.append(Linea)
                    Indice += 1
        return Bloque,Indice
    Resultado,_ = armar(0)
    return Resultado

def main():
    LineasCódigo = args.código.readlines()
    LineasCodigo = [linea.strip() for linea in LineasCódigo]
    LineasCodigo = [linea for linea in LineasCodigo if linea]
    LineasAnidadas = armarBloques(LineasCodigo)
    LineasValidas = anlexsyn.lineas(LineasAnidadas)
    print(LineasValidas)
    if not LineasValidas[0]:
        print("Error encontrado en: ", LineasValidas[1])
        #ToDo Colocar el error según la lista
        return
    BooMe = BVM.BoomeVirtualMachine()
    BooMe.loadText(LineasAnidadas)
    print (BooMe)
    #while BooMe.Estado not in ["dead","done"]:
    while BooMe.Estado == "ready":
        BooMe.step()
        print (BooMe)
    print("Terminado :)")

if __name__ == "__main__":
    main()