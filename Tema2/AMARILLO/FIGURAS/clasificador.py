import json, re, unicodedata

D = json.load(open("figuras.json", encoding="utf-8"))
N, F, A = D["nodos"], D["figuras"], D["aristas"]                  
SIN = {w: c for c, ws in D["sinonimos"].items() for w in ws}      
AVISO = {0: "   Anotado. Ninguna figura de mi lista coincide.\n", 1: "   Anotado. Solo queda 1 figura posible: ya no necesito más preguntas.\n",
         2: "   Anotado. Me quedan {} figuras posibles.\n"}
TITULO = {1: "¡Estabas pensando en: {}!", 0: "Tu figura no está en mi lista, no puedo adivinarla.",
          2: "Aún quedan varias figuras posibles y no tengo más preguntas."}

def palabras(t):
    t = "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
    return [SIN.get(w, w) for w in re.findall(r"[\w?]+", t)]


def opciones(n):
    """Aristas que salen del nodo n: {clave: arista}."""
    return {k.split("|")[1]: v for k, v in A.items() if k.startswith(n + "|")}


def coincidencias(op, t):
    pares = [(len(a), k, a) for k, e in op.items() for a in e["acepta"]]
    return sorted((l, k) for l, k, a in filter(lambda p: f" {p[2]} " in t, pares))


def entender(n, texto, quedan):
    op, p = opciones(n), palabras(texto)
    t = " " + " ".join(p) + " "
    hits = coincidencias(op, t) or coincidencias(op, t + "# " * any(map(str.isdigit, p)))  
    top = [l for l, _ in hits[-1:]]
    mejores = set(k for l, k in filter(lambda h: h[0] in top, hits))
    cabe = lambda k: any(F[f]["attrs"].get(N[n]["atributo"]) in op[k]["vals"] for f in quedan)
    compat = list(filter(cabe, sorted(mejores)))
    elegidas = (compat or sorted(mejores))[:1] * (len(compat) < 2 and " ".join(p) not in D["no_se"])
    return op.get(next(iter(elegidas), None))


def preguntar(n, quedan):
    print(f"PREGUNTA: {N[n]['texto']}")
    r = input("   > ")
    while not (e := entender(n, r, quedan)):
        ej = " / ".join(v["acepta"][0] for v in opciones(n).values())
        print({True: f"   Pista: {N[n]['pista']}", False: f"   No entendí «{r}». Puedes responder, por ejemplo: {ej}"}[" ".join(palabras(r)) in D["no_se"]])
        r = input("   > ")
    return e


def jugar():
    print("\nADIVINA LA FIGURA\nPiensa en una de estas:\n")
    print(*[f"  {i:2}. {f}" for i, f in enumerate(sorted(v["nombre"] for v in F.values()), 1)], sep="\n")
    input("\nResponde con tus propias palabras o con números. Escribe NO SE para una pista. ENTER para comenzar... ")
    n, hechos, quedan = D["inicio"], [], set(F)        
    while n in N and len(quedan) > 1:                    
        e = preguntar(n, quedan)
        hechos.append((N[n]["texto"], e["op"]))
        quedan = set(filter(lambda f: F[f]["attrs"].get(N[n]["atributo"]) in e["vals"], quedan))
        n = e["a"]
        print(AVISO[min(len(quedan), 2)].format(len(quedan)))
    print("=" * 50, TITULO[min(len(quedan), 2)].format("".join(F[f]["nombre"].upper() for f in quedan)), "=" * 50, sep="\n")
    print(f"\nMi razonamiento ({len(hechos)} pregunta(s)):")
    print(*[f"  {i}. {p} → {r}" for i, (p, r) in enumerate(hechos, 1)], sep="\n")


otra = True
while otra:
    jugar()
    otra = palabras(input("\n¿Jugar otra vez?  > "))[:1] == ["si"]
print("¡Gracias por jugar!")
