import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gestionnaire.gestion import gestionnaire,confNeuron

conf = confNeuron(name="Opale",
                  lang="fr",
                  icon="asset/icon.png",
                  asset="asset/",
                  bute="developper un algo de ChatBot qui sera inclut dans SIX et Ryley",
                  createur="Pauchet Baptiste",
                  listFonction=["ouvrir une application", "aider sur les recherches de internet", "donner la meteo",
                                "faire un résumer des actualités"],
                  moteurderecherche="google",
                  etatService=1,
                  etatTime=1,
                  etatOpen=1,
                  etatSearch=1,
                  etatChatbot=1,
                  etatApi=1,
                  etatCodehelp=1,
                  etatWork=1,
                  etatSocket=1,
                  lienDoc="www.google.com",
                  fichierLangue="language/vouvoiment/",
                  fichierKeyword="keyword/",
                  voiceAssistant=True)

gest = gestionnaire(conf)
user = gest.getUserConf()



def main():
    boucle= True
    while boucle :
        print("_____________________________________________________")
        print("1.USER\n"
              "2.Genre\n"
              "3.Domicile\n"
              "4.Travail\n"
              "5.LOGICIEL\n"
              "6.Site Internet\n"
              "7.Moteur de recherche\n"
              "8.Token github\n"
              "9.Dossier de travail\n"
              "10.Dossier video\n"
              "11.Sound Micro\n"
              "12.Tiger Word\n"
              "13.Historique\n"
              "14.IA\n"
              "15.Voice\n"
              "0.Quitter")

        print("_____________________________________________________")
        boucleVerif = True
        while boucleVerif:
            nb = input("Choix : ")
            try:
                nb = int(nb)
                boucleVerif = False
            except ValueError:
                print("Veuillez entrer un nombre valide.")

        match nb :
            case 0 :
                print("Au revoir !")
                boucle = False
            case 1:
                print("1.Prenom\n2.Nom de famille\n3.Lire")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        prenom = input("Prenom : ")
                        user.setFirstnameUser(prenom)
                    case 2:
                        nom = input("Nom : ")
                        user.setLastnameUser(nom)
                    case 3:
                        print(f"Prenom : {user.getFirstnameUser()}\nNom : {user.getLastnameUser()}")
            case 2:
                print("1.Ajouter\n2.Lire")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        genre = input("Genre : ")
                        user.setGenre(genre)
                    case 2:
                        print(user.getGenre())
            case 3 :
                print("1.Ajouter\n2.Adresse complette\n3.Ville\n4.Code postal\n5.Adresse")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        adress = input("adresse: ")
                        cp = input("Code Postal: ")
                        town = input("Ville: ")
                        if user.set_home_adresse(adress, cp, town):
                            print("Ajouter")
                        else:
                            print("Erreur")
                    case 2:
                        print(user.get_full_adress_home())
                    case 3:
                        print(user.get_town_home())
                    case 4:
                        print(user.get_postal_home())
                    case 5 :
                        print(user.get_adresse_home())
            case 4:
                print("1.Ajouter\n2.Adresse complette\n3.Ville\n4.Code postal\n5.Adresse")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        adress = input("adresse: ")
                        cp = input("Code Postal: ")
                        town = input("Ville: ")
                        if user.set_work_adresse(adress, cp, town):
                            print("Ajouter")
                        else :
                            print("Erreur")
                    case 2:
                        print(user.get_full_adress_work())
                    case 3:
                        print(user.get_town_work())
                    case 4:
                        print(user.get_postal_work())
                    case 5 :
                        print(user.get_adresse_work())
            case 5:
                print("1.Ajouter\n2.Voir\n3.Supprimer")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        logiciel = input("Nom du logiciel : ")
                        path = input("Chemin du logiciel : ")
                        if user.setSoft(logiciel, path):
                            print("Logiciel ajouté avec succès.")
                        else:
                            print("Erreur lors de l'ajout du logiciel ou le logiciel existe déjà.")
                    case 2:
                        print(user.getSoft())
                    case 3:
                        logiciel = input("Nom du logiciel à supprimer : ")
                        if user.removeSoft(logiciel):
                            print("Logiciel supprimé avec succès.")
                        else:
                            print("Erreur lors de la suppression du logiciel ou le logiciel n'existe pas.")
            case 6:
                print("1.Ajouter\n2.Lire\n3.Supprimer")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        site = input("Nom Site Internet : ")
                        url = input("URL du site : ")
                        if user.setSite(site, url):
                            print("Site ajouté avec succès.")
                        else:
                            print("Erreur lors de l'ajout du site ou le site existe déjà.")
                    case 2:
                        print(user.getSite())
                    case 3:
                        site = input("Site Internet : ")
                        if user.removeSite(site):
                            print("Site supprimé avec succès.")
                        else:
                            print("Erreur lors de la suppression du site.")
            case 7:
                print("1.Ajouter\n2.Lire")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        moteur = input("Moteur de recherche : ")
                        user.setMoteurRecherche(moteur)
                    case 2:
                        print(user.getMoteurRecherche())
            case 8:
                print("1.Ajouter\n2.Lire")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        token = input("Token Github : ")
                        if user.setTokenGithub(token):
                            print("Token ajouté avec succès.")
                        else:
                            print("Erreur lors de l'ajout du token ou le token existe déjà.")
                    case 2:
                        print(user.getTokenGithub())
            case 9:
                print("1.Ajouter\n2.Lire\n3.Supprimer")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        folder = input("Chemin du dossier de travail : ")
                        if user.setWorkFolder(folder):
                            print("Dossier ajouté avec succès.")
                        else:
                            print("Erreur lors de l'ajout du dossier ou le dossier existe déjà.")
                    case 2:
                        print(user.getWorkFolder())
                    case 3:
                        if user.removeWorkFolder():
                            print("Dossier supprimé avec succès.")
                        else:
                            print("Erreur lors de la suppression du dossier.")
            case 10:
                print("1.Ajouter\n2.Lire\n3.Supprimer")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        folder = input("Chemin du dossier video : ")
                        if user.setVideoDownloadFolder(folder):
                            print("Dossier ajouté avec succès.")
                        else:
                            print("Erreur lors de l'ajout du dossier ou le dossier existe déjà.")
                    case 2:
                        print(user.getVideoDownloadFolder())
                    case 3:
                        if user.removeVideoDownloadFolder():
                            print("Dossier supprimé avec succès.")
                        else:
                            print("Erreur lors de la suppression du dossier.")
            case 11:
                print("1.Activer\n2.Desactiver\n3.Voir")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        if user.setSoundMicro(True):
                            print("Micro activé avec succès.")
                        else:
                            print("Erreur lors de l'activation du micro.")
                    case 2:
                        if user.setSoundMicro(False):
                            print("Micro désactivé avec succès.")
                        else:
                            print("Erreur lors de la désactivation du micro.")
                    case 3:
                        print(user.getSoundMicro())
            case 12:
                print("1.Ajouter\n2.Lire\n3.Supprimer")
                boucleVerif = True
                while boucleVerif:
                    nb = input("Choix : ")
                    try:
                        nb = int(nb)
                        boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                match nb:
                    case 1:
                        word = input("Mot à ajouter : ")
                        if user.addWord(word):
                            print("Mot ajouté avec succès.")
                        else:
                            print("Erreur lors de l'ajout du mot ou le mot existe déjà.")
                    case 2:
                        print(user.getListWord())
                    case 3:
                        word = input("Mot à supprimer : ")
                        if user.removeWord(word):
                            print("Mot supprimé avec succès.")
                        else:
                            print("Erreur lors de la suppression du mot ou le mot n'existe pas.")
            case 13 :
                print("Historique")
                print(f"Etat de l'hitorique : {user.getHist()}")
                out = input("1. Activer\n2. Desactiver\n0. Rien faire\nChoix : ")
                match out:
                    case "1":
                        user.setHist(True)
                    case "2":
                        user.setHist(False)
                    case "0":
                        pass
            case 14 :
                print("IA")
                out = input("1. Voir le model actif\n"
                            "2. Choisir le model\n"
                            "3. Download un model du catalogue\n"
                            "4. Voir les model telecharger\n"
                            "5. Modele dans le dossier\n"
                            "6. Supprimer un modele\n"
                            "7. Voir le catalogue complet (9 modèles + descriptions)\n"
                            "8. Voir la recommandation matérielle (meilleur modèle pour ce PC)\n"
                            "9. Télécharger un modèle personnalisé (lien direct .gguf)\n"
                            "0. Rien faire\n"
                            "Choix : ")
                match out:
                    case "1":
                        print(f"Modèle actif : {user.get_ia_model()}")
                    case "2":
                        model = input("Model : ")
                        user.set_ia_model(model)
                    case "3":
                        print("Model disponible")
                        d = user.get_model_downloaded()
                        for m in user.get_list_model_ia_available():
                            if m not in d:
                                print(f"-{m}")
                        model = input("Model : ")
                        user.download_ia_model(model)
                    case "4":
                        print("Model telecharger")
                        print(user.get_model_downloaded())
                    case "5":
                        print("Model dans le dossier")
                        print(user.get_model_ia_on_directory())
                    case "6" :
                        model = input("Model a supprimer : ")
                        if user.del_ia_model(model):
                            print("Model supprimer")
                        else :
                            print("Impossible de supprimer le model")
                    case "7":
                        print("\n--- Catalogue officiel des modèles IA ---")
                        for m in user.get_list_model_ia_available():
                            name_m, url_m, desc_m = user.get_data_model_ia_available(m)
                            print(f"- [{m}] {name_m} : {desc_m}")
                    case "8":
                        hw = user.get_hardware_ia_recommendation()
                        print("\n--- Recommandation matérielle ---")
                        print(f"Catégorie PC        : {hw.get('category')}")
                        print(f"RAM détectée        : {hw.get('ram_gb')} Go")
                        print(f"VRAM GPU détectée   : {hw.get('vram_gb')} Go")
                        print(f"Coeurs CPU          : {hw.get('cpu_cores')}")
                        print(f"Modèle recommandé   : {user.get_recommended_ia_model()}")
                        print(f"Modèles compatibles : {hw.get('compatible_models')}")
                    case "9":
                        name = input("Nom du modèle personnalisé (ex: mon-modele) : ")
                        url = input("Lien direct .gguf (ou lien HuggingFace) : ")
                        desc = input("Description (optionnel) : ")
                        print("Téléchargement et vérification GGUF en cours...")
                        if user.download_custom_ia_model(name, url, desc):
                            print("Téléchargement terminé avec succès ! Modèles téléchargés :", user.get_model_downloaded())
                        else:
                            print("Erreur : impossible de télécharger le modèle (vérifiez le nom et le lien .gguf).")
                    case "0":
                        pass

            case 15 :
                print("Voice")
                out = input("1. Voir les models\n"
                            "2. Choisir le model\n"
                            "3. Voir le model selectionner\n"
                            "Choix : ")
                match out:
                    case "1":
                        text = "Modele de voix disponible :\n"
                        for l in user.get_list_voice_available():
                            text += f"- {l}\n"
                        print(text)
                    case "2":
                        text = "Modele de voix disponible :\n"
                        for l in user.get_list_voice_available():
                            text += f"- {l}\n"
                        print(text)
                        model = input("Choisir le model : ")
                        if user.set_voice(model):
                            print("Modele ajouter")
                        else :
                            print("Impossible de modifier le model")
                    case "3":
                        print(f"Voix selectionner :{user.get_voice_selected()}")

            case _:
                print("Erreur, veuillez choisir un nombre entre 0 et 14.")

if __name__ == "__main__":
    main()