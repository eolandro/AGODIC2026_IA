import json
import random

ArchivoEntrada = "tabla_pesos.json"

def si_no(mensaje):
    while True:
        valor = input(mensaje).strip().upper()
        if valor in ("S", "N"):
            return valor
        print("Respuesta inválida, ingresa 'S' para Sí o 'N' para No. :)")

def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

#-------------------------------------- MAIN --------------------------------------#
datos = cargar_json(ArchivoEntrada)
caracteristicas = [c["nombre"] for c in datos["caracteristicas"]]  # ya vienen de mayor a menor peso
tabla = {fila["animal"]: fila for fila in datos["tabla"]}
candidatos = list(tabla.keys())

print("* * * ADIVINADOR * * *\n")
print("Piensa en un animal de la siguiente lista y responde las preguntas:")
print(", ".join(candidatos))
input("\nPresiona Enter cuando estés listo. :)\n")

for característica in caracteristicas:
    if len(candidatos) <= 1:
        break
    resp = si_no(f"¿Tu animal cumple con: '{característica}'? (S/N): ")
    nuevos_candidatos = [a for a in candidatos if tabla[a][característica] == resp]
    if nuevos_candidatos:
        candidatos = nuevos_candidatos
    else:
        print("\nTramposillo, ningún animal de mi lista coincide con esa combinación de respuestas.")
        print("Puede que estés pensando en un animal que no conozco, o hubo alguna respuesta inconsistente.")
        candidatos = []
        break
print()

acerte = False
while candidatos:
    AnimalPropuesto = random.choice(candidatos)
    confirmación = si_no(f"Creo que tu animal es: '{AnimalPropuesto}'. ¿Acerté? (S/N): ")
    if confirmación == "S":
        print(f"\n¡WuJUUUUU! tu animal es '{AnimalPropuesto}'. :)")
        acerte = True
        break
    else:
        candidatos.remove(AnimalPropuesto)
if not acerte and not candidatos:
    print("\nMe rindo, no logré adivinar tu animal. :(")