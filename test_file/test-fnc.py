import datetime
from gestionnaire.gestion import gestionnaire
from config.confNeuron import confNeuron

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
print("Chargement de l'IA...")
gest.getGestIA().loadIA()
fnc = gest.getGestFNC()

def partTask():
    taskBoucle = True
    while taskBoucle:
        print("Test des fonctions de tache")
        print("1.Ajouter une tache\n2.Lister les taches non fini\n"
              "3.Supprimer une tache\n4.Compter le nombre de taches non fini\n"
              "5.finir une tache\n6.Check date today\n7.Tache a faire aujourd'hui\n"
              "8.Check date towmorow\n9.Tache a faire demain\n"
              "10.Check task late\n11.Tache en retard"
              "\n12.Voir les taches fini\n13.Compter le nombre de taches fini"
              "\n14.Voir toutes les taches\n15.Compter le nombre total de taches"
              "\n16.Remettre une tache a faire\n0.Quitter")
        print("__________________________\n")
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
                title = input("Titre de la tache : ")
                date = input("Date de la tache (YYYY-MM-DD) : ")
                try:
                    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                    description = input("Description de la tache : ")
                    print(fnc.getFNCTask().addTask(title, date, description))
                except ValueError:
                    print("Format de date invalide. Utilisez YYYY-MM-DD.")
            case 2:
                print(f"Tache non fini : {fnc.getFNCTask().getNoFinishTask()}")
            case 3:
                taskId = input("Name : ")
                sortie = fnc.getFNCTask().delTask(taskId)
                if sortie:
                    print("Tache supprimer")
                else:
                    print("Erreur")
            case 4:
                print(f"Nombre de taches non fini : {fnc.getFNCTask().getNbTaskNoFinish()}")
            case 5:
                taskId = input("Name : ")
                sortie = fnc.getFNCTask().finishTask(taskId)
                if sortie:
                    print("Tache terminer")
                else:
                    print("Erreur")
            case 6:
                taskId = input("Name : ")
                print(fnc.getFNCTask().checkDateTask(taskId))
            case 7:
                print(fnc.getFNCTask().getNbTaskToday())
                print(fnc.getFNCTask().getListTaskToday())
            case 8:
                taskId = input("Name : ")
                print(fnc.getFNCTask().checkDateTaskTowmorow(taskId))
            case 9:
                print(fnc.getFNCTask().getNbTaskTowmorow())
                print(fnc.getFNCTask().getListTaskTowmorow())
            case 10:
                taskId = input("Name : ")
                print(fnc.getFNCTask().checkTaskLate(taskId))
            case 11:
                print(fnc.getFNCTask().getNbTaskLate())
                print(fnc.getFNCTask().getListTaskLate())
            case 12:
                print(f"Tache fini : {fnc.getFNCTask().getFinishTask()}")
            case 13:
                print(f"Nombre de taches fini : {fnc.getFNCTask().getNbTaskFinish()}")
            case 14:
                print(f"Toutes les taches : {fnc.getFNCTask().getAllTask()}")
            case 15:
                print(f"Nombre total de taches : {fnc.getFNCTask().getNbAllTask()}")
            case 16:
                taskId = input("Name : ")
                sortie = fnc.getFNCTask().unfinishTask(taskId)
                if sortie:
                    print("Tache non terminer")
                else:
                    print("Erreur")

            case 0:
                taskBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partSearch():
    searchBoucle = True
    while searchBoucle:
        print("Test des fonctions de recherche")
        print("1.Recherche Ecosia\n2.Recherche Bing\n3.Recherche Perplexity\n4.Recherche Google\n5.Recherche Qwant\n6.Recherche DuckDuckGo\n7.Recherche Big\n8.Recherche assistant\n0.Quitter")
        print("__________________________\n")
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
                query = input("Rechercher : ")
                fnc.getFNCSearch().ecosiaSearch(query)
            case 2:
                query = input("Rechercher : ")
                fnc.getFNCSearch().bingSearch(query)
            case 3:
                query = input("Rechercher : ")
                fnc.getFNCSearch().perplexitySearch(query)
            case 4:
                query = input("Rechercher : ")
                fnc.getFNCSearch().googleSearch(query)
            case 5:
                query = input("Rechercher : ")
                fnc.getFNCSearch().qwantSearch(query)
            case 6:
                query = input("Rechercher : ")
                fnc.getFNCSearch().duckduckgoSearch(query)
            case 7:
                query = input("Rechercher : ")
                fnc.getFNCSearch().bigRecherche(query)
            case 8:
                query = input("Rechercher : ")
                fnc.getFNCSearch().search(query)
            case 0:
                searchBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partDownload():
    downloadBoucle = True
    while downloadBoucle:
        print("Test des fonctions de telechargement")
        print("1.Voir les modes possible\n2.Telechargement en etapes\n3.Telechargement direct\n0.Quitter")
        print("__________________________\n")
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
                print(fnc.getFNCDownload().getAllMode() + " - (audio=2, video=1)")
            case 2:
                print("Telechargement en etapes")
                url = input("URL de la video : ")
                if fnc.getFNCDownload().setUrl(url):
                    print("URL enregistrée")
                    boucleVerif = True
                    while boucleVerif:
                        mode = input("Mode (1-2-3) : ")
                        try:
                            nb = int(mode)
                            if nb == 1 or nb == 2 or nb == 3:
                                boucleVerif = False
                        except ValueError:
                            print("Veuillez entrer un nombre valide.")
                    if fnc.getFNCDownload().refreshDirectory():
                        print("Dossier de telechargement enregistré")
                        if fnc.getFNCDownload().setMode(nb):
                            if fnc.getFNCDownload().download() :
                                print("Telechargement OK")
                            else :
                                print("Erreur lors du telechargement")
                        else :
                            print("Erreur lors de l'enregistrement du mode")
                    else :
                        print("Impossible d'enregistrer le dossier de telechargement")
                else :
                    print("Erreur lors de l'enregistrement de l'URL")
            case 3:
                print("Telechargement en direct")
                url = input("URL de la video : ")
                boucleVerif = True
                while boucleVerif:
                    mode = input("Mode (1-2-3) : ")
                    try:
                        nb = int(mode)
                        if nb == 1 or nb == 2 or nb == 3:
                            boucleVerif = False
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")
                if fnc.getFNCDownload().downloadDirectely(nb,url):
                    print("Telechargement OK")
            case 0:
                downloadBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partCalendar():
    calendarBoucle = True
    while calendarBoucle:
        print("Test des fonctions de calendrier")
        print("1.Ajouter un evenement\n2.Evenement enregister"
              "\n3.Voir les information d'un evenement"
              "\n4.Check event jour\n5.Suppression"
              "\n6.Voir les event du jour\n7.Voir event with date"
              "\n0.Quitter")
        print("__________________________\n")
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
                nom = input("Nom : ")
                date = input("Date (YYYY-MM-DD) : ")
                heure = input("Heure (00:00) : ")
                description = input("Description : ")
                lieu = input("Lieu : ")
                try :
                    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                except ValueError :
                    print("La date n'est pas valide")
                if fnc.getFNCCalendar().addEventToCalendar(nom,date,heure,description,lieu):
                    print("Evenement cree")
                else :
                    print("Impossible de cree l'evenement")
            case 2 :
                print(fnc.getFNCCalendar().getAllEvents())
            case 3 :
                name = input("Entrer le nom de l'evenement :")
                print(fnc.getFNCCalendar().getInformationEvent(name))
            case 4:
                print("Check des evenements du jour")
                print(fnc.getFNCCalendar().checkDateHourEvent())
            case 5 :
                print("Suppression d'un evenement")
                name = input("Entrer le nom de l'evenement :")
                if fnc.getFNCCalendar().delEvent(name):
                    print("Evenement supprimer")
                else :
                    print("Impossible de suppression d'un evenement")
            case 6:
                print("Evenement du jour")
                print(fnc.getFNCCalendar().checkDateDayEvent())
            case 7 :
                date = input("Date (YYYY-MM-DD) : ")
                try :
                    print(fnc.getFNCCalendar().checkEventWithDate(date))
                except ValueError :
                    print("La date n'est pas valide")
            case 0 :
                calendarBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partGPS():
    gpsBoucle = True
    while gpsBoucle:
        print("Test des fonctions de GPS")
        print("1.Get Latitude longitude\n2.Get Ville\n3.Lancer un itineraire sur g map\n0.Quitter")
        print("__________________________\n")
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
                if fnc.getFNCGPS().locate():
                    print("Localisation reussie")
                    latitude = fnc.getFNCGPS().getLatitude()
                    longitude = fnc.getFNCGPS().getLongitude()
                    print(f"Latidude : {latitude} \n logitude : {longitude}")
                else:
                    print("Erreur de localisation")
            case 2:
                if fnc.getFNCGPS().locate():
                    print("Localisation reussie")
                    print(f"Ville : {fnc.getFNCGPS().getTown()}")
                    print(f"Departement : {fnc.getFNCGPS().getRegion()}")
                else:
                    print("Erreur de localisation")
            case 3:
                depart = input("Ville : ")
                arrivee = input("Arrivée : ")
                if fnc.getFNCGPS().launchGoogleMapItinerary(depart, arrivee):
                    print("Itinéraire lancé dans le navigateur")
                else :
                    print("Erreur lors du lancement de l'itinéraire")
            case 0 :
                gpsBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partMeteo():
    meteoBoucle = True
    while meteoBoucle:
        print("Test des fonctions de Météo")
        print("1.Actuelle\n2.Demain\n3.Matinée\n4.Apres-midi\n5.Soirée\n6.Nuit\n0.Quitter")
        print("__________________________\n")
        boucleVerif = True
        while boucleVerif:
            nb = input("Choix : ")
            try:
                nb = int(nb)
                boucleVerif = False
            except ValueError:
                print("Veuillez entrer un nombre valide.")
        if nb == 0:
            meteoBoucle = False
            break

        print("Entrer la localisation : Work,Home,Locate ou Custom")
        data = {"work", "home", "locate", "custom"}
        choix = input("Choix : ").strip().lower()

        if choix in data and nb != 0:
            if choix == "custom":
                ville = input("Entrer la ville : ")
            else :
                ville = ""
            ok = False

            match nb:
                case 1:
                    if gest.getGestFNC().getFNCMeteo().weather_current(choix, ville):
                        print("Donnée recuperer")
                        print("Meteo actuel :")
                        ok = True
                    else :
                        print("Erreur de recuperer")
                case 2:
                    if gest.getGestFNC().getFNCMeteo().weather_tomorrow(choix, ville):
                        print("Donnée recuperer")
                        print("Meteo de demain :")
                        ok = True
                    else:
                        print("Erreur de recuperer")
                case 3:
                    if gest.getGestFNC().getFNCMeteo().weather_morning(choix, ville):
                        print("Donnée recuperer")
                        print("Meteo de la matinée :")
                        ok = True
                    else:
                        print("Erreur de recuperer")
                case 4:
                    if gest.getGestFNC().getFNCMeteo().weather_afternoon(choix, ville):
                        print("Donnée recuperer")
                        print("Meteo de l'apres-midi :")
                        ok = True
                    else:
                        print("Erreur de recuperer")
                case 5:
                    if gest.getGestFNC().getFNCMeteo().weather_evening(choix, ville):
                        print("Donnée recuperer")
                        print("Meteo de la soirée :")
                        ok = True
                    else:
                        print("Erreur de recuperer")
                case 6:
                    if gest.getGestFNC().getFNCMeteo().weather_night(choix, ville):
                        print("Donnée recuperer")
                        print("Meteo de la nuit :")
                        ok = True
                    else:
                        print("Erreur de recuperer")
                case _:
                    print("Choix invalide, veuillez réessayer.")
            if ok:
                print(f"Nom de la ville : {gest.getGestFNC().getFNCMeteo().getNameTown()}")
                print(f"Temperature : {gest.getGestFNC().getFNCMeteo().getTemperature()}")
                print(f"Humiditer : {gest.getGestFNC().getFNCMeteo().getHumidity()}")
                print(f"Description : {gest.getGestFNC().getFNCMeteo().getDescription()}")
                print(f"Icone : {gest.getGestFNC().getFNCMeteo().getIcon()}")
                if gest.getGestFNC().getFNCMeteo().set_alerte():
                    print(f"Alerte Rouge : {gest.getGestFNC().getFNCMeteo().getRedAlert()}")
                    print(f"Alerte Orange : {gest.getGestFNC().getFNCMeteo().getOrangeAlert()}")
                    print(f"Alerte Jaune : {gest.getGestFNC().getFNCMeteo().getYellowAlert()}")
                    print(f"Alerte Vert : {gest.getGestFNC().getFNCMeteo().getGreenAlert()}")
                else :
                    print("Les alerte n'ont pas etais recuperer")
        else :
            print("Erreur : tu dois taper exactement Work, Home, Locate ou Custom. (pas de nom de ville direct)")

