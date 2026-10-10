"""Menú principal: ejecuta las cuatro etapas del clasificador (R006-R009)."""
import os

import clasificador
import detokenizador
import entrenador
import metricas
from common import cargar, guardar

CONOCIMIENTO = "conocimiento.json"
TABLA = "tabla_probabilidades.json"
CLASIFICADOS = "clasificados.json"
METRICAS = "metricas.json"
COMPARACION = "comparacion_metodos.json"


def _necesita(archivo, paso):
    if not os.path.exists(archivo):
        print(f"Falta '{archivo}'. Primero ejecuta el paso {paso}.")
        return True
    return False


def paso_entrenar():
    entrenador.main(None, CONOCIMIENTO)


def paso_tabla():
    if not _necesita(CONOCIMIENTO, 1):
        detokenizador.main(CONOCIMIENTO, TABLA)


def paso_clasificar():
    if _necesita(TABLA, 2):
        return
    m = input(f"Método ({'/'.join(clasificador.METODOS)}) [democracia]: ").strip().lower() or "democracia"
    if m not in clasificador.METODOS:
        print("Método no válido.")
        return
    clasificador.main(None, TABLA, CLASIFICADOS, m)


def paso_metricas():
    if not _necesita(CLASIFICADOS, 3):
        metricas.main(CLASIFICADOS, METRICAS)


def paso_comparar():
    """Corre todos los métodos de consenso y los compara con el supervisor."""
    if _necesita(METRICAS, 4) or _necesita(TABLA, 2):
        return
    guardado = cargar(METRICAS)["mensajes"]
    mensajes = [d["mensaje"] for d in guardado]
    reales = [d["etiqueta_supervisor"] for d in guardado]
    tabla = cargar(TABLA)

    print(f"\n{'Método':<12}{'VP':>4}{'FP':>4}{'FN':>4}{'VN':>4}{'Acc':>7}{'Prec':>7}"
          f"{'Rec':>7}{'F1':>7}{'Bias':>7}")
    fmt = lambda v: "N/A" if v is None else f"{v:.2f}"
    resultado, etiquetas = {}, {}
    for met in clasificador.METODOS:
        pred = [r["etiqueta"] for r in clasificador.clasificar_todos(mensajes, tabla, met)]
        x = metricas.calcular(pred, reales)
        c = x["matriz_confusion"]
        print(f"{met:<12}{c['VP']:>4}{c['FP']:>4}{c['FN']:>4}{c['VN']:>4}"
              f"{fmt(x['accuracy']):>7}{fmt(x['precision']):>7}{fmt(x['recall']):>7}"
              f"{fmt(x['f1']):>7}{fmt(x['bias']):>7}")
        resultado[met] = x
        etiquetas[met] = pred

    desacuerdos = [
        {"mensaje": m, "supervisor": reales[i], **{k: etiquetas[k][i] for k in etiquetas}}
        for i, m in enumerate(mensajes)
        if len({reales[i], *(etiquetas[k][i] for k in etiquetas)}) > 1
    ]
    if desacuerdos:
        print("\nMensajes con error o desacuerdo:")
        for d in desacuerdos:
            print(f" - {d['mensaje']}  (supervisor: {d['supervisor']}, "
                  + ", ".join(f"{k}: {d[k]}" for k in clasificador.METODOS) + ")")
    guardar(COMPARACION, {"metodos": resultado, "mensajes_con_desacuerdo": desacuerdos})


def main():
    acciones = {"1": paso_entrenar, "2": paso_tabla, "3": paso_clasificar,
                "4": paso_metricas, "5": paso_comparar}
    while True:
        print("\n1) Entrenador: etiquetar mensajes (supervisor)")
        print("2) DeTokenizador: tabla de probabilidades")
        print("3) Clasificador: etiquetar mensajes nuevos")
        print("4) Métricas: comparar con el supervisor")
        print("5) Comparar los métodos de consenso")
        print("6) Salir")
        op = input("Elige una opción: ").strip()
        if op == "6":
            break
        acciones.get(op, lambda: print("Opción no válida."))()


if __name__ == "__main__":
    main()
