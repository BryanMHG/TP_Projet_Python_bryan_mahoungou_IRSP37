import re
from collections import Counter
import matplotlib.pyplot as plt  

fichier_log = "C:\\Users\\DELL\\TP_PYTHON\\PROJET_PYTHON\\TP2\\auth.log" 

def analysation_fichier_log(fichier_log):

    lignes_erreurs = []
    adresses_IPs = []

    try:
        with open(fichier_log, 'r') as f:
            for ligne in f:
                if "Failed password" in ligne:
                    lignes_erreurs.append(ligne)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fichier_log}' est introuvable.")
        return None

    pattern_IP = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    for ligne in lignes_erreurs:
        correspondance = pattern_IP.search(ligne)
        if correspondance:
            adresses_IPs.append(correspondance.group(0))

    compteur_ips = Counter(adresses_IPs)
    top_5_ips = compteur_ips.most_common(5)

    return top_5_ips

def visualisation_top_ips(top_ips):
    ips, nb_echecs = zip(*top_ips)
    plt.figure(figsize=(10, 6))
    plt.bar(ips, nb_echecs)
    plt.xlabel("Adresses IP")
    plt.ylabel("Nombre de tentatives échouées")
    plt.title("Top 5 des IPs ayant le plus d'échecs de connexion")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    top_ips = analysation_fichier_log(fichier_log)

    if top_ips:
        print("Les 5 adresses IP avec le plus grand nombre de tentatives de connexion échouées :")
        for ip, nb in top_ips:
            print(f"{ip} : {nb} échecs")
        
        visualisation_top_ips(top_ips)
