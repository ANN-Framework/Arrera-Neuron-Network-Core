import json
from datetime import datetime
from gestionnaire.gestion import gestionnaire


class IARouter:
    """
    Routeur principal basé sur l'IA.
    Reçoit la requête utilisateur, l'envoie à l'IA qui retourne un JSON
    {action, args, reponse}, puis dispatch vers la bonne fonction dans gestFNC ou gestGUI.
    """

    def __init__(self, gestionnaire: gestionnaire):
        self.__gestionnaire = gestionnaire
        self.__gestIA = gestionnaire.getGestIA()
        self.__gestFNC = gestionnaire.getGestFNC()
        self.__listSortie = ["", ""]
        self.__valeurOut = 0

        # Table de dispatch : action -> handler
        self.__dispatch = {
            # Actions FNC
            "tache": self.__handle_tache,
            "calendrier": self.__handle_calendrier,
            "horloge": self.__handle_horloge,
            "gps": self.__handle_gps,
            "meteo": self.__handle_meteo,
            "actu": self.__handle_actu,
            "radio": self.__handle_radio,
            "traduction": self.__handle_traduction,
            "brief": self.__handle_brief,
            "work": self.__handle_work,
            "calculatrice": self.__handle_calculatrice,
            "lecture": self.__handle_lecture,
            "orthographe": self.__handle_orthographe,
            "mail": self.__handle_mail,
            "recherche": self.__handle_recherche,
            "open": self.__handle_open,
            "download_youtube": self.__handle_download,
            "codehelp": self.__handle_codehelp,
            # Actions GUI
            "gui": self.__handle_gui,
            # Fallback
            "reponse_simple": self.__handle_reponse_simple,
        }

        # Mapping radio : nom -> méthode
        self.__radio_map = {
            "Europe 1": "startEurope1",
            "Europe 2": "startEurope2",
            "France Info": "startFranceInfo",
            "France inter": "startFranceInter",
            "France Musique": "startFranceMusique",
            "France Culture": "startFranceCulture",
            "France bleu": "startFranceBleu",
            "Fun radio": "startFunRadio",
            "NRJ": "startNRJ",
            "RFM": "startRFM",
            "Nostalgie": "startNostalgi",
            "Skyrock": "startSkyrock",
            "RTL": "startRTL",
        }

        # Mapping recherche : type -> méthode
        self.__search_map = {
            "recherche": "search",
            "google": "googleSearch",
            "brave": "braveSearch",
            "duckduckgo": "duckduckgoSearch",
            "qwant": "qwantSearch",
            "ecosia": "ecosiaSearch",
            "bing": "bingSearch",
            "perplexity": "perplexitySearch",
            "amazon": "amazonSearch",
            "big_recherche": "bigRecherche",
        }

        # Mapping météo : moment -> méthode
        self.__meteo_map = {
            "actuel": "weather_current",
            "demain": "weather_tomorrow",
            "matin": "weather_morning",
            "apres-midi": "weather_afternoon",
            "soir": "weather_evening",
            "nuit": "weather_night",
        }

        # Mapping formules tableur : nom -> méthode
        self.__formule_map = {
            "somme": "addSommeOnTableur",
            "moyenne": "addMoyenneOnTableur",
            "comptage": "addComptageOnTableur",
            "minimum": "addMinimumOnTableur",
            "maximum": "addMaximumOnTableur",
        }

    # ==========================================
    # MÉTHODES UTILITAIRES
    # ==========================================

    def __arg(self, args, index, default=""):
        """Accès sécurisé aux arguments avec valeur par défaut."""
        if index < len(args):
            return str(args[index]) if args[index] is not None else default
        return default

    def __set_output(self, texte, valeur=1, extra=""):
        """Définit la sortie texte et le code valeurOut."""
        self.__listSortie = [texte, extra]
        self.__valeurOut = valeur

    def __parse_date(self, date_str):
        """Parse une date YYYY-MM-DD en datetime. Retourne None si vide ou invalide."""
        if not date_str or date_str.strip() == "":
            return None
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d")
        except ValueError:
            return None

    def __format_list(self, data):
        """Formate une liste en string lisible."""
        if not data:
            return ""
        if isinstance(data, list):
            return "\n".join(f"- {item}" for item in data)
        return str(data)

    def __clean_json(self, text: str) -> str:
        """Nettoie le markdown autour du JSON s'il y en a."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
            
        if text.endswith("```"):
            text = text[:-3]
            
        return text.strip()

    def __prefilter_projet(self, requette: str):
        """
        Garde-fou PROJET : détecte les actions projet par mots-clés
        pour bypasser le LLM qui confond souvent les actions.
        Retourne (args_list, val_out) ou None si pas de match.
        """
        req = requette.lower().strip()

        # Mots-clés pour détecter les actions projet
        mots_ouvrir = ["ouvre le projet", "ouvrir le projet", "ouvre mon projet",
                       "ouvrir mon projet", "lance le projet", "lancer le projet",
                       "charge le projet", "charger le projet"]
        mots_fermer = ["ferme le projet", "fermer le projet", "quitte le projet",
                       "quitter le projet", "ferme mon projet", "fermer mon projet",
                       "ferme projet", "quitte projet"]
        mots_creer = ["crée le projet", "créer le projet", "cree le projet",
                      "creer le projet", "crée un projet", "créer un projet",
                      "cree un projet", "creer un projet", "nouveau projet",
                      "créer un nouveau projet", "crée un nouveau projet"]
        mots_lister = ["liste mes projets", "lister mes projets", "liste les projets",
                       "lister les projets", "mes projets", "quels sont mes projets",
                       "montre mes projets", "affiche mes projets",
                       "liste projet", "lister projet", "liste des projets"]

        # 1. Ouvrir un projet
        for mot in mots_ouvrir:
            if mot in req:
                # Extraire le nom du projet (tout ce qui suit le mot-clé)
                nom_projet = req.split(mot, 1)[1].strip()
                # Nettoyer les mots résiduels
                for residu in ["s'il te plait", "stp", "s'il te plaît", "please", "svp"]:
                    nom_projet = nom_projet.replace(residu, "").strip()
                if nom_projet:
                    return (["projet_ouvrir", nom_projet], 14)
                return None

        # 2. Fermer le projet
        for mot in mots_fermer:
            if mot in req:
                return (["projet_fermer"], 21)

        # 3. Créer un projet
        for mot in mots_creer:
            if mot in req:
                nom_projet = req.split(mot, 1)[1].strip()
                for residu in ["s'il te plait", "stp", "s'il te plaît", "please", "svp",
                                "nommé", "nomme", "appelé", "appele"]:
                    nom_projet = nom_projet.replace(residu, "").strip()
                if nom_projet:
                    return (["projet_creer", nom_projet], 10)
                return None

        # 4. Lister les projets
        for mot in mots_lister:
            if mot in req:
                return (["projet_lister"], 1)

        return None

    # ==========================================
    # MÉTHODE PRINCIPALE DE ROUTAGE
    # ==========================================

    def route(self, requette: str) -> bool:
        """
        Envoie la requête à l'IA, parse le JSON retourné,
        et dispatch vers le bon handler.
        Retourne True si l'action a été traitée, False sinon.
        """
        self.__listSortie = ["", ""]
        self.__valeurOut = 0

        # 1. Vérifier que l'IA est activée
        if not self.__gestIA.get_ia_is_enable():
            return False

        # 1bis. Garde-fou PROJET : détection par mots-clés pour bypasser le LLM
        projet_result = self.__prefilter_projet(requette)
        if projet_result is not None:
            action_args, val_out = projet_result
            try:
                donnees, val_out = self.__handle_work(action_args)
                if not donnees:
                    donnees = "Action terminée."
                reponse_finale = self.__gestIA.generate_final_response(requette, donnees)
                self.__set_output(reponse_finale, val_out)
            except Exception as e:
                print(f"Erreur IARouter [prefilter_projet]: {e}")
                self.__set_output("Une erreur système s'est produite.", 1)
            return self.__valeurOut != 0

        # 2. Envoyer la requête à l'IA
        if not self.__gestIA.send_request_ia(requette):
            return False

        if not self.__gestIA.get_state_ia_reponse():
            return False

        # 3. Parser la réponse JSON
        reponse_brute = self.__gestIA.get_reponse_ia()
        json_str = self.__clean_json(reponse_brute)
        
        try:
            parsed = json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            # L'IA n'a pas retourné du JSON valide → traiter comme texte brut
            self.__set_output(str(reponse_brute))
            return True

        action = parsed.get("action", "")
        args = parsed.get("args", [])
        reponse = parsed.get("reponse", "")

        # 4. Dispatcher vers le bon handler
        if action not in self.__dispatch:
            if action.startswith("projet_") or action.startswith("tableur_") or action.startswith("word_"):
                args.insert(0, action)
                action = "work"
            elif action.startswith("git_") or action.startswith("doc_") or action.startswith("github_") or action in ["commit", "status"]:
                args.insert(0, action)
                action = "codehelp"
                
        if action in self.__dispatch:
            if action == "reponse_simple":
                self.__set_output(reponse)
            else:
                try:
                    donnees, val_out = self.__dispatch[action](args)
                    if not donnees:
                        donnees = "Action terminée. (Aucune donnée textuelle retournée par le système)"
                        
                    reponse_finale = self.__gestIA.generate_final_response(requette, donnees)
                    self.__set_output(reponse_finale, val_out)
                except Exception as e:
                    print(f"Erreur IARouter [{action}]: {e}")
                    self.__set_output("Une erreur système s'est produite lors de l'exécution de l'action.", 1)
        else:
            if reponse:
                self.__set_output(reponse)
            else:
                self.__set_output("Action non reconnue.")

        return self.__valeurOut != 0

    def getListSortie(self) -> list:
        return self.__listSortie

    def getValeurSortie(self) -> int:
        return self.__valeurOut

    # ==========================================
    # HANDLERS - TÂCHES
    # ==========================================

    def __handle_tache(self, args):
        fnc = self.__gestFNC.getFNCTask()
        if fnc is None:
            return "Erreur: FNC Tâche non disponible.", 1

        type_action = self.__arg(args, 0)

        if type_action == "ajouter":
            nom = self.__arg(args, 1)
            date = self.__parse_date(self.__arg(args, 2))
            description = self.__arg(args, 3) or None
            fnc.addTask(nom, date, description)
            return "Tâche ajoutée avec succès.", 5

        elif type_action == "supprimer":
            fnc.delTask(self.__arg(args, 1))
            return "Tâche supprimée.", 5

        elif type_action == "terminer":
            fnc.finishTask(self.__arg(args, 1))
            return "Tâche terminée.", 5

        elif type_action == "reactiver":
            fnc.unfinishTask(self.__arg(args, 1))
            return "Tâche réactivée.", 5

        elif type_action == "lister_tout":
            data = fnc.getAllTask()
            return self.__format_list(data) if data else "Aucune tâche trouvée.", 5

        elif type_action == "lister_non_terminees":
            data = fnc.getNoFinishTask()
            return self.__format_list(data) if data else "Aucune tâche non terminée.", 5

        elif type_action == "lister_terminees":
            data = fnc.getFinishTask()
            return self.__format_list(data) if data else "Aucune tâche terminée.", 5

        elif type_action == "lister_aujourdhui":
            data = fnc.getListTaskToday()
            return self.__format_list(data) if data else "Aucune tâche pour aujourd'hui.", 5

        elif type_action == "lister_demain":
            data = fnc.getListTaskTowmorow()
            return self.__format_list(data) if data else "Aucune tâche pour demain.", 5

        elif type_action == "lister_retard":
            data = fnc.getListTaskLate()
            return self.__format_list(data) if data else "Aucune tâche en retard.", 5

        elif type_action in ("compter", "compter_non_terminees", "compter_terminees",
                             "compter_aujourdhui", "compter_demain", "compter_retard"):
            return "Demande de comptage des tâches effectuée.", 5

        else:
            return "Action de tâche non reconnue.", 1

    # ==========================================
    # HANDLERS - CALENDRIER
    # ==========================================

    def __handle_calendrier(self, args):
        fnc = self.__gestFNC.getFNCCalendar()
        if fnc is None:
            return "Erreur: FNC Calendrier non disponible.", 1

        type_action = self.__arg(args, 0)

        if type_action == "ajouter":
            nom = self.__arg(args, 1)
            date = self.__parse_date(self.__arg(args, 2))
            heure = self.__arg(args, 3)
            description = self.__arg(args, 4)
            lieu = self.__arg(args, 5)
            repetition = self.__arg(args, 6, "false").lower() == "true"
            if date:
                fnc.addEventToCalendar(nom, date, heure, description, lieu, repetition)
                return "Événement ajouté avec succès.", 5
            return "Date invalide.", 1

        elif type_action == "supprimer":
            fnc.delEvent(self.__arg(args, 1))
            return "Événement supprimé.", 5

        elif type_action == "lister_tout":
            data = fnc.getAllEvents()
            return self.__format_list(data) if data else "Aucun événement.", 5

        elif type_action == "lister_aujourdhui":
            data = fnc.checkDateDayEvent()
            return self.__format_list(data) if data else "Aucun événement aujourd'hui.", 5

        elif type_action == "lister_date":
            date_str = self.__arg(args, 2)
            data = fnc.checkEventWithDate(date_str)
            return self.__format_list(data) if data else f"Aucun événement à la date {date_str}.", 5

        elif type_action == "details":
            nom = self.__arg(args, 1)
            data = fnc.getInformationEvent(nom)
            if data and isinstance(data, dict):
                details = "\n".join(f"{k}: {v}" for k, v in data.items())
                return details, 5
            else:
                return "Événement introuvable.", 1

        else:
            return "Action calendrier non reconnue.", 1

    # ==========================================
    # HANDLERS - HORLOGE
    # ==========================================

    def __handle_horloge(self, args):
        fnc = self.__gestFNC.getFNCHorloge()
        if fnc is None:
            return "Erreur: FNC Horloge non disponible.", 1

        type_action = self.__arg(args, 0)

        if type_action == "heure":
            return fnc.getHorloge(), 5

        elif type_action == "chrono_start":
            fnc.startChrono()
            return "Chronomètre démarré.", 5

        elif type_action == "chrono_stop":
            fnc.stopChrono()
            return "Chronomètre arrêté.", 5

        elif type_action == "chrono_reset":
            fnc.resetChrono()
            return "Chronomètre réinitialisé.", 5

        elif type_action == "chrono_temps":
            temps = fnc.getTimeChrono()
            formatted = fnc.formatTemps(temps)
            return f"Temps du chronomètre: {formatted}", 5

        elif type_action == "chrono_etat":
            etat = fnc.getStatChrono()
            return f"État du chronomètre: {'En cours' if etat else 'Arrêté'}", 5

        elif type_action == "minuteur_start":
            duree = self.__arg(args, 1)
            try:
                fnc.startMinuteur(int(duree))
                return f"Minuteur démarré pour {duree} secondes.", 5
            except (ValueError, TypeError):
                return "Durée invalide.", 1

        elif type_action == "minuteur_stop":
            fnc.stopMinuteur()
            return "Minuteur arrêté.", 5

        elif type_action == "minuteur_etat":
            etat = fnc.getStatMinuteur()
            return f"État du minuteur: {'En cours' if etat else 'Arrêté'}", 5

        elif type_action == "minuteur_temps":
            temps = fnc.getTimeMinuteur()
            return f"Temps restant du minuteur: {temps}", 5

        else:
            return "Action horloge non reconnue.", 1

    # ==========================================
    # HANDLERS - GPS
    # ==========================================

    def __handle_gps(self, args):
        fnc = self.__gestFNC.getFNCGPS()
        if fnc is None:
            return "Erreur: FNC GPS non disponible.", 1

        type_action = self.__arg(args, 0)

        if type_action == "itineraire":
            depart = self.__arg(args, 1)
            arrivee = self.__arg(args, 2)
            fnc.launchGoogleMapItinerary(depart, arrivee)
            return "Itinéraire lancé dans le navigateur.", 5

        elif type_action == "localisation":
            fnc.locate()
            return "Localisation lancée dans le navigateur.", 5

        elif type_action == "departement":
            ville = self.__arg(args, 1)
            dept = fnc.getFrenchDepartementWithTown(ville)
            return dept if dept else "Département introuvable", 5

        elif type_action == "ville_coordonnees":
            lat = self.__arg(args, 1)
            lon = self.__arg(args, 2)
            ville = fnc.getTownWithLatitudeAndLongitude(lat, lon)
            return ville if ville else "Ville introuvable pour ces coordonnées.", 5

        else:
            return "Action GPS non reconnue.", 1

    # ==========================================
    # HANDLERS - MÉTÉO
    # ==========================================

    def __handle_meteo(self, args):
        fnc = self.__gestFNC.getFNCMeteo()
        if fnc is None:
            return "Erreur: FNC Météo non disponible.", 1

        moment = self.__arg(args, 0)
        emplacement = self.__arg(args, 1)
        ville_custom = self.__arg(args, 2)

        if not emplacement or emplacement.strip() == "":
            emplacement = "locate"
        elif emplacement == "custom" and (not ville_custom or ville_custom.strip() == ""):
            emplacement = "locate"

        if moment == "alerte":
            fnc.set_alerte()
            return f"Alerte météo vérifiée. Rouge: {fnc.getRedAlert()}, Orange: {fnc.getOrangeAlert()}, Jaune: {fnc.getYellowAlert()}", 4

        method_name = self.__meteo_map.get(moment)
        if method_name:
            method = getattr(fnc, method_name, None)
            if method:
                if emplacement == "custom" and ville_custom:
                    result = method(emplacement, ville_custom)
                else:
                    result = method(emplacement)
                
                if result:
                    ville = fnc.getNameTown()
                    temp = fnc.getTemperature()
                    desc = fnc.getDescription()
                    return f"Météo à {ville}: {desc}, {temp}°C", 4
                else:
                    return "Impossible d'obtenir la météo.", 1
            else:
                return "Erreur: méthode météo introuvable.", 1
        else:
            return "Erreur: moment météo non reconnu.", 1

    # ==========================================
    # HANDLERS - ACTUALITÉS
    # ==========================================

    def __handle_actu(self, args):
        fnc = self.__gestFNC.getFNCActu()
        if fnc is None:
            return "Erreur: FNC Actu non disponible.", 1

        limite = self.__arg(args, 0, "3")
        try:
            limit_int = int(limite)
        except (ValueError, TypeError):
            limit_int = 3

        if fnc.setActu(limit_int):
            return fnc.get_actu_say() or fnc.getActu() or "Actualités récupérées.", 3
        else:
            return "Impossible d'obtenir les actualités.", 1

    # ==========================================
    # HANDLERS - RADIO
    # ==========================================

    def __handle_radio(self, args):
        fnc = self.__gestFNC.getFNCRadio()
        if fnc is None:
            return "Erreur: FNC Radio non disponible.", 1

        action_radio = self.__arg(args, 0)

        if action_radio == "stop":
            fnc.stop()
            return "Radio arrêtée.", 22

        elif action_radio == "etat":
            fnc.getRadioRunning()
            return "Statut de la radio consulté.", 22

        elif action_radio in self.__radio_map:
            method = getattr(fnc, self.__radio_map[action_radio], None)
            if method and method():
                return f"Radio {action_radio} lancée.", 22
            else:
                return "Impossible de lancer la radio.", 1
        else:
            return "Action radio non reconnue.", 1

    # ==========================================
    # HANDLERS - TRADUCTION
    # ==========================================

    def __handle_traduction(self, args):
        fnc = self.__gestFNC.getFNCTraduction()
        if fnc is None:
            return "Erreur: FNC Traduction non disponible.", 1

        texte = self.__arg(args, 0)
        lang_source = self.__arg(args, 1, "francais")
        lang_cible = self.__arg(args, 2)

        if fnc.setTranlator(lang_source, lang_cible):
            result = fnc.tranlate(texte)
            if result:
                return f"Traduction de '{texte}': {result}", 11
            else:
                return "Impossible de traduire le texte.", 1
        else:
            return "Langues de traduction non supportées.", 1

    # ==========================================
    # HANDLERS - BRIEF
    # ==========================================

    def __handle_brief(self, args):
        moment = self.__arg(args, 0,"morning")

        brief_gui_map = {
            "morning": "morning_brief",
            "afternoon": "afternoon_brief",
            "evening": "evening_brief",
        }

        gui_name = brief_gui_map.get(moment, "morning_brief")

        if self.__gestionnaire.has_gui() and self.__gestionnaire.getGestGUI().setGUIActive(gui_name):
            return f"Interface de brief {moment} ouverte.", 5

        meteo_str = "Indisponible"
        fnc_meteo = self.__gestFNC.getFNCMeteo()

        if fnc_meteo and fnc_meteo.weather_current("locate"):
            meteo_str = f"{fnc_meteo.getNameTown()} : {fnc_meteo.getDescription()}, {fnc_meteo.getTemperature()}°C"

        taches = []
        fnc_task = self.__gestFNC.getFNCTask()

        if fnc_task:
            taches = fnc_task.getListTaskToday() or []
        taches_str = ", ".join(taches) if taches else "Aucune tâche prévue aujourd'hui"

        return f"Brief ({moment}) — Météo : {meteo_str}. Tâches du jour : {taches_str}.", 1

    # ==========================================
    # HANDLERS - WORK (Tableur / Word / Projet)
    # ==========================================

    def __handle_work(self, args):
        fnc = self.__gestFNC.getFNCWork()
        if fnc is None:
            return "Erreur: FNC Work non disponible.", 1

        type_action = self.__arg(args, 0)
        param1 = self.__arg(args, 1)
        param2 = self.__arg(args, 2)
        param3 = self.__arg(args, 3)

        # --- TABLEUR ---
        if type_action == "tableur_ouvrir":
            fnc.openTableur()
            return "Tableur ouvert.", 7

        elif type_action == "tableur_ouvrir_direct":
            fnc.openTableurDirectly(param1)
            return "Tableur ouvert directement.", 7

        elif type_action == "tableur_fermer":
            fnc.closeTableur()
            return "Tableur fermé.", 8

        elif type_action == "tableur_lire":
            if fnc.readTableur():
                data = fnc.getReadTableur()
                return self.__format_list(data) if data else "Le tableur est vide.", 13
            else:
                return "Impossible de lire le tableur.", 1

        elif type_action == "tableur_ecrire":
            fnc.addValeurOnTableur(param1, param2)
            return "Valeur ajoutée au tableur.", 5

        elif type_action == "tableur_supprimer":
            fnc.delValeur(param1)
            return "Valeur supprimée du tableur.", 5

        elif type_action == "tableur_formule":
            formule = param1
            range_parts = param2.split(":") if ":" in param2 else [param2, param2]
            case_start = range_parts[0] if len(range_parts) > 0 else ""
            case_stop = range_parts[1] if len(range_parts) > 1 else ""
            case_dest = param3

            if formule in self.__formule_map:
                method = getattr(fnc, self.__formule_map[formule], None)
                if method:
                    method(case_start, case_stop, case_dest)
                    return f"Formule {formule} appliquée.", 5
            return "Impossible d'appliquer la formule.", 1

        elif type_action == "tableur_ouvrir_os":
            fnc.openTableurOs()
            return "Tableur ouvert via OS.", 5

        elif type_action == "tableur_etat":
            etat = fnc.getEtatTableur()
            return f"État du tableur: {'Ouvert' if etat else 'Fermé'}", 5

        # --- WORD ---
        elif type_action == "word_ouvrir":
            fnc.openWord()
            return "Document Word ouvert.", 7

        elif type_action == "word_ouvrir_direct":
            fnc.openWordDirectly(param1)
            return "Document Word ouvert directement.", 7

        elif type_action == "word_fermer":
            fnc.closeWord()
            return "Document Word fermé.", 8

        elif type_action == "word_lire":
            if fnc.readWord():
                data = fnc.getReadWord()
                return str(data) if data else "Le document est vide.", 9
            else:
                return "Impossible de lire le document Word.", 1

        elif type_action == "word_ecrire":
            fnc.writeWord(param1)
            return "Texte écrit dans Word.", 5

        elif type_action == "word_ecrire_ecrase":
            fnc.writeWordEcrase(param1)
            return "Texte écrasé dans Word.", 5

        elif type_action == "word_ouvrir_os":
            fnc.openWordOs()
            return "Document Word ouvert via OS.", 5

        elif type_action == "word_etat":
            etat = fnc.getEtatWord()
            return f"État de Word: {'Ouvert' if etat else 'Fermé'}", 5

        # --- PROJET ---
        elif type_action == "projet_lister":
            data = fnc.getListProjet()
            return self.__format_list(data) if data else "Aucun projet existant.", 1

        elif type_action == "projet_creer":
            fnc.createProjet(param1)
            return f"Projet '{param1}' créé.", 10

        elif type_action == "projet_ouvrir":
            fnc.openProjet(param1)
            return f"Projet '{param1}' ouvert.", 14

        elif type_action == "projet_fermer":
            fnc.closeProjet()
            return "Projet fermé.", 21

        elif type_action == "projet_type":
            fnc.addTypeProjet(param1)
            return "Type de projet défini.", 5

        elif type_action == "projet_nom":
            nom = fnc.getNameProjet()
            return f"Nom du projet: {nom}", 5

        elif type_action == "projet_get_type":
            type_proj = fnc.getTypeProjet()
            return f"Type du projet: {type_proj}", 5

        elif type_action == "projet_etat":
            etat = fnc.getEtatProject()
            return f"État du projet: {'Ouvert' if etat else 'Fermé'}", 5

        elif type_action == "projet_creer_fichier":
            fnc.createFileProject(param1, param2)
            return f"Fichier '{param1}' avec extension '{param2}' créé dans le projet.", 16

        elif type_action == "projet_lister_fichiers":
            fnc.setlistFileProject()
            data = fnc.getListFileProjet()
            return self.__format_list(data) if data else "Aucun fichier dans le projet.", 5

        elif type_action == "projet_creer_dossier":
            if fnc.createFolderProject(param1):
                return f"Dossier '{param1}' créé avec succès dans le projet.", 5
            return f"Échec de la création du dossier '{param1}'.", 1
        elif type_action == "projet_ecrire_fichier":
            if fnc.writeFileProject(param1, param2):
                return f"Fichier '{param1}' écrit avec succès.", 5
            return f"Échec de l'écriture dans le fichier '{param1}'.", 1
        elif type_action == "projet_lire_fichier":
            contenu = fnc.readFileProject(param1)
            return contenu, 5
        elif type_action == "projet_executer_commande":
            succes, sortie = fnc.executeCommandProject(param1)
            statut = "Succès" if succes else "Échec"
            return f"Exécution ({statut}) :\n{sortie}", 5

        # --- ACTIONS GIT SUR LE PROJET ---
        elif type_action in ["git_commit", "projet_commit", "commit"]:
            msg = param1 or param2 or "Commit automatique agent"
            fnc_ch = self.__gestFNC.getFNCCodeHelp()
            if fnc_ch:
                succes, retour = fnc_ch.gitCommit(msg)
                statut = "Succès" if succes else "Échec"
                return f"Git ({statut}) : {retour}", 5
            return "Erreur: CodeHelp non disponible pour Git.", 1

        elif type_action in ["git_status", "projet_git_status", "status"]:
            fnc_ch = self.__gestFNC.getFNCCodeHelp()
            if fnc_ch:
                return fnc_ch.gitStatus(), 5
            return "Erreur: CodeHelp non disponible pour Git.", 1

        elif type_action in ["git_init", "projet_git_init"]:
            fnc_ch = self.__gestFNC.getFNCCodeHelp()
            if fnc_ch:
                succes, retour = fnc_ch.gitInit()
                statut = "Succès" if succes else "Échec"
                return f"Git ({statut}) : {retour}", 5
            return "Erreur: CodeHelp non disponible pour Git.", 1

        # --- TÂCHES DU PROJET ---
        elif type_action == "projet_tache_ajouter":
            date = self.__parse_date(param2)
            desc = param3 or None
            fnc.addTacheProjet(param1, date, desc)
            return "Tâche de projet ajoutée.", 5

        elif type_action == "projet_tache_supprimer":
            fnc.supprTacheProjet(param1)
            return "Tâche de projet supprimée.", 5

        elif type_action == "projet_tache_terminer":
            fnc.finishTacheProjet(param1)
            return "Tâche de projet terminée.", 5

        elif type_action == "projet_tache_non_terminees":
            fnc.setListTacheNoFinishProjet()
            data = fnc.getListTacheNoFinishProjet()
            return self.__format_list(data) if data else "Aucune tâche de projet non terminée.", 5

        elif type_action == "projet_tache_aujourdhui":
            fnc.setListTacheTodayProjet()
            data = fnc.getListTacheTodayProjet()
            return self.__format_list(data) if data else "Aucune tâche de projet pour aujourd'hui.", 5

        elif type_action == "projet_tache_demain":
            fnc.setListTacheTowmorowProjet()
            data = fnc.getListTacheTowmorowProjet()
            return self.__format_list(data) if data else "Aucune tâche de projet pour demain.", 5

        else:
            return "Action work non reconnue.", 1

    # ==========================================
    # HANDLERS - CALCULATRICE
    # ==========================================

    def __handle_calculatrice(self, args):
        fnc = self.__gestFNC.getFNCCalculatrice()
        if fnc is None:
            return "Erreur: FNC Calculatrice non disponible.", 1

        type_calcul = self.__arg(args, 0)
        param1 = self.__arg(args, 1)
        param2 = self.__arg(args, 2)
        param3 = self.__arg(args, 3)
        param4 = self.__arg(args, 4)

        try:
            if type_calcul == "addition":
                result = fnc.adition(float(param1), float(param2))
                return f"Résultat de l'addition : {result}", 1

            elif type_calcul == "soustraction":
                result = fnc.soustraction(float(param1), float(param2))
                return f"Résultat de la soustraction : {result}", 1

            elif type_calcul == "multiplication":
                result = fnc.multiplication(float(param1), float(param2))
                return f"Résultat de la multiplication : {result}", 1

            elif type_calcul == "division":
                result = fnc.divsion(float(param1), float(param2))
                if result is not None:
                    return f"Résultat de la division : {result}", 1
                else:
                    return "Erreur: division par zéro", 1

            elif type_calcul == "puissance":
                result = fnc.puissance(float(param1), float(param2))
                return f"Résultat de la puissance : {result}", 1

            elif type_calcul == "modulo":
                result = fnc.modulo(float(param1), float(param2))
                if result is not None:
                    return f"Résultat du modulo : {result}", 1
                else:
                    return "Erreur modulo", 1

            elif type_calcul == "racine":
                result = fnc.racine(float(param1), float(param2))
                if result is not None:
                    return f"Résultat de la racine : {result}", 1
                else:
                    return "Erreur de racine", 1

            elif type_calcul == "complexe":
                fnc.setComplexNb(float(param1), float(param2),
                                float(param3), float(param4))
                operation = self.__arg(args, 5, "addition")

                complex_ops = {
                    "addition": fnc.aditionNbComplex,
                    "soustraction": fnc.soustrationNbComplex,
                    "multiplication": fnc.multiplicationNbComplex,
                    "division": fnc.divisionNbComplex,
                }
                op_method = complex_ops.get(operation, fnc.aditionNbComplex)
                result = op_method()
                return f"Résultat du calcul complexe : {result}", 1

            elif type_calcul == "pythagore":
                fnc.setNbPythagore(float(param1), float(param2))
                result = fnc.theoremePythagore()
                return f"Résultat de Pythagore : {result}", 1

            elif type_calcul == "pythagore_reciproque":
                fnc.setNbPythagore(float(param1), float(param2))
                result = fnc.reciproquePythagore()
                return f"Résultat de la réciproque de Pythagore : {result}", 1

            elif type_calcul in ("ouvrir_interface", "ouvrir_interface_normal"):
                return self.__handle_gui(["calculatrice_normal", ""])
            
            elif type_calcul == "ouvrir_interface_pythagore":
                return self.__handle_gui(["calculatrice_pythagore", ""])
            
            elif type_calcul == "ouvrir_interface_complex":
                return self.__handle_gui(["calculatrice_complex", ""])

            else:
                return "Type de calcul non reconnu", 1

        except (ValueError, TypeError, ZeroDivisionError):
            return "Erreur de calcul", 1

    # ==========================================
    # HANDLERS - LECTURE
    # ==========================================

    def __handle_lecture(self, args):
        fnc = self.__gestFNC.getFNCRead()
        if fnc is None:
            return "Erreur: FNC Lecture non disponible.", 1

        type_action = self.__arg(args, 0)

        if type_action == "lire":
            texte = self.__arg(args, 1)
            fnc.read(texte)
            return "Lecture démarrée.", 5

        elif type_action == "etat":
            fnc.getStatTheard()
            return "État de la lecture consulté.", 5

        elif type_action == "ouvrir_interface":
            return self.__handle_gui(["lecture", ""])

        else:
            return "Action lecture non reconnue.", 1

    # ==========================================
    # HANDLERS - ORTHOGRAPHE
    # ==========================================

    def __handle_orthographe(self, args):
        fnc = self.__gestFNC.getFNCOrthographe()
        if fnc is None:
            return "Erreur: FNC Orthographe non disponible.", 1

        type_action = self.__arg(args, 0)

        if type_action == "corriger":
            texte = self.__arg(args, 1)
            if fnc.corrected_text(texte):
                correction = fnc.getCorrections()
                return f"Texte corrigé: {correction}" if correction else "Correction terminée.", 11
            else:
                return "Impossible de corriger le texte.", 1

        elif type_action == "copier":
            fnc.copyCorrections()
            return "Correction copiée dans le presse-papier.", 5

        elif type_action == "etat":
            fnc.getToolLaunched()
            return "État du correcteur consulté.", 5

        elif type_action == "ouvrir_interface":
            return self.__handle_gui(["orthographe", texte if texte else ""])

        else:
            return "Action orthographe non reconnue.", 1

    # ==========================================
    # HANDLERS - MAIL
    # ==========================================

    def __handle_mail(self, args):
        fnc = self.__gestFNC.getFNCMail()
        if fnc is None:
            return "Erreur: FNC Mail non disponible.", 1

        type_action = self.__arg(args, 0)
        objet = self.__arg(args, 1)
        p1 = self.__arg(args, 2)
        p2 = self.__arg(args, 3)

        if type_action in ("creer", "creation", "create"):
            if fnc.create_mail(objet, p1):
                return f"E-mail généré avec succès :\n\n{fnc.get_mail_complet()}", 5
            return "Impossible de générer l'e-mail.", 1

        elif type_action in ("corriger", "correction", "correct"):
            if fnc.correct_mail(objet, p1):
                return f"E-mail corrigé :\n\n{fnc.get_mail_complet()}", 5
            return "Impossible de corriger l'e-mail.", 1

        elif type_action in ("repondre", "reponse", "reply"):
            if fnc.reply_mail(objet, p1, p2):
                return f"Réponse générée :\n\n{fnc.get_mail_complet()}", 5
            return "Impossible de générer la réponse à l'e-mail.", 1

        elif type_action in ("copier_objet", "copy_objet"):
            if fnc.copy_objet():
                return "Objet de l'e-mail copié dans le presse-papier.", 5
            return "Impossible de copier l'objet.", 1

        elif type_action in ("copier_corps", "copy_corps"):
            return "Le corps du mail a déjà été copié automatiquement lors de la génération.", 5

        elif type_action in ("copier_tout", "copier_mail", "copy_mail", "copy_all"):
            if fnc.copy_mail_complet():
                return "E-mail complet copié dans le presse-papier.", 5
            return "Impossible de copier l'e-mail.", 1

        elif type_action in ("etat", "state"):
            etat = fnc.getToolLaunched()
            return f"État de la fonction mail: {'Actif' if etat else 'Inactif'}", 5

        else:
            return "Action mail non reconnue.", 1

    # ==========================================
    # HANDLERS - RECHERCHE
    # ==========================================

    def __handle_recherche(self, args):
        fnc = self.__gestFNC.getFNCSearch()
        if fnc is None:
            return "Erreur: FNC Recherche non disponible.", 1

        type_recherche = self.__arg(args, 0, "recherche")
        requete = self.__arg(args, 1)

        method_name = self.__search_map.get(type_recherche)
        if method_name:
            method = getattr(fnc, method_name, None)
            if method:
                method(requete)
                return f"Recherche {type_recherche} lancée pour '{requete}'.", 5
            else:
                return "Moteur de recherche introuvable.", 1
        else:
            return "Type de recherche non reconnu.", 1

    # ==========================================
    # HANDLERS - OPEN
    # ==========================================

    def __handle_open(self, args):
        fnc = self.__gestFNC.getFNCOpen()
        if fnc is None:
            return "Erreur: FNC Open non disponible.", 1

        type_action = self.__arg(args, 0)
        cible = self.__arg(args, 1)

        if type_action == "logiciel":
            fnc.openSoft(cible)
            return f"Logiciel '{cible}' ouvert.", 5

        elif type_action == "site_enregistre":
            fnc.openSaveWebSite(cible)
            return f"Site enregistré '{cible}' ouvert.", 5

        elif type_action == "url":
            fnc.openWebSite(cible)
            return f"URL '{cible}' ouverte.", 5

        elif type_action == "ouvrir_interface":
            return self.__handle_gui(["open", ""])

        elif type_action == "lister_logiciels":
            user_conf = self.__gestionnaire.getUserConf()
            list_soft = list(user_conf.getSoft().keys())
            if not list_soft:
                return "Aucun logiciel enregistré.", 1
            return "Logiciels enregistrés :\n" + "\n".join(f"- {s}" for s in list_soft), 1

        elif type_action == "lister_sites":
            user_conf = self.__gestionnaire.getUserConf()
            list_sites = list(user_conf.getSite().keys())
            if not list_sites:
                return "Aucun site web enregistré.", 1
            return "Sites web enregistrés :\n" + "\n".join(f"- {s}" for s in list_sites), 1

        elif type_action == "lister_radios":
            radios = ["Europe 1", "Europe 2", "France Info", "France Inter",
                      "France Musique", "France Culture", "France Bleu",
                      "Fun Radio", "NRJ", "RFM", "Nostalgie", "Skyrock", "RTL"]
            return "Radios disponibles :\n" + "\n".join(f"- {r}" for r in radios), 1

        elif type_action == "doc_assistant":
            link = self.__gestionnaire.getLinkDoc()
            if fnc.openSaveWebSiteAssistant(link):
                return "Documentation de l'assistant ouverte.", 1
            else:
                return "Impossible d'ouvrir la documentation.", 1

        else:
            return "Action open non reconnue.", 1

    # ==========================================
    # HANDLERS - DOWNLOAD YOUTUBE
    # ==========================================

    def __handle_download(self, args):
        fnc = self.__gestFNC.getFNCDownload()
        if fnc is None:
            return "Erreur: FNC Download non disponible.", 1

        mode = self.__arg(args, 0, "1")
        url = self.__arg(args, 1)

        try:
            mode_int = int(mode)
        except (ValueError, TypeError):
            if mode == "ouvrir_interface":
                return self.__handle_gui(["arrera_download", ""])
            mode_int = 1

        fnc.downloadDirectely(mode_int, url)
        return "Téléchargement YouTube démarré.", 5

    # ==========================================
    # HANDLERS - CODEHELP
    # ==========================================

    def __handle_codehelp(self, args):
        fnc = self.__gestFNC.getFNCCodeHelp()
        if fnc is None:
            return "Erreur: FNC CodeHelp non disponible.", 1

        type_action = self.__arg(args, 0)
        param1 = self.__arg(args, 1)

        codehelp_actions = {
            "doc_devdoc": lambda: fnc.searchDocInDevDoc(param1),
            "doc_microsoft": lambda: fnc.searchDocInMicrosoft(param1),
            "doc_python": lambda: fnc.searchDocInPython(param1),
            "github_search": lambda: fnc.searchGithub(param1),
            "github_site": lambda: fnc.openSiteGithub(),
            "gui_color": lambda: fnc.openGUIColorSelector(),
            "gui_github": lambda: fnc.openGUIGithubGestion(),
            "gui_librairy": lambda: fnc.openGUILibrairy(),
            "gui_git": lambda: fnc.openGUIGitGestion(),
            "git_init": lambda: fnc.gitInit(),
            "git_status": lambda: fnc.gitStatus(),
            "git_add": lambda: fnc.gitAdd(),
            "git_commit": lambda: fnc.gitCommit(param1),
            "git_log": lambda: fnc.gitLog(),
        }

        action = codehelp_actions.get(type_action)
        if action:
            res = action()
            if isinstance(res, tuple):
                succes, msg = res
                statut = "Succès" if succes else "Échec"
                return f"Git ({statut}) : {msg}", 5
            elif isinstance(res, str):
                return res, 5
            return f"Action CodeHelp '{type_action}' exécutée.", 5
        return "Action CodeHelp non reconnue.", 1

    # ==========================================
    # HANDLERS - GUI
    # ==========================================

    def __handle_gui(self, args):
        nom_gui = self.__arg(args, 0)
        parametre = self.__arg(args, 1)

        parms = parametre if parametre else None

        if self.__gestionnaire.has_gui() and self.__gestionnaire.getGestGUI().setGUIActive(nom_gui, parms):
            return f"Interface graphique '{nom_gui}' ouverte.", 5
        else:
            return f"Impossible d'ouvrir l'interface '{nom_gui}'.", 5

    # ==========================================
    # HANDLERS - RÉPONSE SIMPLE (fallback)
    # ==========================================

    def __handle_reponse_simple(self, args):
        return "Réponse simple sans fonction.", 1
