from librairy.PArreraServer import PArreraServer

if __name__ == "__main__":
    mon_serveur = PArreraServer(port=6780)
    mon_serveur.start()

    import time

    time.sleep(2)

    print("\n==========================================")
    print("   SERVEUR ARRERA - CONSOLE DE TEST")
    print("==========================================")
    print("Instructions :")
    print("- Connectez vos applications sur le port 6780.")
    print("- Elles doivent envoyer 'namesoft [NOM]' au début.")
    print("==========================================\n")

    try:
        while True:
            # On affiche la liste des logiciels actuellement connectés
            apps_connectees = list(mon_serveur.clients.keys())

            if not apps_connectees:
                print("En attente de connexion d'une application...")
                time.sleep(3)
                continue

            print(f"\nApplications en ligne : {apps_connectees}")

            # 2. Choix de la cible
            cible = input("Envoyer à (nom du logiciel ou 'all' pour tout le monde) : ").strip()

            # 3. Saisie du message
            message = input(f"Message pour {cible} : ")

            # 4. Envoi ciblé ou global
            if cible.lower() == 'all':
                mon_serveur.broadcast(message)
            else:
                mon_serveur.sendTo(cible, message)

    except KeyboardInterrupt:
        print("\nArrêt du serveur de test.")