"""Programa principal del intérprete Boome."""

import argparse
import anlexsyn
from BVM import BoomeVirtualMachine


def construir_arbol(lineas):
    def leer(posicion, cierre=None):
        contenido = []

        while posicion < len(lineas):
            partes = lineas[posicion].split()

            if len(partes) == 1 and partes[0] in {"FinSi", "finciclo"}:
                if cierre != partes[0]:
                    raise SyntaxError(
                        f"Cierre inesperado en línea {posicion + 1}"
                    )
                return contenido, posicion + 1

            if len(partes) == 2 and partes[0] in {"Si", "ciclo"}:
                tipo, registro = partes
                cierre_bloque = "FinSi" if tipo == "Si" else "finciclo"
                interior, siguiente = leer(posicion + 1, cierre_bloque)
                contenido.append([tipo, registro, interior, cierre_bloque])
                posicion = siguiente
                continue

            contenido.append(lineas[posicion])
            posicion += 1

        if cierre is not None:
            raise SyntaxError(f"Falta el cierre {cierre}")
        return contenido, posicion

    programa, final = leer(0)
    if final != len(lineas):
        raise SyntaxError("El programa contiene líneas sin procesar")
    return programa


def leer_fuente(nombre):
    with open(nombre, encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]


def main():
    parser = argparse.ArgumentParser(description="Intérprete del agente Boome")
    parser.add_argument("codigo", help="archivo fuente .boome")
    argumentos = parser.parse_args()

    try:
        fuente = leer_fuente(argumentos.codigo)
        programa = construir_arbol(fuente)
        validacion = anlexsyn.lineas(programa)

        if not validacion[0]:
            print("Código inválido:")
            print(validacion[1])
            return 1

        maquina = BoomeVirtualMachine()
        maquina.LoadText(programa)

        print("Estado inicial:")
        print(maquina)

        while maquina.Estado == "ready":
            maquina.step()
            print("\nEstado actual:")
            print(maquina)

        print(f"\nPrograma terminado: {maquina.Estado}")
        return 0

    except (OSError, SyntaxError, ValueError) as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
