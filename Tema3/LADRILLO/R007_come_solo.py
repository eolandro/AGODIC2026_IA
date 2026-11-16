

MOVIMIENTOS_POSIBLES = [
    # Horizontales
    (4, 5, 6), (6, 5, 4),
    (7, 8, 9), (9, 8, 7), (8, 9, 10), (10, 9, 8),
    (11, 12, 13), (13, 12, 11), (12, 13, 14), (14, 13, 12), (13, 14, 15), (15, 14, 13),
    
    # Diagonales
    (1, 2, 4), (4, 2, 1), (1, 3, 6), (6, 3, 1),
    (2, 4, 7), (7, 4, 2), (2, 5, 9), (9, 5, 2), (3, 5, 8), (8, 5, 3), (3, 6, 10), (10, 6, 3),
    (4, 7, 11), (11, 7, 4), (4, 8, 13), (13, 8, 4),
    (5, 8, 12), (12, 8, 5), (5, 9, 14), (14, 9, 5),
    (6, 9, 13), (13, 9, 6), (6, 10, 15), (15, 10, 6)
]

def imprimir_tablero(tab):
    """
    Imprime la lista 'tab' directamente.
    """
    print(f"        ({tab[1]})                 (1)")
    print(f"      ({tab[2]}) ({tab[3]})             (2) (3)")
    print(f"    ({tab[4]}) ({tab[5]}) ({tab[6]})         (4) (5) (6)")
    print(f"  ({tab[7]}) ({tab[8]}) ({tab[9]}) ({tab[10]})     (7) (8) (9) (10)")
    print(f"({tab[11]}) ({tab[12]}) ({tab[13]}) ({tab[14]}) ({tab[15]}) (11)(12)(13)(14)(15)\n")

def resolver_comesolo(tab, historial_movimientos):
    piezas_restantes = tab.count("O")
    
    if piezas_restantes == 1:
        return True

    for origen, saltada, destino in MOVIMIENTOS_POSIBLES:
        if tab[origen] == "O" and tab[saltada] == "O" and tab[destino] == ".":
            
            tab[origen] = "."
            tab[saltada] = "."
            tab[destino] = "O"
            historial_movimientos.append((origen, saltada, destino))

            if resolver_comesolo(tab, historial_movimientos):
                return True

            # --- DESHACER EL MOVIMIENTO (BACKTRACKING) ---
            # Si el camino no tuvo éxito, regresamos las fichas a su estado anterior
            tab[origen] = "O"
            tab[saltada] = "O"
            tab[destino] = "."
            historial_movimientos.pop()

    return False

def main():
    print("==== COME SOLO  ====")
    print("Mapa de posiciones:")
    print("        (1)")
    print("      (2) (3)")
    print("    (4) (5) (6)")
    print("  (7) (8) (9) (10)")
    print("(11)(12)(13)(14)(15)\n")

    while True:
        try:
            vacia = int(input("Ingresa el número de la casilla que empezará VACÍA (1-15): "))
            if 1 <= vacia <= 15:
                break
            print("Por favor, ingresa un número entre 1 y 15.")
        except ValueError:
            print("Entrada no válida. Ingresa un número entero.")

    tab = ["", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]
    tab[vacia] = "."  # Ponemos la casilla elegida como vacía

    historial = []

    print("\nCalculando solución...")
    exito = resolver_comesolo(tab, historial)

    if exito:
        print(f"\n¡SOLUCIÓN ENCONTRADA EN {len(historial)} PASOS!\n")
        
        simulacion = ["", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]
        simulacion[vacia] = "."

        print("ESTADO INICIAL:")
        imprimir_tablero(simulacion)

        for i, (orig, salt, dest) in enumerate(historial, 1):
            print(f"--- PASO {i}: Mover {orig} -> {dest} (comiendo la pieza {salt}) ---")
            simulacion[orig] = "."
            simulacion[salt] = "."
            simulacion[dest] = "O"
            imprimir_tablero(simulacion)

        # Encontrar la casilla donde quedó la última ficha
        pos_final = simulacion.index("O", 1)
        print(f"¡Juego completado! La última pieza quedó en la casilla ({pos_final}).")
    else:
        print("No se encontró solución para esta casilla inicial.")

if __name__ == "__main__":
    main()  