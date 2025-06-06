import pandas as pd
import matplotlib.pyplot as plt
import re

# --- Configuration ---
CHEMIN_FICHIER_LOG = r"C:\Users\DELL\TP_PYTHON\PROJET_PYTHON\TP4\access - Copie.txt" # N'oubliez pas de mettre le bon nom de fichier

# --- 1. Chargement et analyse du fichier ---
def charger_et_analyser_logs(chemin_fichier_log):
    """
    Charge le fichier access.log et analyse les lignes pour extraire les informations.
    """
    donnees_logs = []
    # Nouvelle expression régulière pour s'adapter à votre format de log
    # Elle gère l'absence du champ de taille et l'optionnalité du champ referrer
    motif_log = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] "(.*?) (.*?) HTTP/\d\.\d" (\d{3})(?: "(.*?)"| -)? "(.*?)"')

    with open(chemin_fichier_log, 'r') as f:
        for i, ligne in enumerate(f):
            match = motif_log.match(ligne)
            if match:
                try:
                    ip = match.group(1)
                    date_heure_str = match.group(2)
                    methode = match.group(3)
                    url = match.group(4)
                    statut = int(match.group(5))
                    # Le groupe 6 peut être le referrer ou None.
                    # Le groupe 7 est l'user_agent
                    # Pour s'assurer, nous allons capturer l'avant-dernier et le dernier groupe.
                    # On vérifie la longueur de match.groups() pour déterminer les indices
                    
                    groupes_captures = match.groups()
                    
                    # Le user_agent est toujours le dernier groupe capturé par la regex
                    agent_utilisateur = groupes_captures[-1]
                    
                    # Le référent est l'avant-dernier groupe, mais il peut être None ou vide si non présent
                    # Nous l'initialisons à une chaîne vide si ce n'est pas le cas.
                    referent = groupes_captures[-2] if len(groupes_captures) > 6 and groupes_captures[-2] is not None else ""


                    donnees_logs.append({
                        'ip': ip,
                        'datetime': pd.to_datetime(date_heure_str, format='%d/%b/%Y:%H:%M:%S %z', errors='coerce'),
                        'methode': methode,
                        'url': url,
                        'statut': statut,
                        'agent_utilisateur': agent_utilisateur,
                        'referent': referent # Ajout du référent, même s'il n'est pas utilisé pour le TP principal
                    })
                except ValueError as e:
                    print(f"Erreur de conversion de statut sur la ligne {i+1}: {ligne.strip()} - {e}")
                    continue
                except IndexError as e:
                    print(f"Erreur d'indexation de groupe sur la ligne {i+1}: {ligne.strip()} - {e}. Groupes capturés: {match.groups()}")
                    continue
            else:
                # Ceci affichera les lignes qui ne correspondent pas du tout au motif
                # Dans votre cas, la ligne "bad_line_without_any_formatting" sera affichée ici.
                print(f"Ligne {i+1} malformée ou non correspondante (ignorée): {ligne.strip()}")
                pass

    df_logs = pd.DataFrame(donnees_logs)
    # Assurez-vous que la colonne 'datetime' existe et n'est pas remplie de NaT (Not a Time)
    df_logs.dropna(subset=['datetime'], inplace=True)
    return df_logs

# --- 2. Filtrage des erreurs 404 ---
def filtrer_erreurs_404(df_logs):
    """
    Isole les lignes où le statut est 404.
    """
    return df_logs[df_logs['statut'] == 404]

# --- 3. Top 5 des IPs fautives ---
def obtenir_top_5_ips(df_erreurs_404):
    """
    Groupe par IP, compte et trie pour afficher les 5 IPs générant le plus d'erreurs 404.
    """
    top_ips = df_erreurs_404['ip'].value_counts().nlargest(5)
    return top_ips

# --- 4. Visualisation ---
def visualiser_top_ips(top_ips):
    """
    Crée un histogramme (diagramme à barres) avec matplotlib des top IPs fautives.
    """
    plt.figure(figsize=(10, 6))
    top_ips.plot(kind='bar', color='skyblue')
    plt.title('Top 5 des IPs générant des erreurs 404')
    plt.xlabel('Adresses IP')
    plt.ylabel("Nombre d'erreurs 404")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# --- Bonus: Détection de bots ---
