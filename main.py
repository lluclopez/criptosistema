import tkinter as tk
import os
from sympy import mod_inverse  # Necessitarem calcular la inversa modular
from tkinter import filedialog

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    archivo_seleccionado = filedialog.askopenfilename()
    return archivo_seleccionado

# Funció per llegir el fitxer d'entrada (missatge en clar o xifrat)
def llegir_fitxer(fitxer):
    with open(fitxer, 'r', encoding='utf-8') as file:
        return file.read()

# Funció per escriure el resultat en un fitxer de sortida (missatge xifrat o desxifrat)
def escriure_fitxer(nom_fitxer, contingut):
    with open(nom_fitxer, 'w', encoding='utf-8') as file:
        file.write(contingut)

# Funció de substitució polialfabètica
def substitucio_polialfabetica(text, a, c):
    # Implementar la lògica de la substitució (placeholder per ara)
    return text  # Això haurà de ser el text xifrat

# Funció de transposició
def transposicio(text, permutacio):
    # Implementar la lògica de la transposició (placeholder per ara)
    return text  # Això haurà de ser el text transposat

def substitucio_polialfabetica(text, a, c):
    L = 26  # Mida de l'alfabet anglès
    text_xifrat = ""
    
    for char in text:
        if char.isalpha():  # Només xifrem les lletres
            x = ord(char.lower()) - ord('a')  # Convertim el caràcter en un número (a=0, b=1, ..., z=25)
            print(x)
            y = (a * x + c) % L  # Fórmula de xifrat afí
            text_xifrat += chr(y + ord('a'))  # Convertim el número de nou a caràcter
        else:
            text_xifrat += char  # Els altres caràcters (espais, puntuació) no es xifren
    
    return text_xifrat



def desxifrar_substitucio_polialfabetica(text, a, c):
    L = 26
    a_inv = mod_inverse(a, L)  # Inversa modular de 'a'
    text_desxifrat = ""
    
    for char in text:
        if char.isalpha():  # Només desxifrem les lletres
            y = ord(char.lower()) - ord('a')  # Convertim el caràcter en un número
            x = (a_inv * (y - c)) % L  # Fórmula de desxifrat
            text_desxifrat += chr(x + ord('a'))  # Convertim el número de nou a caràcter
        else:
            text_desxifrat += char  # Els altres caràcters no es desxifren
    
    return text_desxifrat


def transposicio(text, permutacio):
    K = len(permutacio)
    # Omplir la matriu amb les lletres del text
    matriu = [list(text[i:i+K]) for i in range(0, len(text), K)]
    
    # Transposar el text seguint l'ordre de la permutació
    text_transposat = ""
    for fila in matriu:
        for index in permutacio:
            if index - 1 < len(fila):  # Verificar que la columna existeix
                text_transposat += fila[index - 1]
    
    return text_transposat


def desxifrar_transposicio(text, permutacio):
    K = len(permutacio)
    inv_permutacio = sorted(range(len(permutacio)), key=lambda x: permutacio[x])
    
    # Crear la matriu amb el text transposat
    matriu = [list(text[i:i+K]) for i in range(0, len(text), K)]
    
    # Desxifrar el text seguint l'ordre invers de la permutació
    text_desxifrat = ""
    for fila in matriu:
        for index in inv_permutacio:
            if index < len(fila):  # Verificar que la columna existeix
                text_desxifrat += fila[index]
    
    return text_desxifrat


# Funció per xifrar el missatge amb el criptosistema iteratiu
def xifrar(text, N, permutacio_inicial):
    permutacio = permutacio_inicial
    for i in range(N):
        a = 5  # Aquest valor es pot calcular dinàmicament basat en la longitud
        c = 3  # Placeholder; això s'hauria de calcular basat en la primera lletra
        
        # Aplicar la substitució
        text = substitucio_polialfabetica(text, a, c)
        
        # Aplicar la transposició
        text = transposicio(text, permutacio)
        
        # Desplaçar la permutació a l'esquerra
        permutacio = permutacio[1:] + permutacio[:1]
    
    return text

# Funció per desxifrar el missatge amb el criptosistema iteratiu
def desxifrar(text, N, permutacio_inicial):
    permutacio = permutacio_inicial
    for i in range(N):
        # Aplicar la transposició inversa
        text = desxifrar_transposicio(text, permutacio)
        
        # Aplicar el desxifrat de la substitució
        a = 5  # Mismament s'ha de calcular
        c = 3  # Placeholder
        text = desxifrar_substitucio_polialfabetica(text, a, c)
        
        # Desplaçar la permutació a l'esquerra
        permutacio = permutacio[1:] + permutacio[:1]
    
    return text


# Funció principal del programa
def main():
    fitxer_entrada = seleccionar_archivo()

    directori_entrada = os.path.dirname(fitxer_entrada)
    
    #nom_fitxer_entrada = input("Nom del fitxer d'entrada: ")
    nom_fitxer_sortida = input("Nom del fitxer de sortida: ")
    nom_fitxer_sortida = os.path.join(directori_entrada, nom_fitxer_sortida)
    mode = input("Xifrat o desxifrat? (x/d): ").lower()
    N = int(input("Nombre d'iteracions: "))

    # Verificació que N sigui almenys 1
    if N < 1:
        print("El nombre d'iteracions ha de ser almenys 1.")
        N = 1 #? exit?
    
    permutacio_inicial = list(map(int, input("Introdueix la permutació inicial (separada per espais): ").split()))

    while not permutacio_inicial:
        print("La permutació inicial no pot ser buida.")
        permutacio_inicial = list(map(int, input("Introdueix una permutació vàlida (separada per espais): ").split()))

    
    # Llegir el contingut del fitxer
    text = llegir_fitxer(fitxer_entrada)

    # Processar segons el mode seleccionat
    if mode == 'x':  # Mode xifrat
        resultat = xifrar(text, N, permutacio_inicial)
        operacio = "Xifrat"
    elif mode == 'd':  # Mode desxifrat
        resultat = desxifrar(text, N, permutacio_inicial)  # Placeholder per a desxifrat
        operacio = "Desxifrat"
    else:
        print("Mode no reconegut.")
        return

    # Escriure el resultat en el fitxer de sortida
    escriure_fitxer(nom_fitxer_sortida, resultat)
    print(f"{operacio} completat. El resultat s'ha guardat a {nom_fitxer_sortida}.")

if __name__ == "__main__":
    main()