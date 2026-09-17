import argparse
import anlexsyn
import BVM

parser = argparse.ArgumentParser()
parser.add_argument(
	"codigo",
	type=argparse.FileType('r')
)
args = parser.parse_args()

def main():
	LineasCodigo = args.codigo.readlines()
	LineasCodigo =  [
		linea.strip() for linea in LineasCodigo if linea.strip()
	]
	LineasValidas = [
		anlexsyn.linea(linea)[0]
		for linea in LineasCodigo
	]
	print(LineasValidas)
	if not all(LineasValidas):
		print('Error encontrado en:')
		for i, (valida, linae) in enumerate(zip(LineasValidas, LineasCodigo), start=1):
			if not valida:
				print(f"Linea {i}: {linae}")
		#ToDo Colocar el error segun la lista
		return 
	
	BooMe = BVM.BoomeVirtualMachine()
	BooMe.loadText(LineasCodigo)
	print(BooMe)
	#while BooMe.Estado not in ["dead", "done"]:
	while BooMe.Estado == "ready":
		BooMe.step()
		print(BooMe)
	print("Terminado")
	
	
	
if __name__ == "__main__":
	main()
