import json
from pathlib import Path

ARCHIVO_DATOS = Path("datos_animales.json")

CARACTERISTICAS = [
    ("granja", "Se encuentra en granja", 2048),
    ("cola_larga", "Tiene cola larga", 1024),
    ("leal", "Es leal", 512),
    ("vuela", "Vuela", 256),
    ("bigotes", "Tiene bigotes", 128),
    ("dientes_grandes", "Tiene dientes grandes", 64),
    ("salta", "Salta", 32),
    ("tranquilidad", "Es tranquilo", 16),
    ("pone_huevos", "Pone huevos", 8),
    ("galopa", "Galopa", 4),
    ("colmillos_largos", "Tiene colmillos largos", 2),
    ("lenta", "Es lenta", 1),
]

ANIMALES = {
    "perro": {
        "granja": True,
        "cola_larga": True,
        "leal": True,
        "vuela": False,
        "bigotes": True,
        "dientes_grandes": False,
        "salta": True,
        "tranquilidad": False,
        "pone_huevos": False,
        "galopa": False,
        "colmillos_largos": True,
        "lenta": False,
    },
    "mariposa": {
        "granja": True,
        "cola_larga": False,
        "leal": False,
        "vuela": True,
        "bigotes": False,
        "dientes_grandes": False,
        "salta": False,
        "tranquilidad": True,
        "pone_huevos": True,
        "galopa": False,
        "colmillos_largos": False,
        "lenta": False,
    },
    "gato": {
        "granja": True,
        "cola_larga": True,
        "leal": False,
        "vuela": False,
        "bigotes": True,
        "dientes_grandes": False,
        "salta": True,
        "tranquilidad": True,
        "pone_huevos": False,
        "galopa": False,
        "colmillos_largos": False,
        "lenta": False,
    },
    "tuza": {
        "granja": False,
        "cola_larga": True,
        "leal": False,
        "vuela": False,
        "bigotes": True,
        "dientes_grandes": True,
        "salta": True,
        "tranquilidad": True,
        "pone_huevos": False,
        "galopa": False,
        "colmillos_largos": False,
        "lenta": False,
    },
    "conejo": {
        "granja": True,
        "cola_larga": False,
        "leal": False,
        "vuela": False,
        "bigotes": True,
        "dientes_grandes": True,
        "salta": True,
        "tranquilidad": True,
        "pone_huevos": False,
        "galopa": False,
        "colmillos_largos": False,
        "lenta": False,
    },
    "capibara": {
        "granja": False,
        "cola_larga": False,
        "leal": False,
        "vuela": False,
        "bigotes": True,
        "dientes_grandes": True,
        "salta": True,
        "tranquilidad": True,
        "pone_huevos": False,
        "galopa": False,
        "colmillos_largos": False,
        "lenta": False,
    },
    "ornitorrinco": {
        "granja": False,
        "cola_larga": True,
        "leal": False,
        "vuela": False,
        "bigotes": False,
        "dientes_grandes": False,
        "salta": False,
        "tranquilidad": True,
        "pone_huevos": True,
        "galopa": False,
        "colmillos_largos": False,
        "lenta": False,
    },
    "caballo": {
        "granja": True,
        "cola_larga": True,
        "leal": True,
        "vuela": False,
        "bigotes": True,
        "dientes_grandes": True,
        "salta": True,
        "tranquilidad": False,
        "pone_huevos": False,
        "galopa": True,
        "colmillos_largos": False,
        "lenta": False,
    },
    "mamut": {
        "granja": False,
        "cola_larga": True,
        "leal": False,
        "vuela": False,
        "bigotes": False,
        "dientes_grandes": False,
        "salta": False,
        "tranquilidad": False,
        "pone_huevos": False,
        "galopa": False,
        "colmillos_largos": True,
        "lenta": False,
    },
    "tortuga": {
        "granja": False,
        "cola_larga": False,
        "leal": False,
        "vuela": False,
        "bigotes": False,
        "dientes_grandes": False,
        "salta": False,
        "tranquilidad": True,
        "pone_huevos": True,
        "galopa": False,
        "colmillos_largos": False,
        "lenta": True,
    },
}


def calcular_valor(animal):
    valor = 0

    for clave, descripcion, peso in CARACTERISTICAS:
        if animal.get(clave, False):
            valor += peso

    return valor


def main():
    datos = {
        "caracteristicas": [
            {
                "clave": clave,
                "descripcion": descripcion,
                "peso": peso
            }
            for clave, descripcion, peso in CARACTERISTICAS
        ],
        "animales": []
    }

    for nombre, atributos in ANIMALES.items():
        animal = {
            "nombre": nombre,
            "atributos": atributos,
            "valor_agregado": calcular_valor(atributos)
        }

        datos["animales"].append(animal)

    ARCHIVO_DATOS.write_text(
        json.dumps(datos, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Archivo creado: {ARCHIVO_DATOS}")
    print("\nValores calculados:")

    for animal in datos["animales"]:
        print(f"{animal['nombre']:15} {animal['valor_agregado']}")


if __name__ == "__main__":
    main()