import tkinter as tk
import os
from sympy import mod_inverse
from tkinter import filedialog
import math
import unicodedata

def normalitzar_text(text):
    # Descomponem els caràcters en la seva forma base (NFD) i eliminem els diacrítics
    text_normalitzat = unicodedata.normalize('NFD', text)
    text_sense_accents = ''.join(
        lletra for lletra in text_normalitzat if unicodedata.category(lletra) != 'Mn'
    )
    
    return text_sense_accents.lower()  # Convertim tot a minúscules

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

def xifrar_paraula(paraula):
    L = 26  # Mida de l'alfabet anglès
    llargada = len(paraula)
    
    # Trobar el valor de 'a' (coprimer més proper a la llargada de la paraula)
    a = max([i for i in range(1, L) if math.gcd(i, L) == 1 and i <= llargada], default=1)
    
    # Valor de 'c' (valor de la primera lletra)
    c = ord(paraula[0].lower()) - ord('a')
    
    resultat = []
    for lletra in paraula:
        if lletra.isalpha():  # Si és una lletra de l'alfabet
            x = ord(lletra.lower()) - ord('a')
            xifrada = (a * x + c) % L
            lletra_xifrada = chr(xifrada + ord('a'))
            resultat.append(lletra_xifrada)
        else:
            resultat.append(lletra)
    
    return ''.join(resultat)

def desxifrar_paraula(paraula, c):
    L = 26
    llargada = len(paraula)
    
    # Trobar el valor de 'a' (coprimer més proper a la llargada de la paraula)
    a = max([i for i in range(1, L) if math.gcd(i, L) == 1 and i <= llargada], default=1)
    
    # Inversa modular d'a
    a_inv = mod_inverse(a, L)
    
    resultat = []
    for lletra in paraula:
        if lletra.isalpha():
            y = ord(lletra.lower()) - ord('a')
            original = (a_inv * (y - c)) % L
            lletra_original = chr(original + ord('a'))
            resultat.append(lletra_original)
        else:
            resultat.append(lletra)
    
    return ''.join(resultat)

def xifrar(text, fitxer_cs):
    # Normalitzem el text abans de xifrar-lo
    text = normalitzar_text(text)
    
    paraules = text.split()  # Separar el text en paraules
    resultat = []
    cs = []  # Llista per guardar els valors de c

    for paraula in paraules:
        if paraula:  # Si la paraula no és buida
            # Calculem 'c' com el valor de la primera lletra
            c = ord(paraula[0].lower()) - ord('a')
            cs.append(str(c))  # Guardem el valor de c com a string
            resultat.append(xifrar_paraula(paraula))

    # Guardem els valors de c en el fitxer
    escriure_fitxer(fitxer_cs, ' '.join(cs))
    
    return ' '.join(resultat)

def desxifrar(text, fitxer_cs):
    # Llegir el fitxer amb els valors de 'c'
    cs = llegir_fitxer(fitxer_cs).split()  # Llegim i separem els valors de c
    paraules = text.split()  # Separar el text en paraules
    resultat = []

    for idx, paraula in enumerate(paraules):
        if paraula and idx < len(cs):  # Assegurar que tenim un valor de c per a cada paraula
            c = int(cs[idx])  # Convertim el valor de c a un enter
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
    
    # Apliquem la permutació inversa i col·loquem el text a la matriu
    idx = 0
    for col in permutacio:
        for fila in range(n_files):
            if idx < len(text):
                matriu[fila][col - 1] = text[idx]  # Col·locar a la columna corresponent
                idx += 1

    # Llegim el text per files per restaurar el text original
    resultat = []
    for fila in matriu:
        resultat.extend(fila)

    return ''.join(resultat).strip()  # Eliminem els espais extra al final

def xifrar_iteratiu(text, N, permutacio_inicial, fitxer_cs):
    resultat = text
    permutacio = permutacio_inicial[:]

    for i in range(N):
        # Primer xifrem per substitució
        resultat = xifrar(resultat, fitxer_cs)
        
        # Després fem la transposició
        resultat = transposar(resultat, permutacio)
        
        # Fem un shift a l'esquerra a la permutació
        permutacio = permutacio[1:] + permutacio[:1]

    return resultat

def desxifrar_iteratiu(text, N, permutacio_inicial, fitxer_cs):
    resultat = text
    permutacio = permutacio_inicial[:]

    for i in range(N):
        # Fem el shift a la permutació inversa de la mateixa manera
        permutacio = permutacio[1:] + permutacio[:1]

    # Iterem en ordre invers: primer destransposar, després desxifrar
    for i in range(N):
        # Desfem la transposició
        resultat = destransposar(resultat, permutacio)
        
        # Desxifrem per substitució
        resultat = desxifrar(resultat, fitxer_cs)
        
        # Desfem el shift a l'esquerra
        permutacio = permutacio[-1:] + permutacio[:-1]

    return resultat

def main():
    fitxer_entrada = seleccionar_arxiu()
    directori_entrada = os.path.dirname(fitxer_entrada)
    nom_fitxer_sortida = input("Nom del fitxer de sortida: ")
    nom_fitxer_sortida_complet = os.path.join(directori_entrada, nom_fitxer_sortida)
    
    
    # Separem el nom del fitxer de la seva extensió
    nom_sense_extensio, extensio = os.path.splitext(fitxer_entrada)
    nom_sortida_sense_extensio, extensio = os.path.splitext(nom_fitxer_sortida_complet)
    
    mode = input("Xifrat o desxifrat? (x/d): ").lower()
    N = int(input("Nombre d'iteracions: "))
    permutacio_inicial = list(map(int, input("Introdueix la permutació inicial (separada per espais): ").split()))

    text = llegir_fitxer(fitxer_entrada)

    if mode == 'x':
        # Generem el fitxer dels valors de c com a <nom_sense_extensio>_c.txt
        fitxer_cs = nom_sortida_sense_extensio + "_c.txt"
        resultat = xifrar_iteratiu(text, N, permutacio_inicial, fitxer_cs)
        operacio = "Xifrat"
    elif mode == 'd':
        # Quan desxifrem, busquem el fitxer amb els valors de c
        fitxer_cs = nom_sense_extensio + "_c.txt"
        if not os.path.exists(fitxer_cs):
            print(f"No s'ha trobat el fitxer de valors de c ({fitxer_cs}).")
            return
        resultat = desxifrar_iteratiu(text, N, permutacio_inicial, fitxer_cs)
        operacio = "Desxifrat"
    else:
        print("Mode no reconegut.")
        return

    escriure_fitxer(nom_fitxer_sortida_complet, resultat)
    print(f"{operacio} completat. El resultat s'ha guardat a {nom_fitxer_sortida_complet}.")
    if mode == 'x':
        print(f"Els valors de 'c' s'han guardat a {fitxer_cs}.")

if __name__ == "__main__":
    main()