import math
import unicodedata
import tkinter as tk
from tkinter import filedialog
import os

# Funció per trobar el coprimer més proper a una llargada
def coprimer_proper(llargada, L=26):
    coprimers = [i for i in range(1, L) if math.gcd(i, L) == 1]
    diferencies = [(abs(llargada - cp), cp) for cp in coprimers]
    return min(diferencies)[1]

# Funció de xifrat per substitució polialfabètica
def xifrar_paraula(paraula):
    L = 26  # Mida de l'alfabet anglès
    llargada = len(paraula)
    a = coprimer_proper(llargada)  # Trobar el coprimer més proper
    c = ord(paraula[0].lower()) - ord('a')  # c és el codi de la primera lletra de la paraula
    resultat = []
    for lletra in paraula:
        if lletra.isalpha():
            x = ord(lletra.lower()) - ord('a')
            xifrada = (a * x + c) % L
            resultat.append(chr(xifrada + ord('a')))
        else:
            resultat.append(lletra)
    return ''.join(resultat)

# Funció per desxifrar una paraula
def desxifrar_paraula(paraula, c):
    L = 26
    llargada = len(paraula)
    a = coprimer_proper(llargada)  # Utilitzar el mateix coprimer
    a_inv = pow(a, -1, L)  # Invers modular de 'a'
    resultat = []
    for lletra in paraula:
        if lletra.isalpha():
            y = ord(lletra.lower()) - ord('a')
            original = (a_inv * (y - c)) % L
            resultat.append(chr(original + ord('a')))
        else:
            resultat.append(lletra)
    return ''.join(resultat)

# Funció per escriure en un fitxer
def escriure_fitxer(nom_fitxer, contingut):
    with open(nom_fitxer, 'w', encoding='utf-8') as file:
        file.write(contingut)

# Funció per llegir d'un fitxer
def llegir_fitxer(fitxer):
    with open(fitxer, 'r', encoding='utf-8') as file:
        return file.read()

# Funció per seleccionar un arxiu
def seleccionar_arxiu():
    root = tk.Tk()
    root.withdraw()
    arxiu_seleccionat = filedialog.askopenfilename()
    return arxiu_seleccionat

# Funció per normalitzar el text
def normalitzar_text(text):
    text_normalitzat = unicodedata.normalize('NFD', text)
    text_sense_accents = ''.join(
        lletra for lletra in text_normalitzat if unicodedata.category(lletra) != 'Mn'
    )
    return text_sense_accents.lower()

# Funció de transposició
def transposar(text, permutacio):
    K = len(permutacio)
    matriu = [list(text[i:i + K]) for i in range(0, len(text), K)]
    if len(matriu[-1]) < K:
        matriu[-1].extend([' '] * (K - len(matriu[-1])))

    resultat = []
    for col in permutacio:
        for fila in matriu:
            resultat.append(fila[col - 1])
    return ''.join(resultat)

# Funció de destransposició
def destransposar(text, permutacio):
    K = len(permutacio)
    n_files = len(text) // K + (1 if len(text) % K != 0 else 0)
    matriu = [[''] * K for _ in range(n_files)]
    idx = 0
    for col in permutacio:
        for fila in range(n_files):
            if idx < len(text):
                matriu[fila][col - 1] = text[idx]
                idx += 1
    resultat = []
    for fila in matriu:
        resultat.extend(fila)
    return ''.join(resultat).rstrip()

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
    print(f"\nText normalitzat: {text}")

    fitxer_cs = "valors_cs.txt"

    if mode == 'x':
        # Xifrat per substitució polialfabètica
        text_substituit = xifrar_subs(text, fitxer_cs)
        print(f"\nText després del xifrat per substitució: {text_substituit}")
        
        # Xifrat per transposició
        resultat = text_substituit
        permutacio = permutacio_inicial[:]

        for i in range(N):
            print(f"\nIteració {i+1} - Permutació: {permutacio}")
            resultat = transposar(resultat, permutacio)
            print(f"Text xifrat després de la iteració {i+1}: {resultat}")
            permutacio = permutacio[1:] + permutacio[:1]

        operacio = "Xifrat"
    elif mode == 'd':
        # Invers de la permutació per transposició
        permutacio = permutacio_inicial[:]
        for i in range(N-1):
            permutacio = permutacio[1:] + permutacio[:1]

        resultat = text
        for i in reversed(range(N)):
            print(f"\nIteració {N-i} (Desxifrant) - Permutació: {permutacio}")
            resultat = destransposar(resultat, permutacio)
            print(f"Text desxifrat després de la iteració {N-i}: {resultat}")
            permutacio = permutacio[-1:] + permutacio[:-1]

        # Desxifrat per substitució
        resultat = desxifrar_subs(resultat, fitxer_cs)
        print(f"\nText després de desxifrar per substitució: {resultat}")

        operacio = "Desxifrat"
    else:
        print("Mode no reconegut.")
        return

    escriure_fitxer(nom_fitxer_sortida_complet, resultat)
    print(f"{operacio} completat. El resultat s'ha guardat a {nom_fitxer_sortida_complet}.")

if __name__ == "__main__":
    main()
