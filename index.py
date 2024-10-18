import string

def llegir_fitxer(nom_fitxer):
    """Llegeix el contingut d'un fitxer i el retorna com a una cadena."""
    with open(nom_fitxer, 'r', encoding='utf-8') as f:
        return f.read()

def netejar_text(text):
    """Converteix el text a majúscules i elimina caràcters no alfabètics."""
    text = text.upper()
    return ''.join([car for car in text if car in string.ascii_uppercase])

def calcular_frequencies(text):
    """Calcula les freqüències de cada lletra en el text."""
    frequencies = {lletra: 0 for lletra in string.ascii_uppercase}
    for car in text:
        if car in frequencies:
            frequencies[car] += 1
    return frequencies

def index_coincidencia(text):
    """Calcula l'índex de coincidència normalitzat."""
    n = len(text)
    if n <= 1:
        return 0  # Evitem divisió per zero si el text és massa curt

    frequencies = calcular_frequencies(text)
    numerador = sum(freq * (freq - 1) for freq in frequencies.values())
    denominador = n * (n - 1)
    
    return numerador / denominador

# Exemple d'ús
nom_fitxer = "text.txt"  # Substitueix pel nom del teu fitxer
text = llegir_fitxer(nom_fitxer)
text_net = netejar_text(text)
index = index_coincidencia(text_net)

print(f"L'índex de coincidència és: {index:.4f}")