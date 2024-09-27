# Funció per llegir el fitxer d'entrada (missatge en clar o xifrat)
def llegir_fitxer(nom_fitxer):
    with open(nom_fitxer, 'r', encoding='utf-8') as file:
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

# Funció per xifrar el missatge amb el criptosistema iteratiu
def xifrar(text, N, permutacio_inicial):
    # Bucle per iterar el procés de xifrat N vegades
    for i in range(N):
        # Aplicar la substitució polialfabètica
        text = substitucio_polialfabetica(text, a=5, c=3)  # Placeholder per a i c

        # Aplicar la transposició amb la permutació
        text = transposicio(text, permutacio_inicial)

        # Desplaçar la permutació a l'esquerra
        permutacio_inicial = permutacio_inicial[1:] + permutacio_inicial[:1]
    
    return text

# Funció principal del programa
def main():
    nom_fitxer_entrada = input("Nom del fitxer d'entrada: ")
    nom_fitxer_sortida = input("Nom del fitxer de sortida: ")
    mode = input("Xifrat o desxifrat? (x/d): ")
    N = int(input("Nombre d'iteracions: "))
    permutacio_inicial = list(map(int, input("Introdueix la permutació inicial (separada per espais): ").split()))
    
    # Llegir el contingut del fitxer
    text = llegir_fitxer(nom_fitxer_entrada)

    # Processar segons el mode seleccionat
    if mode == 'x':  # Mode xifrat
        resultat = xifrar(text, N, permutacio_inicial)
        operacio = "Xifrat"
    elif mode == 'd':  # Mode desxifrat
        resultat = xifrar(text, N, permutacio_inicial)  # Placeholder per a desxifrat
        operacio = "Desxifrat"
    else:
        print("Mode no reconegut.")
        return

    # Escriure el resultat en el fitxer de sortida
    escriure_fitxer(nom_fitxer_sortida, resultat)
    print(f"{operacio} completat. El resultat s'ha guardat a {nom_fitxer_sortida}.")

if __name__ == "__main__":
    main()