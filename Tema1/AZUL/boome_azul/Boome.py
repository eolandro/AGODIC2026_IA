import argparse
from pathlib import Path


from alenxsyn import analizar_archivo
from bvm import BoomeVirtualMachineCompleta


def main():
    pass

    parser = argparse.ArgumentParser(
        description="Interprete del lenguaje Boome"
    )
    parser.add_argument(
        "archivo",
        nargs="?",
        default="ejemplo.boome",
        help="archivo fuente escrito en lenguaje Boome"
    )
    argumentos = parser.parse_args()

    ruta = Path(argumentos.archivo)
    resultado = analizar_archivo(str(ruta))

    if not resultado[0]:
        print("Error de analisis:", resultado[1])
        return

    boome = BoomeVirtualMachineCompleta()
    cargado = boome.loadText(resultado[1])

    if not cargado[0]:
        print("Error de carga:", cargado[1])
        return

    boome.run()
    print(boome)


if __name__ == "__main__":
    main()
