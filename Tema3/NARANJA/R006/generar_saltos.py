letras = "abcdefgh"
vectores = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]

salida = open("saltos.json", "w")
salida.write("{\n")

total = 0
for numero in range(8, 0, -1):
    for l in range(8):
        lista = []
        for v in vectores:
            nl = l + v[0]
            nn = numero + v[1]
            if nl >= 0 and nl < 8 and nn >= 1 and nn <= 8:
                lista.append('"' + letras[nl] + str(nn) + '"')

        total = total + 1
        renglon = '  "' + letras[l] + str(numero) + '": [' + ", ".join(lista) + "]"
        if total < 64:
            renglon = renglon + ","
        salida.write(renglon + "\n")

salida.write("}\n")
salida.close()
print("saltos.json creado con", total, "casillas")
