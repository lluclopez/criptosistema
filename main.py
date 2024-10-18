import tkinter as tk
import os
from tkinter import filedialog
from sympy import mod_inverse
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

# Funció per trobar el coprimer més proper a una llargada
def coprimer_proper(llargada, L=26):
    # Buscar el coprimer més proper a la llargada
    coprimers = [i for i in range(1, L) if math.gcd(i, L) == 1]
    diferencies = [(abs(llargada - cp), cp) for cp in coprimers]
    # Triar el coprimer més proper, i en cas d'empat, el més petit
    return min(diferencies)[1]

# Funció de xifrat per substitució polialfabètica
def xifrar_paraula(paraula, c):
    L = 26  # Mida de l'alfabet anglès
    llargada = len(paraula)
    a = coprimer_proper(llargada)  # Trobar el coprimer més proper
    resultat = []
    for lletra in paraula:
        if lletra.isalpha():  # Només xifrem lletres
            x = ord(lletra.lower()) - ord('a')  # Convertir la lletra a un valor entre 0 i 25
            xifrada = (a * x + c) % L
            resultat.append(chr(xifrada + ord('a')))  # Tornar a convertir el valor xifrat en lletra
        else:
            resultat.append(lletra)  # Mantenir els caràcters que no són lletres
    return ''.join(resultat)

# Funció per desxifrar paraula
def desxifrar_paraula(paraula, c):
    L = 26
    llargada = len(paraula)
    a = coprimer_proper(llargada)  # Trobar el mateix coprimer que es va utilitzar per xifrar
    # a_inv = mod_inverse(a, L)
    a_inv = pow(a, -1, L)  # Trobar l'invers modular d'a per desxifrar
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
def xifrar_subs(text, fitxer_cs):
    paraules = text.split()
    resultat = []
    cs = []
    for paraula in paraules:
        if paraula:
            c = ord(paraula[0].lower()) - ord('a')
            cs.append(str(c))
            resultat.append(xifrar_paraula(paraula, c))
    escriure_fitxer(fitxer_cs, ' '.join(cs))
    return ' '.join(resultat)

# Funció per desxifrar utilitzant els valors de 'c'
def desxifrar_subs(text, fitxer_cs):
    cs = llegir_fitxer(fitxer_cs).split()
    paraules = text.split()
    resultat = []
    for idx, paraula in enumerate(paraules):
        if paraula and idx < len(cs):
            c = int(cs[idx])
            resultat.append(desxifrar_paraula(paraula, c))
    return ' '.join(resultat)

# Funcions per transposició i destransposició
def transposar(text, permutacio):
    K = len(permutacio)
    n_files = math.ceil(len(text) / K)  # Nombre de files necessàries
    ultima_fila_completa = len(text) % K  # Columnes útils a l'última fila

    # Crear la matriu amb les files necessàries
    matriu = [list(text[i:i + K]) for i in range(0, len(text), K)]

    # Si l'última fila no està completa, no afegim espais, només registrem quina part falta
    if len(matriu[-1]) < K:
        matriu[-1].extend([''] * (K - len(matriu[-1])))

    print("Matriu durant el xifrat:")
    for fila in matriu:
        print(fila)

    resultat = []
    # Aplicar la permutació
    for col in permutacio:
        for fila in matriu:
            if fila[col - 1] != '':  # Només afegim si no és un espai buit
                resultat.append(fila[col - 1])
    return ''.join(resultat)

def destransposar(text, permutacio):
    K = len(permutacio)
    n_files = math.ceil(len(text) / K)  # Nombre de files necessàries
    ultima_fila_completa = len(text) % K  # Columnes amb l'última fila completa

    # Crear una matriu buida amb les files necessàries
    matriu = [[''] * K for _ in range(n_files)]

    idx = 0
    # Omplir la matriu seguint la permutació
    for col in permutacio:
        for fila in range(n_files):
            # Evitar omplir columnes que no tenen caràcter a l'última fila
            if fila == n_files - 1 and col > ultima_fila_completa:
                continue  # Saltar columnes incompletes
            if idx < len(text):
                matriu[fila][col - 1] = text[idx]
                idx += 1

    print("Matriu durant el desxifrat:")
    for fila in matriu:
        print(fila)

    # Llegir per files per reconstruir el text original
    resultat = []
    for fila in matriu:
        resultat.extend(fila)

    # Convertir la llista en text, sense modificar espais finals legítims
    return ''.join(resultat)

# Funció iterativa de xifrat
def xifrar_iteratiu(text, N, permutacio_inicial, nom_fitxer_sortida_sense_extensio):
    resultat = text
    permutacio = permutacio_inicial[:]
    
    for i in range(N):
        fitxer_cs_iter = f"{nom_fitxer_sortida_sense_extensio}_c{i+1}.txt"
        resultat = xifrar_subs(resultat, fitxer_cs_iter)
        print(f"Iteració {i+1} - Permutació: {permutacio}")
        resultat = transposar(resultat, permutacio)
        print(f"Resultat xifrat: .{resultat}.")
        # Desplaçar la permutació cap a l'esquerra
        permutacio = permutacio[1:] + permutacio[:1]
    
    return resultat

# Funció iterativa de desxifrat
def desxifrar_iteratiu(text, N, permutacio_inicial, nom_fitxer_sortida_sense_extensio):
    resultat = text
    permutacio = permutacio_inicial[:]

    # Ajustar la permutació inicial per desxifrar (moure cap a l'esquerra)
    for i in range(N-1):
        permutacio = permutacio[1:] + permutacio[:1]

    # Desxifrar iterativament en ordre invers
    for i in reversed(range(N)):
        print(f"Iteració {N-i} - Permutació: {permutacio}")
        resultat = destransposar(resultat, permutacio)
        print(f"Resultat desxifrat: .{resultat}.")


        fitxer_cs_iter = f"{nom_fitxer_sortida_sense_extensio}_c{i+1}.txt"
        if not os.path.exists(fitxer_cs_iter):
            print(f"No s'ha trobat el fitxer de valors de c ({fitxer_cs_iter}).")
            return
        resultat = desxifrar_subs(resultat, fitxer_cs_iter)


        # Desplaçar cap a la dreta la permutació
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
    print('.'+text+'.')

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
