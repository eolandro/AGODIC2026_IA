import argparse
import anlexsyn
import BVM

parser = argparse.ArgumentParser(description="Boome con toma de decisiones bayesiana (Boom_Bay)")
parser.add_argument("codigo", type=argparse.FileType('r'), help="archivo con el programa de Boome")
parser.add_argument("--mapa", default="mapa.txt", help="archivo del tablero (default: mapa.txt)")
parser.add_argument("--sens", type=float, default=0.9, help="P(+|bomba), sensibilidad del detector")
parser.add_argument("--fp", type=float, default=0.1, help="P(+|no bomba), tasa de falsos positivos")
parser.add_argument("--umbral", type=float, default=0.5, help="P(B) a partir de la cual se considera peligro")
parser.add_argument("--seguro", type=float, default=0.0001, help="P(B) por debajo de la cual la celda se considera segura")
parser.add_argument("--min", type=int, default=3, help="minimo de lecturas por deteccion")
parser.add_argument("--max", type=int, default=15, help="maximo de lecturas por deteccion")
parser.add_argument("--semilla", type=int, default=None, help="semilla para repetir resultados")
parser.add_argument("--tablero", action="store_true", help="imprimir el tablero en cada paso")
args = parser.parse_args()


def main():
	LineasCodigo = [linea.strip() for linea in args.codigo.readlines()]
	LineasCodigo = [linea for linea in LineasCodigo if linea]
	print(LineasCodigo)

	Resultados = [anlexsyn.linea(linea) for linea in LineasCodigo]
	if not all(r[0] for r in Resultados):
		print("Error encontrado en:")
		for n, (linea, r) in enumerate(zip(LineasCodigo, Resultados), start=1):
			if not r[0]:
				print(f"  Linea {n}: '{linea}' -> {r[1]}")
		return

	BooMe = BVM.BommeVirtualMachine(
		archivo_mapa=args.mapa, sensibilidad=args.sens, falso_positivo=args.fp,
		umbral=args.umbral, umbral_seguro=args.seguro, min_lecturas=args.min, max_lecturas=args.max,
		semilla=args.semilla,
	)
	print(f"Tablero leído de {args.mapa}: {len(BooMe.Mapa)}x{len(BooMe.Mapa[0])}, "
		  f"bombas: {len(BooMe.Bombas)}")
	print(f"Probabilidad a priori de bomba P(B) = {BooMe.Prior * 100:.2f}%  |  "
		  f"P(+|B) = {BooMe.Sens}  P(+|~B) = {BooMe.FP}")
	BooMe.LoadText(LineasCodigo)
	print(BooMe)
	while BooMe.Estado not in ["dead", "done", "boom"]:
		BooMe.step()
		if args.tablero:
			print(BooMe)
	print("\n===== Tablero final =====")
	print(BooMe)
	print("terminado")
	print(BooMe.ResumenPositivos())
	print(BooMe.MapaCreencias())


if __name__ == "__main__":
	main()
