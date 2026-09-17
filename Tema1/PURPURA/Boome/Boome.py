import argparse
from pathlib import Path
import anlexsyn 
import BVM

parser=argparse.ArgumentParser()
parser.add_argument("codigo",type=argparse.FileType('r'))
args=parser.parse_args()

def main():
	LineasCodigo=args.codigo.readlines()
	LineasCodigo=[linea.strip() for linea in LineasCodigo]
	print(LineasCodigo)
	LineasValidas=[
		anlexsyn.linea(linea)[0]
		for linea in LineasCodigo
	]
	print(LineasValidas)
	if not all(LineasValidas):
		print('Error encontrado en:')
		#ToDo Colocar el error segun la lista 
		return
	BooMe=BVM.BommeVirtualMachine()
	BooMe.LoadText(LineasCodigo)
	print(BooMe)
	while BooMe.Estado not in ["dead","done","boom"]:
	#while BooMe.Estado == ["ready"]:
		BooMe.step()
		print(BooMe)
		print("terminado")
if __name__ == "__main__":
	main()
