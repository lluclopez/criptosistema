import tkinter as tk
import os
from sympy import mod_inverse
from tkinter import filedialog
import math
import unicodedata

# Funcions per normalitzar el text
def normalitzar_text(text):
    text_normalitzat = unicodedata.normalize('NFD', text)
    text_sense_accents = ''.join(
        lletra for lletra in text_normalitzat if unicodedata.category(lletra) != 'Mn'
    )
    return text_sense_accents.lower()

# Funcions per seleccionar arxius i llegir/escriure fitxers
def seleccionar_arxiu():
    root = tk.Tk()
    root.withdraw()
    archivo_seleccionado = filedialog.askopenfilename()
    return archivo_seleccionado

def llegir_fitxer(fitxer):
    with open(fitxer, 'r', encoding='utf-8') as file:
        return file.read()

def escriure_fitxer(nom_fitxer, contingut):
    with open(nom_fitxer, 'w', encoding='utf-8') as file:
        file.write(contingut)

# Funcions per xifrat i desxifrat per substitució
def xifrar_paraula(paraula):
    L = 26  # Mida de l'alfabet anglès
    llargada = len(paraula)
    a = max([i for i in range(1, L) if math.gcd(i, L) == 1 and i <= llargada], default=1)
    c = ord(paraula[0].lower()) - ord('a')
    resultat = []
    for lletra in paraula:
        if lletra.isalpha():
            x = ord(lletra.lower()) - ord('a')
            xifrada = (a * x + c) % L
            resultat.append(chr(xifrada + ord('a')))
        else:
            resultat.append(lletra)
    return ''.join(resultat)

def desxifrar_paraula(paraula, c):
    L = 26
    llargada = len(paraula)
    a = max([i for i in range(1, L) if math.gcd(i, L) == 1 and i <= llargada], default=1)
    a_inv = mod_inverse(a, L)
    resultat = []
    for lletra in paraula:
        if lletra.isalpha():
            y = ord(lletra.lower()) - ord('a')
            original = (a_inv * (y - c)) % L
            resultat.append(chr(original + ord('a')))
        else:
            resultat.append(lletra)
    return ''.join(resultat)

# Funció per xifrar i guardar els valors de 'c'
def xifrar(text, fitxer_cs):
    paraules = text.split()
    resultat = []
    cs = []
    for paraula in paraules:
        if paraula:
            c = ord(paraula[0].lower()) - ord('a')
            cs.append(str(c))
            resultat.append(xifrar_paraula(paraula))
    escriure_fitxer(fitxer_cs, ' '.join(cs))
    return ' '.join(resultat)

# Funció per desxifrar utilitzant els valors de 'c'
def desxifrar(text, fitxer_cs):
    cs = llegir_fitxer(fitxer_cs).split()
    paraules = text.split()
    resultat = []
    for idx, paraula in enumerate(paraules):
        if paraula and idx < len(cs):
            c = int(cs[idx])
            resultat.append(desxifrar_paraula(paraula, c))
    return ' '.join(resultat)

def transposar(text, permutacio):
    K = len(permutacio)
    # Omplir una matriu amb K columnes
    matriu = [list(text[i:i+K].ljust(K)) for i in range(0, len(text), K)]
    
    # Apliquem la permutació, llegint per columnes segons l'ordre de la permutació
    resultat = []
    for col in permutacio:
        for fila in matriu:
            resultat.append(fila[col - 1])  # -1 perquè la permutació està basada en 1, no en 0

    return ''.join(resultat)

def destransposar(text, permutacio):
    K = len(permutacio)
    n_files = len(text) // K + (1 if len(text) % K != 0 else 0)  # Nombre de files a la matriu

    # Crear una matriu buida amb K columnes i tantes files com necessitem
    matriu = [[''] * K for _ in range(n_files)]
    
    # Col·locar el text xifrat a les columnes seguint la permutació
    idx = 0
    for col in permutacio:
        for fila in range(n_files):
            if idx < len(text):
                matriu[fila][col - 1] = text[idx]  # Col·locar a la columna corresponent
                idx += 1

    # Llegim el text resultant per files per restaurar el text original
    resultat = []
    for fila in matriu:
        resultat.extend(fila)

    return ''.join(resultat).strip()  # Eliminem els espais extra al final


# Funció iterativa de xifrat
def xifrar_iteratiu(text, N, permutacio_inicial, nom_fitxer_sortida_sense_extensio):
    resultat = text
    permutacio = permutacio_inicial[:]
    for i in range(N):
        #fitxer_cs_iter = f"{nom_fitxer_sortida_sense_extensio}_c{i+1}.txt"
        #resultat = xifrar(resultat, fitxer_cs_iter)
        resultat = transposar(resultat, permutacio)
        print(resultat+"|")
        permutacio = permutacio[1:] + permutacio[:1]
    return resultat

# Funció iterativa de desxifrat
def desxifrar_iteratiu(text, N, permutacio_inicial, nom_fitxer_entrada_sense_extensio):
    resultat = text
    permutacio = permutacio_inicial[:]
    for i in range(N-1):
        permutacio = permutacio[1:] + permutacio[:1]
    for i in reversed(range(N)):
        print(f"Missatge xifrat: {resultat}")
        print(f"Destransposició aplicada: {permutacio}")
        resultat = destransposar(resultat, permutacio) #!
        print(f"Missatge desxifrat (permutacio): {resultat}")
        #fitxer_cs_iter = f"{nom_fitxer_entrada_sense_extensio}_c{i+1}.txt"
        #if not os.path.exists(fitxer_cs_iter):
         #   print(f"No s'ha trobat el fitxer de valors de c ({fitxer_cs_iter}).")
          #  return
        #resultat = desxifrar(resultat, fitxer_cs_iter)
        print(f"Missatge desxifrat (substitució): {resultat}|")
        permutacio = permutacio[-1:] + permutacio[:-1]
    return resultat

# Funció principal
def main():
    fitxer_entrada = seleccionar_arxiu()
    directori_entrada = os.path.dirname(fitxer_entrada)
    nom_fitxer_sortida = input("Nom del fitxer de sortida: ")
    nom_fitxer_sortida_complet = os.path.join(directori_entrada, nom_fitxer_sortida)
    
    nom_sense_extensio_entrada, extensio = os.path.splitext(fitxer_entrada)
    nom_sense_extensio_sortida, extensio_sortida = os.path.splitext(nom_fitxer_sortida_complet)
    
    mode = input("Xifrat o desxifrat? (x/d): ").lower()
    N = int(input("Nombre d'iteracions: "))
    permutacio_inicial = list(map(int, input("Introdueix la permutació inicial (separada per espais): ").split()))

    text = llegir_fitxer(fitxer_entrada)
    text = normalitzar_text(text)
    print(text)

    if mode == 'x':
        resultat = xifrar_iteratiu(text, N, permutacio_inicial, nom_sense_extensio_sortida)
        operacio = "Xifrat"
    elif mode == 'd':
        resultat = desxifrar_iteratiu(text, N, permutacio_inicial, nom_sense_extensio_entrada)
        operacio = "Desxifrat"
    else:
        print("Mode no reconegut.")
        return

    escriure_fitxer(nom_fitxer_sortida_complet, resultat)
    print(f"{operacio} completat. El resultat s'ha guardat a {nom_fitxer_sortida_complet}.")

if __name__ == "__main__":
    main()