def partActu():
    if fnc.getFNCActu().setActu():
        print("Actualité récupéré")
        print(f"NON Netoyer : {fnc.getFNCActu().getActu()}")
        fnc.getFNCActu().clear_articles()
        print("Netoyage en cours")
        print(f"Netoyer : {fnc.getFNCActu().getActu()}")

def partHorloge():
    horlogeBoucle = True
    while horlogeBoucle:
        print("Test des fonctions d'horloge")
        print("1.Chronometre\n2.Minuteur\n3.Horloge\n0.Quitter")
        print("__________________________\n")
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
                if fnc.getFNCHorloge().startChrono():
                    print("Chronometre demarrer")
                    while True:
                        print(f"Temps écoulé : {fnc.getFNCHorloge().getTimeChrono()} secondes")
                        var = input("1.Continuer\n2.Arreter\nChoix : ")
                        if var == "1":
                            continue
                        elif var == "2":
                            fnc.getFNCHorloge().stopChrono()
                            print("Chronometre arreter")
                            break
                        else:
                            print("Choix invalide, veuillez réessayer.")
                    fnc.getFNCHorloge().resetChrono()
            case 2 :
                if fnc.getFNCHorloge().startMinuteur(10):
                    print("Minuteur lancer")
                else :
                    print("Erreur lors du lancement du minuteur")
            case 3:
                print(fnc.getFNCHorloge().getHorloge())
            case 0:
                horlogeBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partRead():
    texte = input("Entrez le texte : ")
    fnc.getFNCRead().read(texte)

