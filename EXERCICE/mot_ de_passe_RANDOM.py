import string 

# Caractères ambigus à éviter
ambiguous_chars = {'I', 'l', '1', 'O'}

while True:
    MDP = input("Saisir votre mot de passe : ")

    # Vérifie la longueur
    if len(MDP) < 12:
        print("Votre mot de passe doit contenir au minimum 12 caractères.")
        continue

    # initialisation des caractéristiques du mot de passe
    Majus = 0
    Minus = 0
    Chiffres = 0
    Cara_spe = 0
    Ambigu = 0

    # Parcours du mot de passe caractère par caractère
    for char in MDP:
        if char in ambiguous_chars:
            Ambigu += 1
        elif char.isupper():
            Majus += 1
        elif char.islower():
            Minus += 1
        elif char.isdigit():
            Chiffres += 1
        elif char in string.punctuation:
            Cara_spe += 1

    # Vérification des conditions
    if Majus == 0:
        print("Le mot de passe doit contenir au moins une majuscule.")
        continue
    if Minus == 0:
        print("Le mot de passe doit contenir au moins une minuscule.")
        continue
    if Chiffres == 0:
        print("Le mot de passe doit contenir au moins un chiffre.")
        continue
    if Cara_spe == 0:
        print("Le mot de passe doit contenir au moins un caractère spécial.")
        continue
    if Ambigu > 0:
        print("Le mot de passe contient un caractère ambigu (comme I, l, 1, O, 0).")
        continue

    # Si toutes les vérifications sont passées
    print("Mot de passe accepté.")
    print("Mot de passe :", MDP)
    break
