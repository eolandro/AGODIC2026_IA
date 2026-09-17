import argparse
from pathlib import Path

import BVM
from pyswip import Prolog


parser = argparse.ArgumentParser()
parser.add_argument(
    "codigo",
    type=argparse.FileType("r")
)

args = parser.parse_args()


def main():
    # La gramatica se busca en la misma carpeta del programa
    Ruta = Path(__file__).resolve().parent

    prolog = Prolog()
    prolog.consult(str(Ruta / "grammar.prolog"))

    LineasCodigo = args.codigo.readlines()
    LineasCodigo = [
        linea.strip() for linea in LineasCodigo
        if linea.strip()
    ]

    LineasValidas = []

    for linea in LineasCodigo:
        # Escapar comillas y barras para realizar la consulta a Prolog
        lineaProlog = linea.replace("\\", "\\\\").replace('"', '\\"')
        resultado = list(prolog.query(f'linea("{lineaProlog}")', maxresult=1))
        LineasValidas.append(bool(resultado))

    print(LineasValidas)

    if not all(LineasValidas):
        print("Error encontrado en:")

        for numero, (linea, valida) in enumerate(
            zip(LineasCodigo, LineasValidas), start=1
        ):
            if not valida:
                print(f"Linea {numero}: {linea}")

        return

    BooMe = BVM.BoomeVirtualMachine()
    BooMe.loadText(LineasCodigo)

    print(BooMe)

    while BooMe.Estado not in ["dead", "done"]:
        print("\n--------------------")
        BooMe.step()
        print(BooMe)

    print("\nTerminado")


if __name__ == "__main__":
    main()