def partRadio():
    radioBoucle = True
    while radioBoucle:
        print("Test des fonctions Radio")
        print("1.Europe 1\n2.Europe 2"
              "\n3.France info\n4.France inter"
              "\n5.France Musique\n6.France culture"
              "\n7.France bleu\n8.Fun Radio"
              "\n9.NRJ\n10.RFM"
              "\n11.Nostalgie\n12.Skyrock"
              "\n13.RTL\n14.Stop\n0.Quitter")
        print("__________________________\n")
        boucleVerif = True
        while boucleVerif:
            nb = input("Choix : ")
            try:
                nb = int(nb)
                boucleVerif = False
            except ValueError:
                print("Veuillez entrer un nombre valide.")
        match nb:
            case 1 :
                if fnc.getFNCRadio().startEurope1() :
                    print("Radio Lancer")
                else :
                    print("Erreur lors du lancement de la radio")
            case 2:
                if fnc.getFNCRadio().startEurope2():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 3:
                if fnc.getFNCRadio().startFranceInfo():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 4:
                if fnc.getFNCRadio().startFranceInter():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 5:
                if fnc.getFNCRadio().startFranceMusique():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 6:
                if fnc.getFNCRadio().startFranceCulture():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 7:
                if fnc.getFNCRadio().startFranceBleu():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 8:
                if fnc.getFNCRadio().startFunRadio():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 9:
                if fnc.getFNCRadio().startNRJ():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 10:
                if fnc.getFNCRadio().startRFM():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 11:
                if fnc.getFNCRadio().startNostalgi():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 12:
                if fnc.getFNCRadio().startSkyrock():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 13:
                if fnc.getFNCRadio().startRTL():
                    print("Radio Lancer")
                else:
                    print("Erreur lors du lancement de la radio")
            case 14:
                if fnc.getFNCRadio().stop():
                    print("Radio arreter")
                else:
                    print("Erreur lors de arret de la radio")
            case 0:
                radioBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partTranslate():
    tranlateBoucle = True
    while tranlateBoucle:
        print("Test des fonctions de traduction")
        print("1.View langue\n2.View code langue\n3.View langue et langue code\n4.Set Traducteur\n5.Traduire\n0.Quitter")
        print("__________________________\n")
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
                print(fnc.getFNCTraduction().getLang())
            case 2:
                print(fnc.getFNCTraduction().getLangCode())
            case 3:
                print(fnc.getFNCTraduction().getLangAndLangCode())
            case 4:
                lang1 = input("Langue 1 : ")
                lang2 = input("Langue 2 : ")
                if lang1 != lang2:
                    if fnc.getFNCTraduction().setTranlator(lang1, lang2):
                        print("Traducteur enregistré")
                    else:
                        print("Erreur lors de l'enregistrement du traducteur")
                else:
                    print("Les langues doivent être différentes")
            case 5:
                text = input("Text : ")
                traduction = fnc.getFNCTraduction().tranlate(text)
                if traduction is None:
                    print("Erreur lors de la traduction")
                else :
                    print(traduction)
            case 0:
                tranlateBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partOrthographe():
    orthBoucle = True
    while orthBoucle:
        print("Test des fonctions d'orthographe")
        print("1.Correction orthographique\n2.Copy Correction\n0.Quitter")
        print("__________________________\n")
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
                text = input("Text : ")
                if fnc.getFNCOrthographe().corrected_text(text):
                    print(f"Texte originaux : {fnc.getFNCOrthographe().get_text_no_corrected()}")
                    print(f"Texte corriger : {fnc.getFNCOrthographe().getCorrections()}")
                else :
                    print("Erreur lors du check de l'orthographe")
            case 2:
                if fnc.getFNCOrthographe().copyCorrections():
                    print("Correction copiée dans le presse-papier")
                else:
                    print("Erreur lors de la copie de la correction")
            case 0:
                orthBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partMail():
    mailBoucle = True
    while mailBoucle:
        print("Test des fonctions de Mail")
        print("1.Création complète d'un mail\n"
              "2.Correction d'un mail\n"
              "3.Réponse à un mail\n"
              "4.Copier l'objet\n"
              "5.Copier le mail complet\n"
              "6.Voir le mail complet généré\n"
              "0.Quitter")
        print("__________________________\n")
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
                objet = input("Objet du mail : ")
                consigne = input("Consignes / Détails (optionnel) : ")
                print("Génération en cours (le corps sera automatiquement copié)...")
                if fnc.getFNCMail().create_mail(objet, consigne):
                    print("\n--- Mail généré (corps copié dans le presse-papier) ---")
                    print(fnc.getFNCMail().get_mail_complet())
                    print("-------------------------------------------------------\n")
                else:
                    print("Erreur lors de la génération du mail")
            case 2:
                objet = input("Objet du mail : ")
                mail = input("Corps du mail à corriger : ")
                print("Correction en cours (le corps sera automatiquement copié)...")
                if fnc.getFNCMail().correct_mail(objet, mail):
                    print("\n--- Mail corrigé (corps copié dans le presse-papier) ---")
                    print(fnc.getFNCMail().get_mail_complet())
                    print("--------------------------------------------------------\n")
                else:
                    print("Erreur lors de la correction du mail")
            case 3:
                objet = input("Objet du mail reçu : ")
                mail_recu = input("Corps du mail reçu : ")
                consigne = input("Consignes de réponse : ")
                print("Génération de la réponse en cours (le corps sera automatiquement copié)...")
                if fnc.getFNCMail().reply_mail(objet, mail_recu, consigne):
                    print("\n--- Réponse générée (corps copié dans le presse-papier) ---")
                    print(fnc.getFNCMail().get_mail_complet())
                    print("-----------------------------------------------------------\n")
                else:
                    print("Erreur lors de la génération de la réponse")
            case 4:
                if fnc.getFNCMail().copy_objet():
                    print("Objet copié dans le presse-papier")
                else:
                    print("Erreur lors de la copie de l'objet")
            case 5:
                if fnc.getFNCMail().copy_mail_complet():
                    print("Mail complet copié dans le presse-papier")
                else:
                    print("Erreur lors de la copie du mail complet")
            case 6:
                mail_complet = fnc.getFNCMail().get_mail_complet()
                if mail_complet:
                    print("\n--- Mail Actuel ---")
                    print(mail_complet)
                    print("-------------------\n")
                else:
                    print("Aucun mail généré pour le moment.")
            case 0:
                mailBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partCalculatrice():
    calculBoucle = True
    while calculBoucle:
        print("Test des fonctions de calculatrice")
        print("1.Adition\n2.Soustraction\n3.Multiplication"
              "\n4.Division\n5.Puissance\n6.Modulo"
              "\n7.Racine\n8.Ajouter nombre complexe"
              "\n9.Somme complexe\n10.Soustration complexe"
              "\n11.Multiplication complexe\n12.Division complexe"
              "\n13.Recuperartion complex NB1\n14.Recuperartion complex NB2"
              "\n15.Ajouter nombre Pythagore\n16.Theoreme de Pythagore"
              "\n17.Resiproque de Pythagore\n18.Voir le calcul"
              "\n0.Quitter")
        print("__________________________\n")
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
                a = int(input("Nombre 1 : "))
                b = int(input("Nombre 2 : "))
                print(f"Resultat : {fnc.getFNCCalculatrice().adition(a, b)}")
            case 2:
                a = int(input("Nombre 1 : "))
                b = int(input("Nombre 2 : "))
                print(f"Resultat : {fnc.getFNCCalculatrice().soustraction(a, b)}")
            case 3:
                a = int(input("Nombre 1 : "))
                b = int(input("Nombre 2 : "))
                print(f"Resultat : {fnc.getFNCCalculatrice().multiplication(a, b)}")
            case 4:
                a = int(input("Nombre 1 : "))
                b = int(input("Nombre 2 : "))
                if b == 0:
                    print("Division par zéro impossible")
                else:
                    print(f"Resultat : {fnc.getFNCCalculatrice().divsion(a, b)}")
            case 5:
                a = int(input("Nombre 1 : "))
                b = int(input("Nombre 2 : "))
                print(f"Resultat : {fnc.getFNCCalculatrice().puissance(a, b)}")
            case 6:
                a = int(input("Nombre 1 : "))
                b = int(input("Nombre 2 : "))
                if b == 0:
                    print("Modulo par zéro impossible")
                else:
                    print(f"Resultat : {fnc.getFNCCalculatrice().modulo(a, b)}")
            case 7:
                a = int(input("Nombre (a) : "))
                b = int(input("Racine (b) : "))
                if a < 0 or b <= 0:
                    print("Impossible de calculer la racine")
                else:
                    print(f"Resultat : {fnc.getFNCCalculatrice().racine(a, b)}")
            case 8:
                a1 = complex(input("Nombre complexe 1 (a) : "))
                b1 = complex(input("Nombre complexe 1 (b) : "))
                a2 = complex(input("Nombre complexe 2 (a) : "))
                b2 = complex(input("Nombre complexe 2 (b) : "))
                if fnc.getFNCCalculatrice().setComplexNb(a1, b1, a2, b2):
                    print("Complexe enregistré")
                else:
                    print("Erreur lors de l'enregistrement du complexe")
            case 9:
                print(fnc.getFNCCalculatrice().aditionNbComplex())
            case 10:
                print(fnc.getFNCCalculatrice().soustrationNbComplex())
            case 11:
                print(fnc.getFNCCalculatrice().multiplicationNbComplex())
            case 12:
                print(fnc.getFNCCalculatrice().divisionNbComplex())
            case 13:
                print(fnc.getFNCCalculatrice().recuperationNb1Complex())
            case 14:
                print(fnc.getFNCCalculatrice().recuperationNb2Complex())
            case 15 :
                nb1 = input("Nombre 1 : ")
                nb2 = input("Nombre 2 : ")
                if fnc.getFNCCalculatrice().setNbPythagore(nb1, nb2):
                    print("Nombre Pythagore enregistré")
                else:
                    print("Erreur lors de l'enregistrement du nombre Pythagore")
            case 16:
                print(f"Resultat theoreme : {fnc.getFNCCalculatrice().theoremePythagore()}")
            case 17:
                print(f"Resultat resiproque : {fnc.getFNCCalculatrice().reciproquePythagore()}")
            case 18:
                print(fnc.getFNCCalculatrice().getCalculePythagore())
            case 0:
                calculBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partCodeHelp():
    codeHelpBoucle = True
    while codeHelpBoucle:
        print("Test des fonctions d'aide au codage")
        print("1.Recherche github\n2.Recherche dev doc"
              "\n3.Recherche Microsoft learn\n4.Recherche Python doc"
              "\n0.Quitter")
        print("__________________________\n")
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
                text = input("Recherche : ")
                fnc.getFNCCodeHelp().searchGithub(text)
            case 2:
                text = input("Recherche : ")
                fnc.getFNCCodeHelp().searchDocInDevDoc(text)
            case 3:
                text = input("Recherche : ")
                fnc.getFNCCodeHelp().searchDocInMicrosoft(text)
            case 4:
                text = input("Recherche : ")
                fnc.getFNCCodeHelp().searchDocInPython(text)
            case 0:
                codeHelpBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partWork():
    workBoucle = True
    while workBoucle:
        print("___________________________")
        print("Test des fonctions de travail")
        print("1.Get Etat Open\n2.Open Tableur"
              "\n3.Close Tableur\n4.Lecture tableur"
              "\n5.Ajout d'une valeur\n6.Ajout Somme tableur"
              "\n7.Ajout moyenne tableur\n8.Ajout Comptage tableur"
              "\n9.Ajout Minimum tableur\n10.Ajout Maximum tableur"
              "\n11.Supprimer une valeur"
              "\n12.Open Word\n13.Close Word\n14.Lecture Word"
              "\n15.Ecriture dans Word\n16.Ecrire en effasant le word"
              "\n17.Open Word with OS\n18.Open Tableur with OS"
              "\n19.Voir le projet\n20.Creer un projet"
              "\n21.Ouvrir un projet\n22.Fermer un projet"
              "\n23.Voir le type de projet possible\n24.Ajouter un type au projet"
              "\n25.Voir le type du projet\n26.Voir le nom du projet"
              "\n27.Fichier Nom et extension\n28.Fichier Nom"
              "\n29.Fichier extension\n30.Creation d'un fichier"
              "\n31.Voir le fichier du projet" 
              "\n32. Voir les taches du projet"
              "\n33. Liste taches non fini"
              "\n0.Quitter")
        print("___________________________")
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
                print(f"Word : {fnc.getFNCWork().getEtatWord()}")
                print(f"Tableur : {fnc.getFNCWork().getEtatTableur()}")
                print(f"Projet : {fnc.getFNCWork().getEtatProject()}")
            case 2:
                if fnc.getFNCWork().openTableur():
                    print("Tableur ouvert")
                else:
                    print("Erreur lors de l'ouverture du tableur")
            case 3:
                if fnc.getFNCWork().closeTableur():
                    print("Tableur fermé")
                else:
                    print("Erreur lors de la fermeture du tableur")
            case 4:
                if fnc.getFNCWork().readTableur():
                    print(f"Contenu : {fnc.getFNCWork().getReadTableur()}")
                else :
                    print("Erreur lors de la contenu du tableur")
            case 5 :
                case = input("Case : ")
                valeur = input("Valeur : ")
                if fnc.getFNCWork().addValeurOnTableur(case, valeur):
                    print("Valeur ajouter")
                else :
                    print("Impossible d'ajouter la valeur")
            case 6:
                caseStart = input("Case Start: ")
                caseEnd = input("Case End: ")
                caseDest = input("Case dest: ")
                if fnc.getFNCWork().addSommeOnTableur(caseStart, caseEnd, caseDest):
                    print("Somme ajouter")
                else :
                    print("Impossible d'ajouter la case")
            case 7:
                caseStart = input("Case Start: ")
                caseEnd = input("Case End: ")
                caseDest = input("Case dest: ")
                if fnc.getFNCWork().addMoyenneOnTableur(caseStart, caseEnd, caseDest):
                    print("Somme ajouter")
                else:
                    print("Impossible d'ajouter la case")
            case 8:
                caseStart = input("Case Start: ")
                caseEnd = input("Case End: ")
                caseDest = input("Case dest: ")
                if fnc.getFNCWork().addComptageOnTableur(caseStart, caseEnd, caseDest):
                    print("Somme ajouter")
                else:
                    print("Impossible d'ajouter la case")
            case 9:
                caseStart = input("Case Start: ")
                caseEnd = input("Case End: ")
                caseDest = input("Case dest: ")
                if fnc.getFNCWork().addMinimumOnTableur(caseStart, caseEnd, caseDest):
                    print("Somme ajouter")
                else:
                    print("Impossible d'ajouter la case")
            case 10:
                caseStart = input("Case Start: ")
                caseEnd = input("Case End: ")
                caseDest = input("Case dest: ")
                if fnc.getFNCWork().addMaximumOnTableur(caseStart, caseEnd, caseDest):
                    print("Somme ajouter")
                else:
                    print("Impossible d'ajouter la case")
            case 11 :
                case = input("Case : ")
                if fnc.getFNCWork().delValeur(case):
                    print("Case supprimer")
                else :
                    print("Impossible d'ajouter la case")
            case 12 :
                if fnc.getFNCWork().openWord():
                    print("Word ouvert")
                else:
                    print("Erreur lors de l'ouverture du Word")
            case 13 :
                if fnc.getFNCWork().closeWord():
                    print("Word fermé")
                else:
                    print("Erreur lors de la fermeture du Word")
            case 14 :
                if fnc.getFNCWork().readWord():
                    print(f"Contenu : {fnc.getFNCWork().getReadWord()}")
                else:
                    print("Erreur lors de la lecture du Word")
            case 15 :
                texte = input("Texte : ")
                if fnc.getFNCWork().writeWord(texte):
                    print("Texte écrit dans le Word")
                else :
                    print("Erreur lors de la lecture du Word")
            case 16:
                texte = input("Texte : ")
                if fnc.getFNCWork().writeWordEcrase(texte):
                    print("Texte écrit dans le Word")
                else:
                    print("Erreur lors de la lecture du Word")
            case 17 :
                if fnc.getFNCWork().openWordOs():
                    print("Word ouvert")
                else :
                    print("Erreur lors de l'ouverture du Word")
            case 18:
                if fnc.getFNCWork().openTableurOs():
                    print("Tableur ouvert")
                else:
                    print("Erreur lors de l'ouverture du Tableur")
            case 19 :
                print(f"Liste projet {fnc.getFNCWork().getListProjet()}")
            case 20 :
                name = input("Nom du projet : ")
                if fnc.getFNCWork().createProjet(name):
                    print("Projet créé")
                else:
                    print("Erreur lors de la création du projet")
            case 21:
                name = input("Nom du projet : ")
                if fnc.getFNCWork().openProjet(name):
                    print("Projet ouvert")
                else:
                    print("Erreur lors de l'ouverture du projet")
            case 22:
                if fnc.getFNCWork().closeProjet():
                    print("Projet fermé")
                else :
                    print("Imposible de fermer le projet")
            case 23:
                print("Types de projet possible :")
                print(fnc.getFNCWork().getViewTypeProjetAvailable())
            case 24:
                typeProjet = input("Type de projet : ")
                if fnc.getFNCWork().addTypeProjet(typeProjet):
                    print("Type de projet ajouté")
                else:
                    print("Erreur lors de l'ajout du type de projet")
            case 25:
                print(f"Le type est {fnc.getFNCWork().getTypeProjet()}")
            case 26:
                print(f"Le nom du projet est {fnc.getFNCWork().getNameProjet()}")
            case 27:
                print(f"{fnc.getFNCWork().getNameTypeFileWithExtension()}")
            case 28:
                print(f"{fnc.getFNCWork().getListTypeFileName()}")
            case 29:
                print(f"{fnc.getFNCWork().getListTypeFileExtension()}")
            case 30:
                name = input("Nom du fichier : ")
                type = input("Type du fichier : ")
                if fnc.getFNCWork().createFileProject(name, type):
                    print("Fichier créé")
                else:
                    print("Erreur lors de la création du fichier")
            case 31:
                if fnc.getFNCWork().setlistFileProject():
                    print(f"Liste fichier : {fnc.getFNCWork().getListFileProjet()}")
            case 32 :
                print(f"Liste taches : {fnc.getFNCWork().getFNCTaskProjet().getAllTask()}")
            case 33:
                print(f"Liste taches non fini : {fnc.getFNCWork().getFNCTaskProjet().getNoFinishTask()}")
            case 0:
                workBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")


