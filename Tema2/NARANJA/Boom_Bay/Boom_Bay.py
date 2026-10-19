import os
import random
# =====================================================================
#  DATOS DEL PROBLEMA  
# =====================================================================
DESACTIVADORES = 6
# Detector / sensor
P_D_BOOM = 0.90     # P(D+|Boom)  : con bomba, positivo 9 de 10
P_D_VACIO = 0.20    # P(D+|-Boom) : sin bomba, positivo 2 de 10 (falso positivo)

# Reglas de decision
PRUEBAS_POR_CASILLA = 3     # un positivo dispara hasta 3 pruebas en la casilla
FALSAS_PARA_DESCARTAR = 2   # 2 lecturas falsas (D-) -> "no hay bomba"
UMBRAL = 0.51               # con P(Boom|D+) >= UMBRAL se usa un desactivador
SEMILLA = 7                 # para que la simulacion sea repetible

ARCHIVO_TABLERO = "tablero.txt"
ANCHO = 74                  

def leer_tablero(ruta):
    """Lee el tablero desde un archivo de texto.

    Una fila por linea, valores separados por espacios:
        0 = casilla vacia
        1 = bomba
    """
    mapa = []
    with open(ruta) as archivo:
        for linea in archivo:
            fila = []
            for e in linea.split():
                match e:
                    case "0" | "1":
                        fila.append(int(e))
                    case _:
                        raise ValueError(f"Simbolo invalido '{e}' en la fila {len(mapa) + 1}")
            if fila:
                mapa.append(fila)

    if not mapa:
        raise ValueError("El tablero esta vacio")
    if any(len(fila) != len(mapa[0]) for fila in mapa):
        raise ValueError("Todas las filas deben tener el mismo numero de columnas")
    if not any(1 in fila for fila in mapa):
        raise ValueError("El tablero no tiene ninguna bomba (1)")
    return mapa

def mostrar_tablero(mapa):
    """Dibuja el tablero con marco. B = bomba, . = vacia.
    (Solo la simulacion conoce las bombas; Boome no.)"""
    columnas = len(mapa[0])
    borde = "     +" + "-" * (columnas * 2 + 1) + "+"

    print("       " + " ".join(chr(65 + j) for j in range(columnas)))
    print(borde)
    for i, fila in enumerate(mapa):
        celdas = " ".join("B" if e == 1 else "." for e in fila)
        print(f"  {i + 1:2d} | {celdas} |")
    print(borde)

def nombre(pos):
    """(fila, columna) -> 'A1'   (letra = columna, numero = fila)"""
    i, j = pos
    return f"{chr(65 + j)}{i + 1}"

def recorrido(filas, columnas):
    """Boome recorre en zigzag:
    fila 1 de izquierda a derecha, fila 2 de derecha a izquierda, etc."""
    camino = []
    for i in range(filas):
        if i % 2 == 0:
            columnas_fila = range(columnas)
        else:
            columnas_fila = range(columnas - 1, -1, -1)
        for j in columnas_fila:
            camino.append((i, j))
    return camino


def bayes(creencia):
    """
                         P(D+|Boom) * P(Boom)
    P(Boom|D+) = -----------------------------------------
                 P(D+|Boom) * P(Boom) + P(-Boom) * P(D+|-Boom)
    """
    rama_bomba = P_D_BOOM * creencia
    rama_vacia = (1 - creencia) * P_D_VACIO
    return rama_bomba / (rama_bomba + rama_vacia)

def texto_formula(creencia, resultado):
    """La formula del pizarron con los numeros sustituidos."""
    return (f"({P_D_BOOM}*{creencia:.4f}) / "
            f"(({P_D_BOOM}*{creencia:.4f}) + ({1 - creencia:.4f}*{P_D_VACIO})) "
            f"= {resultado:.4f}")

def detector(mapa, pos, azar):
    """Revisa una casilla ANTES de moverse a ella.
    Regresa 1 = D+ (dice que hay bomba)  |  0 = D- (dice que no hay)."""
    i, j = pos
    p_positivo = P_D_BOOM if mapa[i][j] == 1 else P_D_VACIO
    return 1 if azar.random() < p_positivo else 0

def revisar_casilla(mapa, pos, creencia, azar, log):
    """La primera lectura ya salio D+. Hace las pruebas que faltan y
    regresa (probabilidad final, numero de lecturas falsas)."""
    casilla = nombre(pos)
    posterior = bayes(creencia)
    falsas = 0

    log(f"\n  Casilla {casilla}  (el detector marco positivo)")
    log(f"    Prueba 1/{PRUEBAS_POR_CASILLA}: D+   creencia = {creencia:.4f}")
    log(f"       P(Boom|D+) = {texto_formula(creencia, posterior)}")

    for prueba in range(2, PRUEBAS_POR_CASILLA + 1):
        if detector(mapa, pos, azar) == 1:
            anterior = posterior
            posterior = bayes(anterior)
            log(f"    Prueba {prueba}/{PRUEBAS_POR_CASILLA}: D+   creencia = {anterior:.4f}")
            log(f"       P(Boom|D+) = {texto_formula(anterior, posterior)}")
        else:
            falsas += 1
            log(f"    Prueba {prueba}/{PRUEBAS_POR_CASILLA}: D-   lectura falsa #{falsas}, "
                f"la probabilidad no cambia")
            if falsas >= FALSAS_PARA_DESCARTAR:
                break

    return posterior, falsas


