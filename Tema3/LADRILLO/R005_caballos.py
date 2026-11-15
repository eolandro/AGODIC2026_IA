
def crear_tablero_inicial():
    """Crea la matriz 3x3 idéntica al Excel del profesor."""
    return [
        ['CB1', '.',  'CB2'],
        ['.',   '.',  '.'],
        ['CN1', '.',  'CN2']
    ]

def imprimir_tablero(tablero):
    """Imprime el tablero visualmente."""
    print("+-----+-----+-----+")
    for fila in tablero:
        linea = "|"
        for casilla in fila:
            linea += f" {casilla:3s} |"
        print(linea)
        print("+-----+-----+-----+")
    print()

CAMINO_HORARIO = [
    (0, 0), (1, 2), (2, 0), (0, 1),
    (2, 2), (1, 0), (0, 2), (2, 1) ]

def ejecutar_juego():
    print("==========================================")
    print("      PROBLEMA DE LOS 4 CABALLOS (3x3)    ")
    print("==========================================\n")
    
    print("Selecciona el sentido de rotación de los caballos:")
    print("1. Sentido Horario")
    print("2. Sentido Antihorario")
    
    opcion = input("Ingresa tu opción (1 o 2): ").strip()
    while opcion not in ['1', '2']:
        opcion = input("Opción inválida. Ingresa 1 o 2: ").strip()
        
    es_horario = (opcion == '1')
    direccion_texto = "HORARIO" if es_horario else "ANTIHORARIO"
    
    tablero = crear_tablero_inicial()
    
    print("\n--- ESTADO INICIAL ---")
    imprimir_tablero(tablero)
    
    # Definir la dirección del ciclo
    if es_horario:
        camino = CAMINO_HORARIO
    else:
        camino = [CAMINO_HORARIO[0]] + list(reversed(CAMINO_HORARIO[1:]))

    # Seguimiento individual de las posiciones de cada caballo
    pos_actuales = {
        'CB1': (0, 0),
        'CB2': (0, 2),
        'CN1': (2, 0),
        'CN2': (2, 2)
    }
    print(f"Iniciando resolución en sentido {direccion_texto}...\n")
    
    pasos_totales = 16

    for i in range(pasos_totales):
        for pieza, pos in list(pos_actuales.items()):
            idx = camino.index(pos)
            siguiente_pos = camino[(idx + 1) % len(camino)]
            
            # Si el destino está libre ('.'), se efectúa el salto
            if tablero[siguiente_pos[0]][siguiente_pos[1]] == '.':
                f_orig, c_orig = pos
                f_dest, c_dest = siguiente_pos
                
                tipo_pieza = tablero[f_orig][c_orig]
                tablero[f_orig][c_orig] = '.'
                tablero[f_dest][c_dest] = tipo_pieza
                
                pos_actuales[pieza] = siguiente_pos
                
                del pos_actuales[pieza]
                pos_actuales[pieza] = siguiente_pos
                
                print(f"Paso {i+1}: Se mueve {tipo_pieza} de {pos} a {siguiente_pos} ({direccion_texto})")
                imprimir_tablero(tablero)
                break

    print("¡finalizado! Los caballos han intercambiado posiciones exitosamente.")

if __name__ == "__main__":
    ejecutar_juego()