def partBreef():
    breefBoucle = True
    while breefBoucle:
        print("Test des fonctions de Brief")
        print("1.Morning Brief\n2.Afternoon Brief\n3.Evening Brief\n0.Quitter")
        print("__________________________\n")
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
                print(fnc.getFNCBrief().morning_brief())
            case 2:
                print(fnc.getFNCBrief().afternoon_brief())
            case 3 :
                print(fnc.getFNCBrief().evening_brief())
            case 0:
                breefBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def partOPEN():
    openBoucle = True
    while openBoucle:
        print("Test des fonctions d'Open")
        print("1.Ouvrir un logiciel"
              "\n2.Ouvrir un site"
              "\n3.Ouverture logiciel socket"
              "\n0.Quitter")
        print("__________________________\n")
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
                name = input("Name du logiciel : ")
                if fnc.getFNCOpen().openSoft(name):
                    print(f"Logiciel {name} ouvert")
                else:
                    print(f"Erreur lors de l'ouverture du logiciel {name}")
            case 2:
                name = input("Name du site : ")
                if fnc.getFNCOpen().openSaveWebSiteAssistant(name):
                    print(f"Site {name} ouvert")
                else:
                    print(f"Erreur lors de l'ouverture du site {name}")
            case 3:
                name = input("Name du logiciel : ")
                if fnc.getFNCOpen().openSoftSocket(name):
                    print(f"Logiciel {name} ouvert")
                else:
                    print(f"Erreur lors de l'ouverture du logiciel {name}")
            case 0:
                openBoucle = False
            case _:
                print("Choix invalide, veuillez réessayer.")

