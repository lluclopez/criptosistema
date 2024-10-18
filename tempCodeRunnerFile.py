fitxer_cs_iter = f"{nom_fitxer_sortida_sense_extensio}_c{i+1}.txt"
        if not os.path.exists(fitxer_cs_iter):
            print(f"No s'ha trobat el fitxer de valors de c ({fitxer_cs_iter}).")
            return
        resultat = desxifrar_subs(resultat, fitxer_cs_iter)