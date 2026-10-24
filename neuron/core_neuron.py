from datetime import *

from neuron.CNeuronBase import neuronBase,gestionnaire

class core_neuron(neuronBase):
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire)
        self.__fnc_meteo = self._gestFNC.getFNCMeteo()
        self.__fnc_radio = self._gestFNC.getFNCRadio()
        self.__gestIA = self._gestionnaire.getGestIA()

    def neuron(self, intent:str, requette_raw:str):
        mots = intent.split(" ")
        #print(intent)
        
        if mots[0] != "COMPLEXE" and mots[0] != "ARRET":
            
            if mots[0] == "METEO":
                if self.__part_meteo(mots):
                    town = self.__fnc_meteo.getNameTown()
                    temperature = self.__fnc_meteo.getTemperature()
                    description = self.__fnc_meteo.getDescription()
                    donnees = f"OK {town} : {description} avec {temperature}°C"
                    reponse = self.__gestIA.generate_final_response(requette_raw, donnees)
                    self._valeurOut = 1
                    self._listSortie = [reponse, ""]
                else :
                    donnees = "PAS OK : Impossible de récupérer la météo."
                    reponse = self.__gestIA.generate_final_response(requette_raw, donnees)
                    self._valeurOut = 1
                    self._listSortie = [reponse, ""]
                
            elif mots[0] == "TEMPERATURE":
                if self.__part_meteo(mots):
                    temperature = self.__fnc_meteo.getTemperature()
                    donnees = f"OK {temperature}°C"
                    reponse = self.__gestIA.generate_final_response(requette_raw, donnees)
                    self._valeurOut = 1
                    self._listSortie = [reponse, ""]
                else :
                    donnees = "PAS OK : Impossible de récupérer la température."
                    reponse = self.__gestIA.generate_final_response(requette_raw, donnees)
                    self._valeurOut = 1
                    self._listSortie = [reponse, ""]

            elif mots[0] == "ACTU":
                theme = mots[1] if len(mots) > 1 else ""
                if theme == "TOUT":
                    target = "actu_all"
                elif theme == "TECH":
                    target = "actu_tech"
                elif theme == "GENERALISTE":
                    target = "actu_main"
                elif theme == "SCIENCE":
                    target = "actu_science"
                elif theme == "SPORT":
                    target = "actu_sport"
                elif theme == "CULTURE":
                    target = "actu_culture"
                else:
                    target = "actu_all"

                if self._gestionnaire.has_gui() and self._gestionnaire.getGestGUI().setGUIActive(target):
                    self._valeurOut = 5
                    self._listSortie = ["", ""]
                else:
                    fnc_actu = self._gestFNC.getFNCActu()
                    if fnc_actu and fnc_actu.setActu(3):
                        actu_say = fnc_actu.get_actu_say()
                        if isinstance(actu_say, list) and actu_say and actu_say[0] != "error":
                            donnees = actu_say[0]
                        else:
                            donnees = str(fnc_actu.getActu())
                    else:
                        donnees = "Impossible de récupérer les actualités pour le moment."
                    self._valeurOut = 1
                    reponse = self.__gestIA.generate_final_response(requette_raw, donnees)
                    self._listSortie = [reponse, ""]

            elif mots[0] == "RADIO":
                nom_radio = " ".join(mots[1:]) if len(mots) > 1 else ""
                if self.__part_radio(mots):
                    if nom_radio == "STOP":
                        donnees = "OK Radio arrêtée"
                        self._valeurOut = 1
                    else:
                        donnees = f"OK Radio lancée : {nom_radio}"
                        self._valeurOut = 22
                    reponse = self.__gestIA.generate_final_response(requette_raw, donnees)
                    self._listSortie = [reponse, ""]
                else:
                    donnees = "PAS OK pour la radio"
                    reponse = self.__gestIA.generate_final_response(requette_raw, donnees)
                    self._valeurOut = 1
                    self._listSortie = [reponse, ""]

            elif mots[0] == "HEURE":
                heure_str = datetime.now().strftime("%H:%M")
                reponse = self.__gestIA.generate_final_response(requette_raw, heure_str)
                self._valeurOut = 1
                self._listSortie = [reponse, ""]

            elif mots[0] == "MINUTEUR":
                if self._gestionnaire.has_gui() and self._gestionnaire.getGestGUI().setGUIActive("minuteur"):
                    self._valeurOut = 5
                    self._listSortie = ["", ""]
                else:
                    donnees = "Mode sans interface graphique : précise une durée en secondes pour démarrer un minuteur."
                    reponse = self.__gestIA.generate_final_response(requette_raw, donnees)
                    self._valeurOut = 1
                    self._listSortie = [reponse, ""]

            elif mots[0] == "GUI":
                nom_gui = mots[1].lower() if len(mots) > 1 else ""

                mapping = {
                    "calculatrice": "calculatrice_normal",
                    "lecture": "lecture",
                    "orthographe": "orthographe",
                    "traducteur": "traducteur",
                    "agenda": "agenda",
                    "tache": "tache",
                    "work": "work",
                    "tache_projet": "tache_projet",
                    "download": "arrera_download"
                }

                if nom_gui == "tache" and self._gestionnaire.getGestFNC().getFNCWork().getEtatProject():
                    nom_gui = "tache_projet"

                target_gui = mapping.get(nom_gui, nom_gui)

                if self._gestionnaire.has_gui() and self._gestionnaire.getGestGUI().setGUIActive(target_gui):
                    self._valeurOut = 5
                    self._listSortie = ["", ""]
                else:
                    # Fallback Headless pour Tâches et Agenda
                    if nom_gui == "tache":
                        taches = self._gestFNC.getFNCTask().getNoFinishTask()
                        donnees = f"Tâches en cours : {', '.join(taches)}" if taches else "Aucune tâche en cours."
                    elif nom_gui == "agenda":
                        events = self._gestFNC.getFNCCalendar().checkDateDayEvent()
                        donnees = f"Événements du jour : {', '.join(events)}" if events else "Aucun événement prévu aujourd'hui."
                    else:
                        donnees = f"Aucune interface graphique n'est connectée pour afficher {nom_gui}, mais tu peux me demander d'exécuter l'action directement."
                    self._valeurOut = 1
                    reponse = self.__gestIA.generate_final_response(requette_raw, donnees)
                    self._listSortie = [reponse, ""]

        elif mots[0] == "ARRET":
            self._valeurOut = 15
            self._listSortie = ["stop",""]

    def __part_meteo(self,mots:list):
        valid_moments = ["MAINTENANT", "NOW", "DEMAIN", "MATIN", "APREM"]
        
        # Si le 2ème mot est un moment valide, on parse normalement
        if len(mots) > 1 and mots[1] in valid_moments:
            moment = mots[1]
            lieu = " ".join(mots[2:]) if len(mots) > 2 else ""
        else:
            # Sinon, ça veut dire que l'IA a omis le moment, et mots[1] est déjà le début du lieu !
            moment = "MAINTENANT" # Moment par défaut
            lieu = " ".join(mots[1:]) if len(mots) > 1 else ""

        if lieu == "DOMICILE" or lieu == "HOME":
            location = "home"
        elif lieu == "TRAVAIL" or lieu == "WORK":
            location = "work"
        elif lieu == "LOCATE" or lieu == "":
            location = "locate"
        else:
            location = "custom"

        if moment == "DEMAIN":
            return self.__fnc_meteo.weather_tomorrow(location, town=lieu)
        elif moment == "MATIN":
            return self.__fnc_meteo.weather_matin(location, town=lieu)
        elif moment == "APREM":
            return self.__fnc_meteo.weather_afternoon(location, town=lieu)
        else :
            return self.__fnc_meteo.weather_current(location, town=lieu)

    def __part_radio(self, mots: list):
        nom_radio = " ".join(mots[1:]) if len(mots) > 1 else ""
        if nom_radio == "STOP":
            return self.__fnc_radio.stop()
        elif nom_radio == "EUROPE 1":
            return self.__fnc_radio.startEurope1()
        elif nom_radio == "EUROPE 2":
            return self.__fnc_radio.startEurope2()
        elif nom_radio == "FRANCE INFO":
            return self.__fnc_radio.startFranceInfo()
        elif nom_radio == "FRANCE INTER":
            return self.__fnc_radio.startFranceInter()
        elif nom_radio == "FRANCE MUSIQUE":
            return self.__fnc_radio.startFranceMusique()
        elif nom_radio == "FRANCE CULTURE":
            return self.__fnc_radio.startFranceCulture()
        elif nom_radio == "FRANCE BLEU":
            return self.__fnc_radio.startFranceBleu()
        elif nom_radio == "FUN RADIO":
            return self.__fnc_radio.startFunRadio()
        elif nom_radio == "NRJ":
            return self.__fnc_radio.startNRJ()
        elif nom_radio == "RFM":
            return self.__fnc_radio.startRFM()
        elif nom_radio == "NOSTALGIE":
            return self.__fnc_radio.startNostalgi()
        elif nom_radio == "SKYROCK":
            return self.__fnc_radio.startSkyrock()
        elif nom_radio == "RTL":
            return self.__fnc_radio.startRTL()
        else:
            return False
