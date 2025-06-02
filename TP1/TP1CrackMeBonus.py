import random

with open("C:\\Users\\DELL\\Documents\\mot_de_passe_CrackMe.txt", "r") as fichier:
    mots_de_passe_faibles = [ligne.strip() for ligne in fichier if ligne.strip()]

mdp_random = random.choice(mots_de_passe_faibles)

nb_essais = 0
historique = []
mode_triche = False
triche_proposee = False

while True:
    tentative = input("Devinez le mot de passe : ")
    nb_essais += 1
    historique.append(tentative)

    if tentative == mdp_random:
        print("Super ! Vous avez trouvé le mot de passe.")
        print("Avec :", nb_essais, "essai")
        break
    else:
        # Partie indice
        if len(tentative) < len(mdp_random):
            print("Indice : le mot de passe est plus long.")
        elif len(tentative) > len(mdp_random):
            print("Indice : le mot de passe est plus court.")

        if tentative and tentative[0] == mdp_random[0]:
            print("Indice : le mot commence par la même lettre.")

        lettres_communes = 0
        for lettre in tentative:
            if lettre in mdp_random:
                lettres_communes += 1
        print("Indice :", lettres_communes, "lettres communes avec le mot de passe.")

        
        if nb_essais == 3 and not mode_triche and not triche_proposee:
            activer_triche = input("Souhaitez-vous activer le mode triche ? (o/n) : ").lower()
            triche_proposee = True
            if activer_triche == "o":
                mode_triche = True
                print("Mot de passe (triche) :", mdp_random)


print("\nHistorique des tentatives :")
for i, essai in enumerate(historique, start=1):
    print("Essai numéro", i, ":", essai)
