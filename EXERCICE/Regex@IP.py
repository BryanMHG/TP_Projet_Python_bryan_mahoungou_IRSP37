# import re


# regex = r'^((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$'

# def ip_valide(ip):
#     return re.match(regex, ip) is not None

# def demander_ip():
#     while True:
#         ip = input("Veuillez entrer une adresse IP (IPv4) : ")
#         if ip_valide(ip):
#             print(f"L'adresse IP '{ip}' est valide.")
#             break
#         else:
#             print(f"'{ip}' n'est pas une adresse IP valide. Veuillez réessayer.\n")

# if __name__ == "__main__":
#     demander_ip()

import re


regex = r'^((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$'


def ip_valide(ip):
    return re.match(regex, ip) is not None


nom_fichier = "C:\\Users\\DELL\\TP_PYTHON\\PROJET_PYTHON\\EXERCICE\\@IP.txt"

try:
    with open(nom_fichier, "r") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            ip = ligne.strip()  
            if ip_valide(ip):
                print(f"{ip} : Valide")
            else:
                print(f"{ip} : Invalide")
except FileNotFoundError:
    print(f"Fichier introuvable : {nom_fichier}")
