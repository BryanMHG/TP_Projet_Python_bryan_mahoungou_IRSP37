import random


mdp_faibles = ["123456", "password", "admin", "123456789","qwerty", "abc123", "letmein", "welcome","monkey", "football"]

mdp_random = random.choice(mdp_faibles)

nb_essais = 0

while True:
    tentative = input("essaye de devinez le mot de passe : ")
    nb_essais += 1

    if tentative == mdp_random:
        print("Super ! tu a trouvé le mot de passe.")
        print("Avec:", nb_essais, "essai")
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
        print(lettres_communes, "lettres communes avec le mot de passe a trouver.")
