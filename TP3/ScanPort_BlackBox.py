import socket
import argparse
import threading

def scan_port(ip, port, timeout, open_ports, verbose, lock):
    """
    Fonction qui tente de se connecter à un port spécifique sur une adresse IP donnée.
    Si le port est ouvert, il est ajouté à la liste des ports ouverts.
    Affiche le statut du port (ouvert/fermé) si le mode verbeux est activé.
    Utilise un verrou pour éviter les conflits lors de l'accès aux ressources partagées.
    """

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                with lock:
                    open_ports.append(port)
                if verbose:
                    print(f"Port {port} est OUVERT")
            elif verbose:
                print(f"Port {port} est FERMÉ")
    except socket.gaierror:
        with lock:
            print(f"Le nom d'hôte n'a pas pu être résolu : {ip}")
        return
    except socket.error as e:
        with lock:
            print(f"Impossible de se connecter au serveur {ip} : {e}")
        return

#<<<<<<< SEARCH
def main():
    """
    Fonction principale qui gère l'analyse des arguments en ligne de commande,
    lance le scan des ports sur la plage spécifiée en utilisant éventuellement plusieurs threads,
    affiche les résultats et les sauvegarde dans un fichier si demandé.
    """

    parser = argparse.ArgumentParser(description="Un simple scanner de ports TCP.")
    parser.add_argument("--ip", required=True, help="L'adresse IP à scanner.")
    parser.add_argument("--start-port", type=int, default=1, help="Le port de début pour le scan.")
    parser.add_argument("--end-port", type=int, default=1024, help="Le port de fin pour le scan.")
    parser.add_argument("--timeout", type=float, default=1.0, help="Délai d'attente du socket en secondes.")
    parser.add_argument("--verbose", action="store_true", help="Afficher également les ports fermés.")
    parser.add_argument("--output", help="Sauvegarder les résultats dans un fichier spécifié (ex: resultats.txt ou resultats.csv).")
    parser.add_argument("--threads", type=int, default=1, help="Nombre de threads à utiliser pour le scan.")

    args = parser.parse_args()

    ip_cible = args.ip
    port_debut = args.start_port
    port_fin = args.end_port
    delai_attente = args.timeout
    mode_verbeux = args.verbose
    fichier_sortie = args.output
    nombre_threads = args.threads

    # Vérification de la validité de la plage de ports
    if not (1 <= port_debut <= 65535 and 1 <= port_fin <= 65535 and port_debut <= port_fin):
        print("Plage de ports invalide. Les ports doivent être entre 1 et 65535, et le port de début doit être inférieur ou égal au port de fin.")
        return

    print(f"Scan des ports {port_debut}-{port_fin} sur {ip_cible}...")

    ports_ouverts = []
    verrou = threading.Lock()
    liste_threads = []

    # Lancement du scan des ports, en multithreading si demandé
    for port in range(port_debut, port_fin + 1):
        if nombre_threads > 1:
            thread = threading.Thread(target=scan_port, args=(ip_cible, port, delai_attente, ports_ouverts, mode_verbeux, verrou))
            liste_threads.append(thread)
            thread.start()
            
            # Limite le nombre de threads actifs pour ne pas dépasser le nombre demandé
            while threading.active_count() > nombre_threads:
                pass 
        else:
            # Scan séquentiel si un seul thread demandé
            scan_port(ip_cible, port, delai_attente, ports_ouverts, mode_verbeux, verrou)

    # Attente de la fin de tous les threads
    for thread in liste_threads:
        thread.join()

    # Affichage des ports ouverts trouvés
    if ports_ouverts:
        print("\nPorts ouverts trouvés :")
        for port in sorted(ports_ouverts):
            print(f"  Port {port}")
    else:
        print("\nAucun port ouvert trouvé dans la plage spécifiée.")

    # Sauvegarde des résultats dans un fichier si demandé
    if fichier_sortie:
        try:
            with open(fichier_sortie, 'w') as f:
                if fichier_sortie.lower().endswith('.csv'):
                    f.write("Port\n")
                    for port in sorted(ports_ouverts):
                        f.write(f"{port}\n")
                else:
                    f.write(f"Ports ouverts sur {ip_cible} ({port_debut}-{port_fin}):\n")
                    for port in sorted(ports_ouverts):
                        f.write(f"Port {port}\n")
            print(f"Résultats sauvegardés dans {fichier_sortie}")
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des résultats dans le fichier : {e}")

