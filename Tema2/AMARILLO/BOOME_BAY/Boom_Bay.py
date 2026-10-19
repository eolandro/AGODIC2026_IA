import json
import random


def cargar_tablero():
    try:
        with open("tablero.json", "r", encoding="utf-8-sig") as archivo:
            datos = json.load(archivo)
    except (OSError, ValueError, UnicodeError):
        print("ERROR: no se pudo leer tablero.json.")
        return None
    if not isinstance(datos, dict):
        print("ERROR: la configuracion debe ser un objeto JSON.")
        return None
    campos = ["filas", "columnas", "bomba", "sensibilidad", "falso_positivo",
              "umbral", "desactivadores", "semilla"]
    for campo in campos:
        if campo not in datos:
            print("ERROR: falta", campo)
            return None
    for campo, minimo, maximo in [["filas", 5, 5], ["columnas", 10, 10],
                                  ["bomba", 1, 50], ["desactivadores", 0, 3]]:
        if type(datos[campo]) != int or not minimo <= datos[campo] <= maximo:
            print("ERROR:", campo, "debe ser entero entre", minimo, "y", maximo)
            return None
    for campo in ["sensibilidad", "falso_positivo", "umbral"]:
        if type(datos[campo]) not in [int, float] or not 0 <= datos[campo] <= 1:
            print("ERROR:", campo, "debe ser un numero entre 0 y 1.")
            return None
    if datos["semilla"] is not None and type(datos["semilla"]) != int:
        print("ERROR: semilla debe ser un entero o null.")
        return None
    return datos


def detector(casilla, bomba, sensibilidad, falso_positivo):
    probabilidad = falso_positivo
    if casilla == bomba:
        probabilidad = sensibilidad
    if random.random() < probabilidad:
        return 1
    return 0


def bayes(previa, sensibilidad, falso_positivo):
    con_bomba = sensibilidad * previa
    total = con_bomba + falso_positivo * (1 - previa)
    if total == 0:
        return None
    return con_bomba / total


def mostrar_tablero(posicion, revisadas, desactivada, explosion):
    for fila in range(5):
        texto = ""
        for columna in range(10):
            numero = fila * 10 + columna + 1
            simbolo = "?"
            if numero in revisadas:
                simbolo = "."
            if numero == posicion:
                simbolo = "R"
            if numero == desactivada:
                simbolo = "D"
            if numero == explosion:
                simbolo = "X"
            texto += str(numero).rjust(2) + simbolo + "  "
        print(texto.rstrip())
    print("Posicion de Boome:", posicion, "(0 = fuera del tablero)")
    print("Casillas revisadas:", revisadas)


def main():
    datos = cargar_tablero()
    if datos is None:
        return
    random.seed(datos["semilla"])
    recorrido = []
    for fila in range(5):
        inicio = fila * 10 + 1
        numeros = range(inicio, inicio + 10)
        if fila % 2 == 1:
            numeros = range(inicio + 9, inicio - 1, -1)
        for numero in numeros:
            recorrido.append(numero)
    restantes = datos["desactivadores"]
    revisadas = []
    posicion = 0
    desactivada = 0
    explosion = 0
    falsas_alarmas = 0
    estado = "recorrido terminado sin encontrar la bomba"
    print("Boom_Bay: ? pendiente, . revisada, R robot, D desactivada, X explosion")
    print("Revisada no garantiza seguridad. Los negativos adicionales conservan Bayes.")
    mostrar_tablero(posicion, revisadas, desactivada, explosion)
    for indice in range(50):
        casilla = recorrido[indice]
        probabilidad = 1 / (50 - indice)
        print("Evaluando casilla", casilla, "| Pendientes:", 50 - indice)
        for numero in range(1, 4):
            lectura = detector(casilla, datos["bomba"], datos["sensibilidad"], datos["falso_positivo"])
            print("Lectura", numero, ":", lectura, "| Previa:", format(probabilidad * 100, ".2f"), "%")
            if lectura == 1:
                probabilidad = bayes(probabilidad, datos["sensibilidad"], datos["falso_positivo"])
            if probabilidad is None:
                break
            print("Posterior (sin actualizar si negativa):", format(probabilidad * 100, ".2f"), "%")
            if numero == 1 and lectura == 0:
                break
        if probabilidad is None:
            estado = "error de calculo; simulacion detenida"
            print("ERROR: Bayes no definido; denominador cero.")
            break
        revisadas.append(casilla)
        if numero == 3:
            print("Comparacion:", format(probabilidad * 100, ".2f"), "% | Umbral:", format(datos["umbral"] * 100, ".2f"), "%")
            if probabilidad >= datos["umbral"]:
                if restantes > 0:
                    restantes -= 1
                    print("Usar un desactivador.")
                    if casilla == datos["bomba"]:
                        desactivada = casilla
                        estado = "victoria"
                    else:
                        falsas_alarmas += 1
                        print("Falsa alarma: desactivador consumido.")
                else:
                    print("No quedan desactivadores. Continuar.")
            else:
                print("Por debajo del umbral: no usar desactivador.")
        if desactivada == 0:
            posicion = casilla
            print("Boome avanza a la casilla", casilla)
            if casilla == datos["bomba"]:
                explosion = casilla
                estado = "explosion"
        print("Desactivadores restantes:", restantes)
        mostrar_tablero(posicion, revisadas, desactivada, explosion)
        if estado == "victoria" or estado == "explosion":
            break
    print("Resultado final:", estado)
    print("Falsas alarmas:", falsas_alarmas)
    print("Desactivadores restantes:", restantes)
    return [estado, restantes, falsas_alarmas, revisadas, posicion]


if __name__ == "__main__":
    main()
