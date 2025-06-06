import random

with open("C:\\Users\DELL\\TP_PYTHON\\PROJET_PYTHON\TP1\\mot_de_passe_CrackMe.txt", "r") as fichier:
    mdp_faibles = [ligne.strip() for ligne in fichier if ligne.strip()]

mdp_random = random.choice(mdp_faibles)

nb_essais = 0
historique = []
mode_triche = False
proposition_triche = False

while True:
    tentative = input("essaye de devinez le mot de passe :")
    nb_essais += 1
    historique.append(tentative)

    if tentative == mdp_random:
        print("Super ! tu a trouvé le mot de passe.")
        print("Avec :", nb_essais, "essai")
        break
    else:
        # Partie indice
        if len(tentative) < len(mdp_random):
            print("le mot de passe est plus long.")
        elif len(tentative) > len(mdp_random):
            print("le mot de passe est plus court.")

        if tentative and tentative[0] == mdp_random[0]:
            print("le mot commence par la même lettre.")

        lettres_communes = 0
        for lettre in tentative:
            if lettre in mdp_random:
                lettres_communes += 1
        print(lettres_communes, "lettres communes avec le mot de passe.")

        
        if nb_essais == 3 and not mode_triche and not proposition_triche:
            activer_triche = input("Souhaitez-vous activer le mode triche ? (o/n) : ").lower()
            proposition_triche = True
            if activer_triche == "o":
                mode_triche = True
                print("Mot de passe (triche) :", mdp_random)


print("\nHistorique:")
for i, essai in enumerate(historique, start=1):
    print("Essai", i, ":", essai)
