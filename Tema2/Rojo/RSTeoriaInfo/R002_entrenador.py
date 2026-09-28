import json
import math
import sys
from pathlib import Path

ENTRADA = Path("animales.json")
SALIDA = Path("tabla_pesos.json")

CARACTERISTICAS = [
    ("granja", "Se encuentra en granja"),
    ("cola_larga", "Cola larga"),
    ("leal", "Leal"),
    ("vuela", "Vuela"),
    ("bigotes", "Bigotes"),
    ("dientes_grandes", "Dientes grandes"),
    ("salta", "Salta"),
    ("tranquilidad", "Tranquilidad"),
    ("pone_huevos", "Pone huevos"),
    ("galopa", "Galopa"),
    ("colmillos_largos", "Colmillos largos"),
    ("lenta", "Lenta"),
]

N = len(CARACTERISTICAS)
PESOS = {clave: 2 ** (N - 1 - i) for i, (clave, _) in enumerate(CARACTERISTICAS)}
CLAVES = set(PESOS)


def entropia(n):
    return math.log2(n) if n > 1 else 0.0


def ganancia(animales, clave):
    total = len(animales)
    si = sum(1 for a in animales if a["caracteristicas"][clave])
    no = total - si
    if si == 0 or no == 0:
        return 0.0
    return entropia(total) - si / total * entropia(si) - no / total * entropia(no)


def valor_agregado(animal):
    return sum(PESOS[c] for c, cumple in animal["caracteristicas"].items() if cumple)


def cargar_animales():
    if not ENTRADA.exists():
        sys.exit("No existe animales.json. Ejecuta primero R001_inicializador.py")
    try:
        animales = json.loads(ENTRADA.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"animales.json no es un JSON válido: {e}")
    if not isinstance(animales, list) or not animales:
        sys.exit("animales.json debe ser una lista con al menos un animal.")

    nombres = set()
    for a in animales:
        if not isinstance(a, dict) or not isinstance(a.get("animal"), str) or not a["animal"].strip():
            sys.exit("Hay un animal sin nombre válido.")
        nombre = a["animal"].strip().lower()
        if nombre in nombres:
            sys.exit(f"El animal '{nombre}' está repetido.")
        nombres.add(nombre)
        caracteristicas = a.get("caracteristicas")
        if not isinstance(caracteristicas, dict) or set(caracteristicas) != CLAVES:
            sys.exit(f"'{nombre}' no tiene exactamente las {N} características esperadas.")
        if not all(isinstance(v, bool) for v in caracteristicas.values()):
            sys.exit(f"'{nombre}' tiene valores que no son true/false.")
    return animales


def main():
    animales = cargar_animales()

    tabla_animales = [
        {
            "animal": a["animal"],
            "valor_agregado": valor_agregado(a),
            "caracteristicas": a["caracteristicas"],
        }
        for a in animales
    ]
    tabla_preguntas = [
        {
            "clave": clave,
            "pregunta": texto,
            "peso": PESOS[clave],
            "ganancia_informacion": ganancia(animales, clave),
        }
        for clave, texto in CARACTERISTICAS
    ]

    salida = {"preguntas": tabla_preguntas, "animales": tabla_animales}
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{'Característica':26}{'Peso':>7}{'Ganancia':>11}")
    for p in tabla_preguntas:
        print(f"{p['pregunta']:26}{p['peso']:>7}{p['ganancia_informacion']:>11.4f}")

    print(f"\n{'Animal':16}{'Valor':>7}")
    for a in tabla_animales:
        print(f"{a['animal']:16}{a['valor_agregado']:>7}")

    grupos = {}
    for a in tabla_animales:
        grupos.setdefault(a["valor_agregado"], []).append(a["animal"])
    for valor, nombres in grupos.items():
        if len(nombres) > 1:
            print(f"\nAviso: {', '.join(nombres)} tienen el mismo valor ({valor}) y R003 no podrá distinguirlos.")

    print(f"\nArchivo generado: {SALIDA}")
    print("Siguiente paso: python3 R003_adivinador.py")


if __name__ == "__main__":
    main()