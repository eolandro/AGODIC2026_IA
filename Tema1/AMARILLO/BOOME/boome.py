import argparse
import anlexsyn
import BVM
parser = argparse.ArgumentParser()
parser.add_argument(
    "codigo",
    type=argparse.FileType("r")
)
args = parser.parse_args()

def armarBloques(lineas):
    bloques = []
    i = 0
    while i < len(lineas):
        partes = lineas[i].split(" ")
        if partes[0] == "Si":
            cuerpo = []
            i += 1
            while i < len(lineas) and lineas[i] != "FinSi":
                cuerpo.append(lineas[i])
                i += 1
            bloques.append(["Si", partes[1], cuerpo, "FinSi"])
        elif partes[0] == "ciclos":
            cuerpo = []
            i += 1
            while i < len(lineas) and lineas[i] != "Finciclo":
                cuerpo.append(lineas[i])
                i += 1
            bloques.append(["ciclos", partes[1], cuerpo, "Finciclo"])
        else:
            bloques.append(lineas[i])
        i += 1
    return bloques

def main():
    LineasCodigo = args.codigo.readlines()
    LineasCodigo = [
        linea.strip()
        for linea in LineasCodigo
        if linea.strip()
    ]
    LineasCodigo = armarBloques(LineasCodigo)

    LineasValidas = [
        anlexsyn.linea(linea)
        for linea in LineasCodigo
    ]
    print(LineasValidas)
    ###############
    for lineas in LineasValidas:
        if lineas[0] == False:
            print ("ERROR ENCONTRADO")
            return
    ###############
    """""
    if not all(LineasValidas):
        print("ERROR ENCONTRADO")
        return
    """
    Boome = BVM.BoomeVirtualMachine()
    Boome.loadText(LineasCodigo)
    print(Boome)
    while Boome.Estado == "ready":
        Boome.step()
        print(Boome)
    print("terminado")

main()