def simular(mapa, azar, imprimir=True):
    log = print if imprimir else (lambda *a, **k: None)

    mapa = [fila[:] for fila in mapa]            
    filas, columnas = len(mapa), len(mapa[0])
    total = filas * columnas
    bombas_restantes = sum(fila.count(1) for fila in mapa)
    desactivadores = DESACTIVADORES
    desarmadas = 0
    falsas_alarmas = 0
    revisadas = 0
    resultado = "recorrido completo"

    log("\n" + "=" * ANCHO)
    log("RECORRIDO DE BOOME".center(ANCHO))
    log("=" * ANCHO)

    for pos in recorrido(filas, columnas):
        if bombas_restantes == 0:
            resultado = "todas las bombas desactivadas"
            break
        if desactivadores == 0:
            resultado = "sin desactivadores"
            break

        casilla = nombre(pos)

        if detector(mapa, pos, azar) == 1:
            creencia = bombas_restantes / (total - revisadas)
            posterior, falsas = revisar_casilla(mapa, pos, creencia, azar, log)

            if falsas >= FALSAS_PARA_DESCARTAR:
                log(f"    Decision: {falsas} lecturas falsas -> no hay bomba")

            elif posterior >= UMBRAL:
                desactivadores -= 1
                if mapa[pos[0]][pos[1]] == 1:
                    mapa[pos[0]][pos[1]] = 0
                    bombas_restantes -= 1
                    desarmadas += 1
                    que_paso = "bomba desarmada"
                else:
                    falsas_alarmas += 1
                    que_paso = "no habia bomba"
                log(f"    Decision: {posterior:.1%} >= {UMBRAL:.0%} -> se usa un DESACTIVADOR")
                log(f"              {que_paso} (quedan {desactivadores})")

            else:
                log(f"    Decision: {posterior:.1%} < {UMBRAL:.0%} -> no se usa el desactivador")

        if mapa[pos[0]][pos[1]] == 1:
            log(f"\n  *** BOOM: Boome piso una bomba en {casilla} ***")
            resultado = "boom"
            break
        revisadas += 1

    if resultado == "recorrido completo" and bombas_restantes == 0:
        resultado = "todas las bombas desactivadas"


    log("\n" + "=" * ANCHO)
    log("RESULTADO".center(ANCHO))
    log("=" * ANCHO)
    log(f"  Resultado final          : {resultado.upper()}")
    log(f"  Casillas recorridas      : {revisadas} / {total}")
    log(f"  Bombas desarmadas        : {desarmadas}")
    log(f"  Falsas alarmas           : {falsas_alarmas}")
    log(f"  Desactivadores restantes : {desactivadores}")
    log(f"  Bombas sin desactivar    : {bombas_restantes}")
    log("=" * ANCHO)
    return resultado

def main():
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(carpeta, ARCHIVO_TABLERO)
    semilla = SEMILLA

    if not os.path.exists(ruta):
        print(f"No se encontro '{ARCHIVO_TABLERO}'.")
        print(f"Ponlo en la misma carpeta que Boom_Bay.py:\n  {carpeta}")
        return
    mapa = leer_tablero(ruta)

    filas, columnas = len(mapa), len(mapa[0])
    bombas = sum(fila.count(1) for fila in mapa)

    print("=" * ANCHO)
    print("BOOME  -  DETECTOR DE BOMBAS CON TEOREMA DE BAYES".center(ANCHO))
    print("=" * ANCHO)
    print(f"  Tablero          : {filas} x {columnas}  ({filas * columnas} casillas)")
    print(f"  Bombas           : {bombas}")
    print(f"  Desactivadores   : {DESACTIVADORES}")
    print(f"  Semilla          : {semilla}")
    print("-" * ANCHO)
    print(f"  P(D+|Boom)       : {P_D_BOOM}   (con bomba, positivo)")
    print(f"  P(D+|-Boom)      : {P_D_VACIO}   (sin bomba, falso positivo)")
    print(f"  Umbral           : {UMBRAL:.0%}")
    print(f"  Pruebas/casilla  : {PRUEBAS_POR_CASILLA}  "
          f"(se descarta con {FALSAS_PARA_DESCARTAR} lecturas falsas)")
    print("-" * ANCHO)
    print("  TABLERO   (B = bomba, . = vacia)\n")
    mostrar_tablero(mapa)

    simular(mapa, random.Random(semilla))


if __name__ == "__main__":
    main()