if __name__ == "__main__":
    main()
#=======
def main():
    """
    Fonction principale qui gère l'analyse des arguments en ligne de commande,
    lance le scan des ports sur la plage spécifiée en utilisant éventuellement plusieurs threads,
    affiche les résultats et les sauvegarde dans un fichier si demandé.
    """

    parser = argparse.ArgumentParser(description="Un simple scanner de ports TCP.")
    parser.add_argument("--ip", required=True, help="L'adresse IP à scanner.")
    parser.add_argument("--start-port", type=int, default=1, help="Le port de début pour le scan.")
    parser.add_argument("--end-port", type=int, default=1024, help="Le port de fin pour le scan.")
    parser.add_argument("--timeout", type=float, default=1.0, help="Délai d'attente du socket en secondes.")
    parser.add_argument("--verbose", action="store_true", help="Afficher également les ports fermés.")
    parser.add_argument("--output", help="Sauvegarder les résultats dans un fichier spécifié (ex: resultats.txt ou resultats.csv).")
    parser.add_argument("--threads", type=int, default=1, help="Nombre de threads à utiliser pour le scan.")

    args = parser.parse_args()

    ip_cible = args.ip
    port_debut = args.start_port
    port_fin = args.end_port
    delai_attente = args.timeout
    mode_verbeux = args.verbose
    fichier_sortie = args.output
    nombre_threads = args.threads

    # Vérification de la validité de la plage de ports
    if not (1 <= port_debut <= 65535 and 1 <= port_fin <= 65535 and port_debut <= port_fin):
        print("Plage de ports invalide. Les ports doivent être entre 1 et 65535, et le port de début doit être inférieur ou égal au port de fin.")
        return

    print(f"Scan des ports {port_debut}-{port_fin} sur {ip_cible}...")

    ports_ouverts = []
    verrou = threading.Lock()
    liste_threads = []

    # Lancement du scan des ports, en multithreading si demandé
    for port in range(port_debut, port_fin + 1):
        if nombre_threads > 1:
            thread = threading.Thread(target=scan_port, args=(ip_cible, port, delai_attente, ports_ouverts, mode_verbeux, verrou))
            liste_threads.append(thread)
            thread.start()
            
            # Limite le nombre de threads actifs pour ne pas dépasser le nombre demandé
            while threading.active_count() > nombre_threads:
                pass 
        else:
            # Scan séquentiel si un seul thread demandé
            scan_port(ip_cible, port, delai_attente, ports_ouverts, mode_verbeux, verrou)

    # Attente de la fin de tous les threads
    for thread in liste_threads:
        thread.join()

    # Affichage des ports ouverts trouvés
    if ports_ouverts:
        print("\nPorts ouverts trouvés :")
        for port in sorted(ports_ouverts):
            print(f"  Port {port}")
    else:
        print("\nAucun port ouvert trouvé dans la plage spécifiée.")

    # Sauvegarde des résultats dans un fichier si demandé
    if fichier_sortie:
        try:
            with open(fichier_sortie, 'w') as f:
                if fichier_sortie.lower().endswith('.csv'):
                    f.write("Port\n")
                    for port in sorted(ports_ouverts):
                        f.write(f"{port}\n")
                else:
                    f.write(f"Ports ouverts sur {ip_cible} ({port_debut}-{port_fin}):\n")
                    for port in sorted(ports_ouverts):
                        f.write(f"Port {port}\n")
            print(f"Résultats sauvegardés dans {fichier_sortie}")
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des résultats dans le fichier : {e}")

if __name__ == "__main__":
    main()