def detecter_bots(df_erreurs_404):
    """
    Détecte les erreurs 404 provenant de bots et calcule leur pourcentage.
    """
    motifs_bots = ["bot", "crawler", "spider"]
    # Créer une expression régulière unique pour la recherche insensible à la casse
    regex_bots = "|".join(motifs_bots)

    # Filtrer les lignes dont l'agent_utilisateur contient des motifs de bot
    df_bots_404 = df_erreurs_404[df_erreurs_404['agent_utilisateur'].str.contains(regex_bots, case=False, na=False)]

    # Identifier les IPs suspectes de bots (celles qui ont généré des erreurs 404 et sont des bots)
    ips_suspectes_bots = df_bots_404['ip'].unique()

    total_erreurs_404 = len(df_erreurs_404)
    erreurs_404_bots = len(df_bots_404)

    pourcentage_erreurs_bots = (erreurs_404_bots / total_erreurs_404) * 100 if total_erreurs_404 > 0 else 0

    return df_bots_404, ips_suspectes_bots, pourcentage_erreurs_bots

# --- Fonction principale du script ---
def principale():
    print("--- Démarrage de l'analyse des logs Apache ---")

    # 1. Chargement et analyse du fichier
    print(f"Chargement et analyse du fichier log: {CHEMIN_FICHIER_LOG}...")
    df_principal = charger_et_analyser_logs(CHEMIN_FICHIER_LOG)
    print(f"Nombre total de requêtes chargées: {len(df_principal)}")
    print("\nAperçu des données chargées (head()):")
    print(df_principal.head())

    # 2. Filtrage des erreurs 404
    print("\nFiltrage des erreurs 404...")
    df_erreurs_404 = filtrer_erreurs_404(df_principal)
    print(f"Nombre d'erreurs 404 trouvées: {len(df_erreurs_404)}")
    print("\nAperçu des erreurs 404 (head()):")
    print(df_erreurs_404.head())

    # 3. Top 5 des IPs fautives
    print("\nCalcul du Top 5 des IPs générant des erreurs 404...")
    top_5_ips = obtenir_top_5_ips(df_erreurs_404)
    print("\nTop 5 des IPs fautives:")
    print(top_5_ips)

    # 4. Visualisation
    print("\nGénération du graphique des Top 5 IPs...")
    visualiser_top_ips(top_5_ips)
    print("Graphique généré (fermez la fenêtre du graphique pour continuer).")

    # Bonus: Détection de bots
    print("\n--- Détection de bots (Bonus) ---")
    df_bots_404, ips_suspectes_bots, pourcentage_erreurs_bots = detecter_bots(df_erreurs_404)
    if not df_bots_404.empty:
        print(f"Nombre d'erreurs 404 attribuées à des bots: {len(df_bots_404)}")
        print(f"Pourcentage d'erreurs 404 provenant de bots: {pourcentage_erreurs_bots:.2f}%")
        print("Aperçu des erreurs 404 de bots (head()):")
        print(df_bots_404.head())
        print("IPs suspectes (bots) ayant généré des erreurs 404:")
        for ip in ips_suspectes_bots:
            print(f"- {ip}")
    else:
        print("Aucune erreur 404 attribuée à des bots trouvée.")

    # Discussion des résultats
    print("\n--- Discussion des résultats ---")
    print("Conclusions possibles :")
    print("- L'analyse a permis d'identifier les adresses IP les plus actives dans la génération d'erreurs 404. Ces IPs peuvent indiquer des tentatives d'accès à des ressources inexistantes, des scans de vulnérabilité, ou des erreurs de configuration.")
    print("- Le pourcentage d'erreurs 404 provenant de bots est un indicateur important. Un pourcentage élevé peut signifier que votre site est la cible de crawlers malveillants ou de tentatives d'exploitation.")
    print("\nCes IPs doivent-elles être bannies ?")
    print("- Le bannissement d'IP est une action drastique. Il est recommandé d'analyser la nature des requêtes (URLs tentées, user-agent) avant de bannir. Si les IPs sont clairement associées à des activités malveillantes (scans de ports, tentatives d'injection), le bannissement via un pare-feu (ex: iptables, fail2ban) ou le fichier .htaccess peut être envisagé.")
    print("- Pour les bots légitimes (moteurs de recherche), un blocage pourrait nuire au référencement. Il faut être vigilant.")
    print("\nPeut-on automatiser ce type de détection ?")
    print("- Oui, absolument. Des outils comme Fail2ban surveillent les logs en temps réel et peuvent automatiquement bloquer les IPs après un certain nombre de tentatives infructueuses (comme des 404 répétées).")
    print("- Des scripts Python comme celui-ci peuvent être planifiés (via cron jobs sur Linux, Tâches planifiées sur Windows) pour générer des rapports réguliers ou déclencher des alertes.")
    print("- L'intégration avec des systèmes de SIEM (Security Information and Event Management) permet une analyse plus poussée et une corrélation d'événements à grande échelle.")
    print("\n--- Fin de l'analyse ---")

if __name__ == "__main__":
    principale()