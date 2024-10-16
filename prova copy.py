import math

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
    with open(nom_fitxer, 'w') as f:
        f.write(contingut)

# Funció per llegir d'un fitxer
def llegir_fitxer(nom_fitxer):
    with open(nom_fitxer, 'r') as f:
        return f.read()

# Funció per xifrar el text i guardar els valors de 'c'
def xifrar_subs(text, fitxer_cs):
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
def desxifrar_subs(text, fitxer_cs):
    cs = llegir_fitxer(fitxer_cs).split()
    paraules = text.split()
    resultat = []
    for idx, paraula in enumerate(paraules):
        if paraula and idx < len(cs):
            c = int(cs[idx])
            resultat.append(desxifrar_paraula(paraula, c))
    return ' '.join(resultat)

# Funció de transposició
def transposar(text, permutacio):
    K = len(permutacio)
    matriu = [list(text[i:i + K]) for i in range(0, len(text), K)]
    if len(matriu[-1]) < K:
        matriu[-1].extend([' '] * (K - len(matriu[-1])))
    resultat = []
    for col in permutacio:
        for fila in matriu:
            resultat.append(fila[col - 1])  # -1 perquè la permutació està basada en 1
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
    # Demanar el text a xifrar
    text = input("Introdueix el text: ")  # Mantindrem els espais en el text
    N = int(input("Introdueix el nombre d'iteracions: "))
    
    # Demanar la permutació inicial
    permutacio_inicial = list(map(int, input("Introdueix la permutació inicial (separada per espais): ").split()))
    
    # Fitxer on es guardaran els valors de 'c' per la substitució
    fitxer_cs = "valors_cs.txt"
    
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
    
    # Preguntar si es vol desxifrar
    desxifrar = input("\nVols desxifrar el text? (s/n): ").lower() == 's'
    
    if desxifrar:
        permutacio = permutacio_inicial[:]
        for i in range(N-1):
            permutacio = permutacio[1:] + permutacio[:1]
        for i in reversed(range(N)):
            print(f"\nIteració {N-i} (Desxifrant) - Permutació: {permutacio}")
            resultat = destransposar(resultat, permutacio)
            print(f"Text desxifrat després de la iteració {N-i}: {resultat}")
            permutacio = permutacio[-1:] + permutacio[:-1]
        
        # Desxifrat per substitució
        resultat = desxifrar_subs(resultat, fitxer_cs)
        print(f"\nText després de desxifrar per substitució: {resultat}")
    
    print(f"\nText final: {resultat}")

if __name__ == "__main__":
    main()
