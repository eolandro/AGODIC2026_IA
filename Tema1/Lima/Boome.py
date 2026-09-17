# ─────────────────────────────────────────────────────────────────────────────
# Boome.py  —  Punto de entrada del intérprete Boome
# Uso: python Boome.py <archivo.boome>
# ─────────────────────────────────────────────────────────────────────────────

import argparse
import anlexsyn
import BVM

# ── Argumentos de línea de comandos ──────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Intérprete del lenguaje Boome"
)
parser.add_argument("código", type=argparse.FileType("r"), help="Archivo fuente .boome")
args = parser.parse_args()

# ── Convierte texto plano en bloques anidados ─────────────────────────────────
def armarBloques(lineas):
    def armar(indice):
        bloque = []
        while indice < len(lineas):
            linea  = lineas[indice]
            partes = linea.split()
            match partes:
                case [apertura, Re] if apertura.lower() == "ciclo":
                    sub, indice = armar(indice + 1)
                    bloque.append(["ciclo", Re, sub, "finciclo"])
                    indice += 1
                case [cierre] if cierre.lower() == "finciclo":
                    return bloque, indice
                case [apertura, Re] if apertura.lower() == "si":
                    sub, indice = armar(indice + 1)
                    bloque.append(["Si", Re, sub, "FinSi"])
                    indice += 1
                case [cierre] if cierre.lower() == "finsi":
                    return bloque, indice
                case _:
                    bloque.append(linea)
                    indice += 1
        return bloque, indice

    resultado, _ = armar(0)
    return resultado

# ── Programa principal ────────────────────────────────────────────────────────
def main():
    # Leer y limpiar líneas del archivo fuente
    lineas_raw    = args.código.readlines()
    lineas_limpias = [l.strip() for l in lineas_raw if l.strip()]

    # Construir bloques anidados (Si / ciclo)
    bloques = armarBloques(lineas_limpias)

    # Análisis léxico-semántico
    print("─" * 50)
    print("Analizando código fuente...")
    resultado = anlexsyn.lineas(bloques)

    if not resultado[0]:
        print(f"Error sintactico: {resultado[1]}")
        return

    print("Codigo valido")
    print("─" * 50)

    # Crear la VM y cargar el programa
    boome = BVM.BoomeVirtualMachine()
    boome.loadText(bloques)

    # Estado inicial
    print(boome)
    print("─" * 50)

    # R004: bucle de ejecución — sobrevive a cualquier instrucción
    while boome.Estado == "ready":
        boome.step()
        print(boome)
        print("─" * 50)

    print("Terminado :)")

if __name__ == "__main__":
    main()