def main():

    while True:
        boucleVerif = True
        print("Teste des fonction d'Arrera Neuron Network\n")
        print("1.Taches\n2.Recherche\n"
              "3.Download\n4.Calendrier\n"
              "5.GPS\n6.Meteo\n7.Actualites\n"
              "8.Horloge\n9.Read\n"
              "10.Radio\n11.Traducteur\n"
              "12.Orthographe\n13.Calculatrice\n"
              "14.Codehelp\n15.Work\n"
              "16.Beef\n17.OPEN\n"
              "18.Mail\n"
              "0.Quitter")
        print("__________________________\n")


        while boucleVerif:
            nb = input("Choix : ")
            try :
                nb = int(nb)
                boucleVerif = False
            except ValueError:
                print("Veuillez entrer un nombre valide.")

        match nb:
            case 1:
                partTask()
                break
            case 2 :
                partSearch()
                break
            case 3 :
                partDownload()
            case 4 :
                partCalendar()
            case 5 :
                partGPS()
            case 6 :
                partMeteo()
            case 7 :
                partActu()
            case 8 :
                partHorloge()
            case 9 :
                partRead()
            case 10 :
                partRadio()
            case 11 :
                partTranslate()
            case 12 :
                partOrthographe()
            case 13 :
                partCalculatrice()
            case 14 :
                partCodeHelp()
            case 15 :
                partWork()
            case 16 :
                partBreef()
            case 17:
                partOPEN()
            case 18:
                partMail()
            case 0:
                print("Fin du programme")
                break
            case _:
                continue

if __name__ == "__main__":
    main()
