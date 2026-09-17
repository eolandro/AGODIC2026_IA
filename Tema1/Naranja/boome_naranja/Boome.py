import argparse
import anlexsyn
import BVM

parser = argparse.ArgumentParser()
parser.add_argument(
    "codigo",
    nargs="?",                 
    type=argparse.FileType('r'),
    default=None,
)

MAX_PASOS = 200000  


def ejecutar_archivo(archivo):
    LineasCodigo = archivo.readlines()
    LineasCodigo = [
        linea.strip() for linea in LineasCodigo
    ]
    LineasCodigo = [
        linea for linea in LineasCodigo if linea
    ]  

    resultado = anlexsyn.programa(LineasCodigo)
    if not resultado[0]:
        print("Error en el código fuente:")
        for numero, texto, mensaje in resultado[1]:
            print(f"  Línea {numero}: '{texto}' -> {mensaje}")
        return

    BooMe = BVM.BoomeVirtualMachine()
    BooMe.loadText(LineasCodigo)
    print(BooMe)

    pasos = 0
    while BooMe.Estado == "\nready" and pasos < MAX_PASOS:
        BooMe.step()
        print(BooMe)
        pasos += 1

    if pasos >= MAX_PASOS:
        print("Se alcanzó el límite de pasos (posible ciclo infinito: revisa que")
        print("el registro del 'ciclo' sí llegue a #0000 dentro del cuerpo).")

    print("Terminado")


def _tokenizar(texto):
    return [t for t in texto.split(" ") if t]


def _capturar_bloque(texto_apertura, tokens_apertura):
    apertura = tokens_apertura[0]
    cierre = "FinSi" if apertura == "Si" else "finciclo"

    if len(tokens_apertura) != 2:
        print(f"  Error: '{apertura}' debe ir seguido de un solo registro")
        return None
    RG = anlexsyn.regs(tokens_apertura[1])
    if not RG[0]:
        print(f"  Error: {RG[1]}")
        return None

    lineas_bloque = [texto_apertura]
    print(f"  (capturando el cuerpo del bloque; escribe '{cierre}' para cerrarlo)")
    while True:
        try:
            linea_texto = input(f"  {apertura}...> ").strip()
        except EOFError:
            print(f"\n  Error: '{apertura}' no se cerró con '{cierre}'")
            return None
        if not linea_texto:
            continue
        tokens_linea = _tokenizar(linea_texto)
        if tokens_linea == [cierre]:
            lineas_bloque.append(linea_texto)
            return lineas_bloque
        if tokens_linea[:1] in (["Si"], ["ciclo"]):
            print("  Error: no se permiten bloques anidados dentro de otro bloque")
            return None
        R = anlexsyn.linea(tokens_linea)
        if not R[0]:
            print(f"  Error: {R[1]}")
            return None
        lineas_bloque.append(linea_texto)


def _ejecutar_hasta_agotar(BooMe):
    pasos = 0
    while BooMe.Estado == "\nready" and BooMe.RIP < len(BooMe.Instrucciones) and pasos < MAX_PASOS:
        BooMe.step()
        print(BooMe)
        pasos += 1
    if pasos >= MAX_PASOS:
        print("Se alcanzó el límite de pasos (posible ciclo infinito).")


def ejecutar_interactivo():
    BooMe = BVM.BoomeVirtualMachine()
    BooMe.iniciarInteractivo()

    print("Modo interactivo de Boome. Escribe una instrucción por línea.")
    print("Para un bloque, escribe 'Si R1' o 'ciclo R3' y sigue con las")
    print("líneas del cuerpo hasta cerrarlo con 'FinSi' / 'finciclo'.")
    print("('salir' o Ctrl+D para terminar).\n")
    print(BooMe)

    while BooMe.Estado == "\nready":
        try:
            texto = input("boome> ").strip()
        except EOFError:
            print()
            break

        if not texto:
            continue
        if texto.lower() in ("salir", "exit", "quit"):
            break

        tokens = _tokenizar(texto)

        if tokens[:1] in (["Si"], ["ciclo"]):
            bloque = _capturar_bloque(texto, tokens)
            if bloque is None:
                continue
            for linea_bloque in bloque:
                BooMe.agregarInstruccion(linea_bloque)
            _ejecutar_hasta_agotar(BooMe)
            continue

        if tokens in (["FinSi"], ["finciclo"]):
            print(f"  Error: '{texto}' no tiene una apertura correspondiente")
            continue

        resultado = anlexsyn.linea(tokens)
        if not resultado[0]:
            print(f"  Error: {resultado[1]}")
            continue

        BooMe.agregarInstruccion(texto)
        BooMe.step()
        print(BooMe)

    print("Terminado")


def main():
    args = parser.parse_args()

    if args.codigo is None:
        ejecutar_interactivo()
    else:
        ejecutar_archivo(args.codigo)


if __name__ == "__main__":
    main()
