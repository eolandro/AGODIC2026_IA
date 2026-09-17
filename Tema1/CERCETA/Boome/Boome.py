import argparse
import alexsyn
import BVM


parser = argparse.ArgumentParser(
    description="Ejecuta un programa de BoomeVirtualMachine"
)

parser.add_argument(
    "codigo",
    type=argparse.FileType("r", encoding="utf-8"),
    help="Archivo .boome que contiene las instrucciones"
)

args = parser.parse_args()


def armar_bloques(lineas):
    """Convierte la lista PLANA de líneas de texto (una por línea del
    archivo) en una lista ANIDADA, agrupando cada bloque Si/ciclo junto
    con las líneas que tiene adentro
    Las palabras de apertura/cierre (Si, FinSi, ciclo, finciclo) se
    reconocen sin importar si vienen en mayúsculas o minúsculas."""

    def armar(indice):
        bloque = []
        while indice < len(lineas):
            texto = lineas[indice]
            partes = [t for t in texto.split(" ") if t]
            match partes:
                case [apertura, registro] if apertura.lower() == "ciclo":
                    # Abrimos un ciclo: procesamos todo lo de adentro con una llamada recursiva, hasta toparnos con sufinciclo' correspondiente.
                    sub, indice = armar(indice + 1)
                    bloque.append(["ciclo", registro, sub, "finciclo"])
                    indice += 1
                case [cierre] if cierre.lower() == "finciclo":
                    # Encontramos el cierre: regresamos lo acumulado para que lo use la llamada que abrió este ciclo.
                    return bloque, indice
                case [apertura, registro] if apertura.lower() == "si":
                    sub, indice = armar(indice + 1)
                    bloque.append(["Si", registro, sub, "FinSi"])
                    indice += 1
                case [cierre] if cierre.lower() == "finsi":
                    return bloque, indice
                case _:
                    # Línea normal (movimiento o asignación): se agrega tal cual.
                    bloque.append(texto)
                    indice += 1
        return bloque, indice
    resultado, _ = armar(0)
    return resultado

def main():
    # Leer el archivo y eliminar líneas vacías
    lineas_codigo = [
        linea.strip()
        for linea in args.codigo.readlines()
        if linea.strip()
    ]
    #Convertir la lista plana en la estructura anidada de bloques.
    lineas_anidadas = armar_bloques(lineas_codigo)

    #Validar la sintaxis completa (recorre también dentro de los bloques).
    resultado = alexsyn.lineas(lineas_anidadas)

    if not resultado[0]:
        print("Se encontraron instrucciones incorrectas:")
        print(resultado)
        return

    #Si la sintaxis es válida, se ejecuta en la máquina virtual.
    boome = BVM.BoomeVirtualMachine()
    boome.loadText(lineas_anidadas)

    print("\nEstado inicial:")
    print(boome)

    while boome.Estado == "ready":
        boome.step()
        print("\nDespués de ejecutar una instrucción:")
        print(boome)

    print("\nTerminado")


if __name__ == '__main__':
    raise SystemExit(main())