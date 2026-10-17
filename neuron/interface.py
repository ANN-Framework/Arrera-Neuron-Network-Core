from neuron.CNeuronBase import neuronBase,gestionnaire
import random
from datetime import time,datetime

class interface(neuronBase):
    def __init__(self,gestionnaire:gestionnaire) -> None:
        super().__init__(gestionnaire)

    def neurone(self,requette:str):
        if self._keyword.checkInterface(requette,"erreuropensoft") :
            self._valeurOut = 1
            self._listSortie = [self._gestIA.generate_final_response("","Erreur de l'ouverture d'un logiciel par l'application Arrera"),""]
        elif self._keyword.checkInterface(requette,"noopensoft") :
            self._valeurOut = 1
            self._listSortie = [self._gestIA.generate_final_response("","Ouverture d'un logiciel par l'application Arrera"),""]
        elif self._keyword.checkInterface(requette,"opensoft") :
            self._valeurOut = 1
            self._listSortie = [self._gestIA.generate_final_response("","Ouverture d'un logiciel par l'application Arrera")
                ,""]
        elif self._keyword.checkInterface(requette,"breef"):
            self._gestionnaire.updateDate()
            if (time(0, 0) <= datetime.now().time() < time(11, 0) and not
            self._gestionnaire.get_state_morning_brief()):
                self._gestionnaire.set_state_morning_brief()
                self._gestionnaire.getGestGUI().active_morning_brief()
                self._listSortie = [self._gestIA.generate_final_response("", "Ouverture du brief du matin"), ""]
                self._valeurOut = 5

            elif (time(11, 0) <= datetime.now().time() < time(16, 0) and not
            self._gestionnaire.get_state_afternoon_brief()):
                self._gestionnaire.set_state_afternoon_brief()
                self._gestionnaire.getGestGUI().active_afternoon_brief()
                self._listSortie = [self._gestIA.generate_final_response("", "Ouverture du brief de l'apres midi"), ""]
                self._valeurOut = 5

            elif (time(16, 0) <= datetime.now().time() and not
            self._gestionnaire.get_state_evening_brief()):
                self._gestionnaire.set_state_evening_brief()
                self._gestionnaire.getGestGUI().active_evening_brief()
                self._listSortie = [self._gestIA.generate_final_response("", "Ouverture du brief de la soirée"), ""]
                self._valeurOut = 5


        elif self._keyword.checkInterface(requette,"meteo"):
            if self._gestFNC.getFNCMeteo().weather_current("locate"):
                town = self._gestFNC.getFNCMeteo().getNameTown()
                temperature = self._gestFNC.getFNCMeteo().getTemperature()
                description = self._gestFNC.getFNCMeteo().getDescription()
                donnees = f"OK {town} : {description} avec {temperature}°C"
            else :
                donnees = "PAS OK : Impossible de récupérer la météo."

            self._valeurOut = 0
            self._listSortie = [self._gestIA.generate_final_response("METEO",donnees),""]

        elif self._keyword.checkInterface(requette, "task"):
            self._valeurOut = 1
            self._listSortie = [self._gestIA.generate_final_response("OUVRE INTERFACE TACHE", ""), ""]
            self._gestionnaire.getGestGUI().activeTache()

        elif self._keyword.checkInterface(requette, "agenda"):
            self._valeurOut = 1
            self._listSortie = [self._gestIA.generate_final_response("OUVRE INTERFACE AGENDA", ""), ""]
            self._gestionnaire.getGestGUI().activeAgenda()

        elif self._keyword.checkInterface(requette,"modeone"):
            self._valeurOut = 1
            name = requette.replace(self._keyword.getListKeyword("interface","modeone")[0],"").strip()
            self._listSortie = [self._gestIA.generate_final_response("",f"Ouverture du mode {name} par l'application Arrera"),
                                ""]
            self._gestHist.add_action("open_mode","mode1")
            self._gestionnaire.setModeIsEnabled(True)
        elif self._keyword.checkInterface(requette,"modetwo"):
            self._valeurOut = 1
            name = requette.replace(self._keyword.getListKeyword("interface","modetwo")[0],"").strip()
            self._listSortie = [
                self._gestIA.generate_final_response("", f"Ouverture du mode {name} par l'application Arrera"),
                ""]
            self._gestHist.add_action("open_mode","mode2")
            self._gestionnaire.setModeIsEnabled(True)
        elif self._keyword.checkInterface(requette,"modetheer"):
            self._valeurOut = 1
            name = requette.replace(self._keyword.getListKeyword("interface","modetheer")[0],"").strip()
            self._listSortie = [
                self._gestIA.generate_final_response("", f"Ouverture du mode {name} par l'application Arrera"),
                ""]
            self._gestHist.add_action("open_mode","mode3")
            self._gestionnaire.setModeIsEnabled(True)
        elif self._keyword.checkInterface(requette,"modefoor"):
            self._valeurOut = 1
            name = requette.replace(self._keyword.getListKeyword("interface","modefoor")[0],"").strip()
            self._listSortie = [
                self._gestIA.generate_final_response("", f"Ouverture du mode {name} par l'application Arrera"),
                ""]
            self._gestHist.add_action("open_mode","mode4")
            self._gestionnaire.setModeIsEnabled(True)
        elif self._keyword.checkInterface(requette,"modefive"):
            self._valeurOut = 1
            name = requette.replace(self._keyword.getListKeyword("interface","modefive")[0],"").strip()
            self._listSortie = [
                self._gestIA.generate_final_response("", f"Ouverture du mode {name} par l'application Arrera"),
                ""]
            self._gestHist.add_action("open_mode","mode5")
            self._gestionnaire.setModeIsEnabled(True)
        elif self._keyword.checkInterface(requette,"modesix"):
            self._valeurOut = 1
            name = requette.replace(self._keyword.getListKeyword("interface","modesix")[0],"").strip()
            self._listSortie = [
                self._gestIA.generate_final_response("", f"Ouverture du mode {name} par l'application Arrera"),
                ""]
            self._gestHist.add_action("open_mode","mode6")
            self._gestionnaire.setModeIsEnabled(True)
        elif self._keyword.checkInterface(requette,"errorlaunchmode"):
            self._valeurOut = 1
            self._listSortie = [
                self._gestIA.generate_final_response("", "Erreur d'ouverture d'un mode par l'application Arrera"),
                ""]
        elif self._keyword.checkInterface(requette,"closemode"):
            self._valeurOut = 1
            name = requette.replace(self._keyword.getListKeyword("interface","closemode")[0],"").strip()
            self._listSortie = [
                self._gestIA.generate_final_response("", f"Fermeture du mode {name} par l'application Arrera"),
                ""]
            self._gestHist.add_action("close_mode",name)
            self._gestionnaire.setModeIsEnabled(False)
        elif self._keyword.checkInterface(requette,"close"):
            self._valeurOut = 15