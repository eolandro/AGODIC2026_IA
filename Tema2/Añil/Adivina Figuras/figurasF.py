import json

with open("caminos.json", encoding="utf-8") as f:
    datos = json.load(f)

preguntas = dict(datos["Preguntas"])          # {camino: pregunta o figura}

trans = {}                                    # {camino: {respuesta: destino}}
for camino, respuesta, destino in datos["Trans"]:
    trans.setdefault(camino, {})[str(respuesta)] = destino

# Figura = camino sin transiciones de salida
figuras = sorted(t for n, t in preguntas.items() if n not in trans)


def normalizar(texto):
    return texto.strip().lower().replace("í", "i")      # acepta "sí" y "si"


def preguntar(camino):
    """Hace la pregunta del camino, valida la respuesta y devuelve el
    camino al que lleva (según Trans del JSON)."""
    opciones = trans[camino]
    print(f"\n{preguntas[camino]}")
    print("Opciones:", " / ".join(opciones))
    while (resp := normalizar(input("> "))) not in opciones:
        print("Respuesta no válida, intenta de nuevo.")
    return opciones[resp]


def jugar():
    c = preguntar(0)                 # ¿Cuántos lados tiene?

    if c == 1:                       # 0 lados
        c = preguntar(1)             # ¿Radio constante? -> Círculo / Elipse

    elif c == 2:                     # 3 lados (triángulos)
        c = preguntar(2)             # ¿Lados iguales? -> Equilátero / 11
        if c == 11:
            c = preguntar(11)        # ¿Ángulo de 90°? -> Rectángulo / 13
            if c == 13:
                c = preguntar(13)    # ¿Dos lados iguales? -> Isósceles / Escaleno

    elif c == 3:                     # 4 lados (cuadriláteros)
        c = preguntar(3)             # ¿Dos pares paralelos? -> 16 / 17
        if c == 16:
            c = preguntar(16)        # ¿Lados iguales? -> 20 / 21
        c = preguntar(c)             # 20, 21 o 17: última pregunta

    # 5, 6, 7 u 8 lados llegan aquí directo: c ya es la figura
    print(f"\n>>> La figura es: {preguntas[c]}")

print("=== ADIVINADOR DE FIGURAS ===")
print(f"Figuras posibles ({len(figuras)}):")
for i, nombre in enumerate(figuras, 1):
    print(f"  {i:>2}. {nombre}")
print("\nPiensa en una de ellas y responde las preguntas.")

otra = "si"
while otra == "si":
    jugar()
    otra = normalizar(input("\n¿Quieres jugar de nuevo? (si/no): "))

print("\n¡Gracias por jugar!")
