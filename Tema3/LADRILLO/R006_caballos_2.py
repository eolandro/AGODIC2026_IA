# R006 - Problema de los caballos 2

import re

MOVS = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]


def a_indices(casilla, n):
	texto = casilla.strip().lower()
	if not re.fullmatch(r"[a-z]\d{1,2}", texto):
		return None
	columna = ord(texto[0]) - ord('a')
	numero = int(texto[1:])
	if not (0 <= columna < n and 1 <= numero <= n):
		return None
	return n - numero, columna

def a_casilla(f, c, n):
	return f"{chr(ord('a') + c)}{n - f}"



def crear_tablero(n):
	return [[0] * n for _ in range(n)]


def movimientos_validos(tablero, f, c):
	#Casillas a las que puede saltar el caballo desde (f, c) y que no ha visitado
	n = len(tablero)
	lista = []
	for df, dc in MOVS:
		nf, nc = f + df, c + dc
		if 0 <= nf < n and 0 <= nc < n and tablero[nf][nc] == 0:
			lista.append((nf, nc))
	return lista


def salidas(tablero, f, c):
	#Cuantas salidas libres tiene una casilla (para ordenar con Warnsdorff)
	return len(movimientos_validos(tablero, f, c))


def recorrer(tablero, f, c, paso):
	#Marca la casilla con el numero de paso y sigue recursivamente. Devuelve True si logra completar el recorrido
	tablero[f][c] = paso

	if paso == len(tablero) * len(tablero):
		return True  # ya se visitaron todas las casillas

	opciones = movimientos_validos(tablero, f, c)
	opciones.sort(key=lambda p: salidas(tablero, p[0], p[1]))

	for nf, nc in opciones:
		if recorrer(tablero, nf, nc, paso + 1):
			return True

	tablero[f][c] = 0  # vuelta atras: este camino no funciona
	return False


def obtener_ruta(tablero):
	#Lista de casillas (fila, columna) en el orden en que se visitaron
	n = len(tablero)
	ruta = [None] * (n * n)
	for f in range(n):
		for c in range(n):
			ruta[tablero[f][c] - 1] = (f, c)
	return ruta

def imprimir_tablero(tablero):
	#Imprime el tablero como uno real: columnas a-h abajo y arriba, filas n..1 a los lados, y dentro de cada casilla el numero de paso en que se visito
	n = len(tablero)
	ancho = len(str(n * n))
	borde = "   +" + ("-" * (ancho + 2) + "+") * n
	letras = "    " + " ".join(f"{chr(ord('a') + c):^{ancho + 2}}" for c in range(n))
	print(letras)
	print(borde)
	for f, fila in enumerate(tablero):
		etiqueta = f"{n - f:>2}"
		print(f"{etiqueta} |" + "|".join(f" {v:>{ancho}} " for v in fila) + f"| {etiqueta.strip()}")
		print(borde)
	print(letras)
	print()

def imprimir_recorrido(tablero):
	#Imprime la lista ordenada de casillas en notacion de ajedrez
	n = len(tablero)
	print("Recorrido:")
	print(" -> ".join(a_casilla(f, c, n) for f, c in obtener_ruta(tablero)))
	print()

def recorrido(inicio="a1", n=8):
	posicion = a_indices(inicio, n) if isinstance(inicio, str) else None
	if n < 1 or posicion is None:
		ultima = chr(ord('a') + n - 1) if 1 <= n <= 26 else "?"
		print(f"Casilla invalida: '{inicio}'. Usa una letra de la a a la {ultima} y un numero "
			  f"del 1 al {n}, por ejemplo e4.\n")
		return False

	f, c = posicion
	tablero = crear_tablero(n)
	print(f"Tablero {n}x{n}. El caballo entra por la casilla {inicio.strip().lower()}.\n")

	if recorrer(tablero, f, c, 1):
		print("¡El caballo recorrio todo el tablero!\n")
		imprimir_tablero(tablero)
		imprimir_recorrido(tablero)
		return True

	print(f"No existe un recorrido completo en un tablero {n}x{n} empezando en {inicio.strip().lower()}.\n")
	return False


if __name__ == "__main__":
	print("------ RECORRIDO DEL CABALLO ------")
	print("Escribe la casilla de entrada como en el tablero de ajedrez: ")
	print("columna de la -a- a la -h- y fila del 1 al 8. Ejemplo:  a1   e4   h8")

	while True:
		comando = input("Casilla de entrada o comando: ").strip()

		if comando.lower() == 'q':
			print("Programa finalizado.")
			break

		if re.fullmatch(r"[a-zA-Z]\d{1,2}", comando):
			recorrido(comando)
			continue

		try:
			eval(comando)
		except Exception as e:
			print(f"Error al evaluar la instruccion: {e}")
			print("Escribe una casilla como e4, o un comando como recorrido('e4')\n")
