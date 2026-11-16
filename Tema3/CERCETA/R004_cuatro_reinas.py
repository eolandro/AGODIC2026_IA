"""R004: colocar cuatro reinas sin que se ataquen."""


def es_seguro(reinas, fila, columna):
    for otra_fila, otra_columna in enumerate(reinas):
        if columna == otra_columna:
            return False
        if abs(fila - otra_fila) == abs(columna - otra_columna):
            return False
    return True


def resolver(reinas):
    if len(reinas) == 4:
        return reinas

    fila = len(reinas)
    for columna in range(4):
        if es_seguro(reinas, fila, columna):
            # Si esta opcion no funciona, se prueba otra columna.
            solucion = resolver(reinas + [columna])
            if solucion is not None:
                return solucion
    return None


def main():
    print("CUATRO REINAS")
    solucion = resolver([])
    if solucion is None:
        print("No se encontro una solucion.")
        return
    for columna_reina in solucion:
        print(" ".join("R" if c == columna_reina else "." for c in range(4)))
    print("R = reina. No comparten fila, columna ni diagonal.")


if __name__ == "__main__":
    main()
