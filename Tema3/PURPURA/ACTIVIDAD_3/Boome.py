'''
##R008##
##15##
"""
Descripción: Aplicacion de pathfinding A*.
Restricciones: NA
"""
'''
import argparse
import anlexsyn
import BVM

parser = argparse.ArgumentParser(description="Boome: busqueda de la bomba con A*")
parser.add_argument("tablero", nargs="?", default="tablero.json",
					help="archivo del tablero .json o .yaml (default: tablero.json)")
parser.add_argument("--bomba", default=None,
					help="posicion de la bomba elegida por el maestro: casilla (ej. 57) "
						 "o fila,col (ej. 5,7). Reemplaza la B del archivo")
args = parser.parse_args()


def main():
	# 1) Analisis lexico/sintactico del tablero
	datos = BVM.BommeVirtualMachine.LeerArchivo(args.tablero)
	Resultado = anlexsyn.tablero(datos)
	if not Resultado[0]:
		print(f"Error encontrado en {args.tablero}:")
		for e in Resultado[1]:
			print(f"  {e}")
		return

	# 2) Maquina virtual
	BooMe = BVM.BommeVirtualMachine(archivo_tablero=args.tablero)

	# 3) El maestro elige la bomba (por argumento o preguntando si no hay B)
	if args.bomba is not None:
		BooMe.ColocarBomba(args.bomba)
	elif BooMe.Bomba is None:
		print(BooMe)
		while True:
			texto = input("¿Dónde se coloca la bomba? (casilla, ej. 57, o fila,col, ej. 5,7): ")
			try:
				BooMe.ColocarBomba(texto)
				break
			except ValueError as e:
				print(f"  {e}. Intenta de nuevo.")

	bx, by = BooMe.Bomba
	print(f"Tablero: {args.tablero} ({len(BooMe.Mapa)}x{len(BooMe.Mapa[0])})  |  "
		  f"bomba en casilla {BooMe.NumCasilla(bx, by)} (fila {bx}, col {by})\n")

	# 4) A* y recorrido del camino
	if not BooMe.AEstrella():
		print("No existe un camino de R a la bomba.")
		print(BooMe)
		return
	while BooMe.Estado not in ["dead", "done"]:
		BooMe.step()

	# 5) Al final solo se muestra el camino resultante
	print(BooMe.CaminoResultante())


if __name__ == "__main__":
	try:
		main()
	except ValueError as e:
		print(f"Error: {e}")
