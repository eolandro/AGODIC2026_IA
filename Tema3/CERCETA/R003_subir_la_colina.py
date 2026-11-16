"""R003: buscar un valor alto avanzando siempre hacia un vecino mejor."""


def altura(x):
    return -(x - 7) ** 2 + 49


def subir_la_colina(inicio):
    actual = inicio
    camino = [actual]

    while True:
        mejor = actual
        for vecino in (actual - 1, actual + 1):
            if 0 <= vecino <= 14 and altura(vecino) > altura(mejor):
                mejor = vecino

        if mejor == actual:
            return camino

        actual = mejor
        camino.append(actual)


def main():
    print("SUBIR LA COLINA")
    print("Funcion: f(x) = -(x - 7)^2 + 49, con x entre 0 y 14")
    camino = subir_la_colina(0)
    for x in camino:
        print(f"x = {x:2}, altura = {altura(x)}")
    print("Se detiene porque ningun vecino tiene mayor altura.")


if __name__ == "__main__":
    main()
