from entrenador import ejecutar_entrenador
from detoquenizador import ejecutar_detokenizador
from Clasificador import ejecutar_clasificador
from metricas import ejecutar_metricas

def main():
    print("\n==================================================")
    print("   SISTEMA MODULAR DE CLASIFICACIÓN DE SPAM   ")
    print("==================================================")


    ejecutar_entrenador()
    ejecutar_detokenizador()
    ejecutar_clasificador()
    ejecutar_metricas()
    print("\n==================================================")
    print("   PROCESO COMPLETO FINALIZADO CON ÉXITO XD      ")
    print("==================================================")

if __name__ == "__main__":
    main()