listatom_liststring([A],[C]) :- atom_string(A,C).
listatom_liststring([A|RA],[ C | LCC]) :- 
	listatom_liststring(RA,LCC),
	atom_string(A,C).
	
string_to_liststring(Cadena,LCadenas) :- 
	string_chars(Cadena,LAtomos),
	listatom_liststring(LAtomos,LCadenas).


uhex("A").
uhex("B").
uhex("C").
uhex("D").
uhex("E").
uhex("F").
uhex(N) :- is_digit(N).

numhex(Str) :- string_to_liststring(Str,[S,A,B,C,D]),
				numhex(S,A,B,C,D).
numhex("#",A,B,C,D) :- uhex(A),uhex(B),uhex(C),uhex(D).

regs("R0").
regs("R1").
regs("R2").
regs("R3").

opmat("+").
opmat("-").

movs("arriba").
movs("abajo").
movs("izq").
movs("der").

opera(A,B,C) :- regs(A),opmat(B),regs(C).
opera(A,B,C) :- regs(A),opmat(B),numhex(C).
opera(A,B,C) :- numhex(A),opmat(B),regs(C).
opera(A,B,C) :- numhex(A),opmat(B),numhex(C).

asign(Str) :- split_string(Str," ","",[A,B,C]),asign(A,B,C).
asign(Str) :- split_string(Str," ","",[A,B,C,D]),asign(A,B,C,D).
asign(Str) :- split_string(Str," ","",[A,B,C,D,E]),asign(A,B,C,D,E).
asign(R,"=",Nh) :- regs(R),numhex(Nh).
asign(R,"=","sensor",M) :- regs(R),movs(M).
asign(R,"=",A,O,B) :- regs(R),opera(A,O,B).

linea(L) :- asign(L).
linea(L) :- movs(L).
linea(L) :- movs(L).
lineas([L]) :- linea(L).
lineas([P | R]) :- linea(P), lineas(R).
condicional("Si",Re,[F|R],"FinSi") :- regs(Re), lineas([F | R]).
ciclos("ciclo",Re,[F | R],"finciclo") :- regs(Re), lineas([F | R]).
