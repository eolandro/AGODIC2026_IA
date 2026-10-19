import random
import json 

UMBRAL = 0.3

def load_map(name_file):
    casillas = []
    with open(name_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                partes = line.split()
                for parte in partes:
                    casillas.append(int(parte))
    return casillas

def sensor(es_bomba):
    azar = random.random()
    if es_bomba == 1:
        if azar < 0.9:
            return 1
        else:
            return 0
    else:
        if azar < 0.8:
            return 0
        else:
            return 1

def calculo_bayes(prob_prior):
    prob_bomba = 0.9
    prob_vacio = 0.2

    if prob_prior <= 0:
        return 0.0

    prob_positivo = (prob_bomba * prob_prior) + prob_vacio * (1 - prob_prior)
    p_posterior = (prob_bomba * prob_prior) / prob_positivo
    return p_posterior

def revisar(es_bomba, prob_prior, desactivadores, bombas_restantes):
    lecturas = []

    l1 = sensor(es_bomba)
    lecturas.append(l1)
    
    if l1 == 1:
        prob_prior = calculo_bayes(prob_prior)
        print(f"Detector L1 POSITIVO (1) -> Bayes actualizado: {prob_prior} | Bombas restantes: {bombas_restantes}/2 | Desactivadores: {desactivadores}")

    l2 = sensor(es_bomba)
    lecturas.append(l2)
    
    if l2 == 1:
        prob_prior = calculo_bayes(prob_prior)
        print(f"Detector L2 POSITIVO (1) -> Bayes actualizado: {prob_prior} | Bombas restantes: {bombas_restantes}/2 | Desactivadores: {desactivadores}")
   
    if l1 == 0 and l2 == 0:
        return False, lecturas, prob_prior

    l3 = sensor(es_bomba)
    lecturas.append(l3)
    
    if l3 == 1:
        prob_prior = calculo_bayes(prob_prior)
        print(f"Detector L3 POSITIVO (1) -> Bayes actualizado: {prob_prior} | Bombas restantes: {bombas_restantes}/2 | Desactivadores: {desactivadores}")

    positivo = prob_prior >= UMBRAL
    return positivo, lecturas, prob_prior

def imprimir_tablero(mapa):
    
    print("\n================ TABLERO ================")
    for i in range(len(mapa)):
        print(mapa[i], end=" ")
        if (i + 1) % 10 == 0:
            print()
    print("=========================================================\n")

def main():
   
    random.seed(42)
    mapa = load_map("tablero.txt")

    desactivadores = 6
    bombas_restantes = 2
    boome_vivo = True

    print("*****************    INICIANDO SIMULACION BOOM_BAY ********************\n")
    
    for i in range(len(mapa)):
        es_bomba = mapa[i]

        prob_prior_casilla = 2 / 50 
        
        positivo, lecturas, prob_casilla = revisar(es_bomba, prob_prior_casilla, desactivadores, bombas_restantes)
        
        bomba_desactivada = False

        if positivo:
            if desactivadores > 0:
                desactivadores -= 1
                if es_bomba == 1:
                    bombas_restantes -= 1
                    bomba_desactivada = True
                    print(f"Casilla {i}: ALERTA {lecturas} - ¡Bomba ENCONTRADA y DESACTIVADA!")
                else:
                    print(f"Casilla {i}: ALERTA {lecturas} - FALSO POSITIVO (Sin bomba)")
                
                print(f"   -> Resumen casilla -> Desactivadores restantes: {desactivadores} | Bombas faltantes: {bombas_restantes}/2\n")
            else:
                print(f"Casilla {i}: ALERTA {lecturas} - ¡SIN DESACTIVADORES DISPONIBLES! | Bayes: {prob_casilla}\n")
        else:
            print(f"Casilla {i}: Segura (Sin alerta) {lecturas}\n")
        if es_bomba == 1 and not bomba_desactivada:
            print(f"¡BOOM! Boome pisó una bomba no desactivada en la casilla {i}. BOOME MURIO.\n")
            boome_vivo = False
            break

    print("=== FIN DE LA SIMULACIÓN ===")
    if boome_vivo:
        print("¡Boome logró completar todo el mapa con éxito!")
    else:
        print("La simulación finalizó prematuramente por la destrucción de Boome.")

    print(f"Total de bombas restantes sin desactivar: {bombas_restantes}")
    print(f"Desactivadores sobrantes: {desactivadores}")
    imprimir_tablero(mapa)

if __name__ == "__main__":
    main()