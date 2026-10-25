import threading as th
from gestionnaire.gestion import *
from datetime import datetime, time


class ABrain :
    __KEYWORDS_ARRET = {
        "arret", "arreter", "arrete", "stop", "stoppe", "stopper",
        "eteindre", "eteins", "quitter", "quitte", "fermer", "exit",
        "shutdown", "bye", "byebye", "ciao", "adieu",
        "au revoir", "aurevoir", "a la prochaine", "a plus", "a plus tard",
        "a demain", "a bientot", "bonne nuit", "bonne soiree", "bon apres midi",
        "arrete toi", "eteins toi", "ferme toi", "coupe toi",
        "eteins l assistant", "ferme l assistant", "eteins le systeme",
        "je te laisse", "je dois y aller", "je m en vais", "je pars",
        "je vais dormir", "je vais me coucher", "c est tout", "c est bon",
        "on arrete la", "j ai termine", "j ai fini", "on a fini", "coupe tout"
    }

    __NON_ARRET_TARGETS = (
        "radio", "musique", "son", "flux",
        "minuteur", "chrono", "chronometre", "alarme", "bip", "compte a rebours",
        "projet", "project", "tableur", "excel", "word", "fichier", "document", "page",
        "fenetre", "calculatrice", "calculette", "agenda", "calendrier", "tache", "traducteur", "lecture",
        "de parler", "d ecrire", "de lire"
    )

    __EXCLUSION_EXPRESSIONS = (
        "arret de bus", "arret de tram", "arret de metro", "arret de train",
        "arret maladie", "arret de travail", "sans arret", "pourquoi ca s arrete"
    )

    __POLITENESS_RESIDUES = (
        "s il te plait", "s il vous plait", "stp", "svp", "please",
        "merci", "bonne journee", "bon courage", "dis", "dit"
    )

    def __init__(self,config:confNeuron):
        self.__listOut =  []
        self.__valeurOut = 0
        self.__networkRunning = True
        self.__update = False
        self.__neuronUsed = str
        # Gestionnaire
        self.__gestionnaire = gestionnaire(config)
        self.__gestIA = self.__gestionnaire.getGestIA()
        if self.__gestionnaire.getUserConf().get_ia_model() != "":
            if not self.__gestIA.loadIA():
                raise Exception("Erreur critique : Impossible de charger le modèle IA.")
        self.__gestNeuron = self.__gestionnaire.getGestNeuron()
        # Partie serveur
        self.__gestSocket = self.__gestionnaire.getSocketObjet()
        #initilisation du gestionnaire du reseau de neuron
        self.__gestLangue = self.__gestionnaire.getLanguageObjet()
        #recuperation etat du reseau
        self.__etatReseau = self.__gestionnaire.getNetworkObjet().getEtatInternet()
        # Theard recevied message socket
        if self.__gestSocket is not None and self.__gestSocket.get_client_is_on():
            self.__threadSocket = th.Thread(target=self.__gestSocket.received_message_client)
            self.__threadSocket.daemon = True
            self.__threadSocket.start()


    def getGestionnaire(self):
        return self.__gestionnaire

    def getNeuronRunning(self):
        return self.__networkRunning

    def boot(self):
        return self.__gestionnaire.boot()

    def shutdown(self):
        hour = datetime.now().hour
        text = self.__gestLangue.aurevoir(hour)
        if self.__gestIA is not None:
            self.__gestIA.unloadIA()
        if self.__gestionnaire.getGestNeuron().getSocket():
            if self.__gestSocket.get_client_is_on():
                self.__gestSocket.stop_socket_client()

            if self.__gestSocket.get_server_is_on():
                self.__gestSocket.stop_socket_server()
        self.__gestionnaire.getGestHist().saveHist()
        self.__gestionnaire.getGestSession().clearSession()
        return str(text)

    def reload_ia(self) -> bool:
        """Désinstancie le modèle actuel et recharge/réinstancie le modèle IA configuré."""
        if self.__gestIA is not None:
            return self.__gestIA.loadIA()
        return False

    def get_ia_queue_size(self) -> int:
        if self.__gestIA is not None:
            return self.__gestIA.get_queue_size()
        return 0

    def is_ia_busy(self) -> bool:
        if self.__gestIA is not None:
            return self.__gestIA.is_busy()
        return False

    
    def getListSortie(self)->list :
        if self.__valeurOut == 5 or self.__valeurOut == 12 or self.__valeurOut == 18 or self.__valeurOut == 19:
            if not self.__valeurOut == 12 or not self.__valeurOut == 18 or not self.__valeurOut == 19:
                texte = self.__getTextWithTkinterWindows()
                if texte is not None:
                    self.__listOut = texte

        if self.__valeurOut == 23 :
            self.__gestionnaire.getGestFNC().getFNCCodeHelp().launchGui()

        if self.__listOut == ["",""]:
            self.__listOut = [self.__gestLangue.nocomprehension(), ""]

        #print(self.__listOut)
        return self.__listOut

    def getNeuronUsed(self)-> type[str]:
        return self.__neuronUsed

    def getValeurSortie(self)->int :
        """
        0 : Aucun sortie
        1 : Sortie normale
        3 : Sortie actu
        4 : Meteo / temperature / GPS
        5 : Sortie avec fenetre tkinter
        6 : Erreur actu
        7 : Ouverture de fichier
        8 : Fermeture de fichier
        9 : Lecture fichier
        10 : Creation d'un projet
        11 : Erreur du resumer actulités
        12 : Reussite du resumer actulités
        13 : Lecture tableur
        14 : Ouverture d'un projet
        15 : Arret de l'assistant
        16 : Creation d'un fichier dans un projet
        17 : Affichage aide
        18 : Resumer tache / agenda
        19 : Resumer all ok 
        20 : Resumer all fail
        21 : Close projet
        22 : Lancement de radio
        23 : GUI Codehelp
        """
        return self.__valeurOut

    def __getTextWithTkinterWindows(self):
        if self.__gestionnaire.getGestGUI().launch_gui():
            return [self.__gestionnaire.getGestGUI().textOut(),""]
        else :
            return None
    
    def getTableur(self):
        return self.__gestionnaire.getGestFNC().getFNCWork().getEtatTableur()
    
    def getWord(self):
        return self.__gestionnaire.getGestFNC().getFNCWork().getEtatWord()

    def getProject(self):
        return self.__gestionnaire.getGestFNC().getFNCWork().getEtatProject()

    def getUserData(self):
        return self.__gestionnaire.getLanguageObjet().getDataUser()

    def is_stop_assistant_requette(self, requete: str) -> bool:
        req = self.__gestionnaire.netoyageChaine(str(requete).lower()).strip()

        for expr in self.__EXCLUSION_EXPRESSIONS:
            if expr in req:
                return False

        verbes_arret = ("arrete", "stop", "stoppe", "coupe", "eteins", "ferme", "quitte")
        if any(v in req for v in verbes_arret):
            for target in self.__NON_ARRET_TARGETS:
                if target in req:
                    return False

        nom_assistant = self.__gestionnaire.getName().lower()
        if nom_assistant and nom_assistant in req:
            req = req.replace(nom_assistant, "").strip()

        for residu in self.__POLITENESS_RESIDUES:
            req = req.replace(residu, "").strip()

        req = " ".join(req.split())

        return req in self.__KEYWORDS_ARRET

    def neuron(self, var: str):
        # Var local
        requette = self.__gestionnaire.netoyageChaine(str(var).lower())
        # Var de l'objet
        self.__valeurOut = 0
        self.__listOut = []
        self.__neuronUsed = "none"

        if self.is_stop_assistant_requette(requette):
            self.__listOut = [self.shutdown(), ""]
            self.__valeurOut = 15
            self.__neuronUsed = "core"
            self.__gestionnaire.setOld(self.__listOut[0], requette)
            return

        intent = self.__gestionnaire.getGestIA().classify_intent(requette)
        mots_intent = intent.split(" ")

        # 2. Check pour arrêt complet issu de la classification IA (avec filtre de sécurité)
        if mots_intent[0] == "ARRET" and not any(target in requette for target in self.__NON_ARRET_TARGETS):
            self.__listOut = [self.shutdown(), ""]
            self.__valeurOut = 15
            self.__neuronUsed = "core"
        elif mots_intent[0] != "COMPLEXE":
            # 3. Utilisation du core neuron (les intents rapides)
            self.__gestNeuron.ncore.neuron(intent, requette)
            self.__valeurOut = self.__gestNeuron.ncore.getValeurSortie()
            self.__listOut = self.__gestNeuron.ncore.getListSortie()
            self.__neuronUsed = "core"
        else:
            # 4. Utilisation du routeur IA complexe
            success = self.__gestNeuron.iarouter.route(requette)
            
            if success and self.__gestNeuron.iarouter.getValeurSortie() != 0:
                self.__valeurOut = self.__gestNeuron.iarouter.getValeurSortie()
                self.__listOut = self.__gestNeuron.iarouter.getListSortie()
                self.__neuronUsed = "IA"
            else:
                self.__valeurOut = 0
                self.__listOut = [self.__gestLangue.nocomprehension(), ""]

        # Sauvegarde de la sortie et de l'entrée
        if (self.__valeurOut == 3) or (self.__valeurOut == 12) or (self.__valeurOut == 11):
            self.__gestionnaire.setOld("requette api", requette)
        else:
            self.__gestionnaire.setOld(self.__listOut[0], requette)

        # Enregistrement dans la mémoire à court terme (session active)
        if self.__listOut and self.__listOut[0] and self.__valeurOut != 15:
            mots_reset = [
                "oublie notre conversation", "oublie cette conversation",
                "oublie notre discussion", "oublie cette discussion",
                "recommencons a zero", "recommençons a zero", "recommençons à zéro",
                "nouveau sujet", "changeons de sujet", "efface la session",
                "reset session"
            ]
            if not any(mot in requette for mot in mots_reset):
                self.__gestionnaire.getGestSession().addTurn(
                    user_input=str(var),
                    assistant_output=self.__listOut[0],
                    action=self.__neuronUsed
                )

    def updateAssistant(self):
        # print("updateAssistant")
        # Ajouter la partie mise a jour du socket
        self.__gestionnaire.updateDate()
        if (time(0,0) <= datetime.now().time() < time(11,0) and not
        self.__gestionnaire.get_state_morning_brief() and self.__gestNeuron.getBrief() and
        self.__gestionnaire.has_gui()):
            self.__gestionnaire.set_state_morning_brief()
            try:
                response = self.__gestIA.generate_final_response("","Annonce-lui que son brief du matin est prêt.")
                self.__listOut = [response if response else "Brief du matin prêt.",""]
            except Exception as e:
                print(f"Erreur generate_final_response morning: {e}")
                self.__listOut = ["Brief du matin prêt.",""]
            self.__gestionnaire.getGestGUI().active_morning_brief()
            self.__valeurOut = 5
            return True
        elif (time(11,0) <= datetime.now().time() < time(16,0) and not
        self.__gestionnaire.get_state_afternoon_brief() and self.__gestNeuron.getBrief() and
        self.__gestionnaire.has_gui()):
            self.__gestionnaire.set_state_afternoon_brief()
            try:
                response = self.__gestIA.generate_final_response("","Annonce-lui que son brief de l'après-midi est prêt.")
                self.__listOut = [response if response else "Brief de l'après-midi prêt.",""]
            except Exception as e:
                print(f"Erreur generate_final_response afternoon: {e}")
                self.__listOut = ["Brief de l'après-midi prêt.",""]
            self.__gestionnaire.getGestGUI().active_afternoon_brief()
            self.__valeurOut = 5
            return True
        elif (time(16,0) <= datetime.now().time() and not
        self.__gestionnaire.get_state_evening_brief() and self.__gestNeuron.getBrief() and
        self.__gestionnaire.has_gui()):
            self.__gestionnaire.set_state_evening_brief()
            try:
                response = self.__gestIA.generate_final_response("","Annonce-lui que son brief de la soirée est prêt.")
                self.__listOut = [response if response else "Brief de la soirée prêt.",""]
            except Exception as e:
                print(f"Erreur generate_final_response evening: {e}")
                self.__listOut = ["Brief de la soirée prêt.",""]
            self.__gestionnaire.getGestGUI().active_evening_brief()
            self.__valeurOut = 5
            return True
        elif self.__gestSocket is not None:
            if self.__gestSocket.get_new_client_is_connected():
                new_client = self.__gestSocket.get_name_new_client()
                if new_client == "arrera_markdown":
                    fnc_work = self.__gestionnaire.getGestFNC().getFNCWork()
                    if fnc_work is not None:
                        pending_file = fnc_work.popPendingMarkdownFile()
                        if pending_file:
                            self.__gestSocket.send_data_with_server_to("arrera_markdown", f"openfile {pending_file}")
                self.__listOut = ["soft connected",""]
                self.__valeurOut = 1
                return True
            elif self.__gestSocket.get_message_is_received_from_server():
                out = self.__gestSocket.get_message_from_server()
                client = out["client"]
                message = out["message"]
                if message != "Message Received" :
                    if client == "arrera_markdown":
                        self.__gestNeuron.nmarkdown.neurone(message)
                        self.__listOut = self.__gestNeuron.nmarkdown.getListSortie()
                        self.__valeurOut = self.__gestNeuron.nmarkdown.getValeurSortie()
                        return True
                    else :
                        return False
                else :
                    return False
            elif self.__gestSocket.get_message_is_received_form_client():
                if self.__gestionnaire.getKeywordObjet().checkInterface(
                        self.__gestSocket.get_message_form_client(), "requette"):
                    mots = self.__gestionnaire.getKeywordObjet().getListKeyword("interface", "requette")
                    message = self.__gestSocket.get_message_form_client().replace(mots[0], "").strip()
                    self.neuron(message)
                    return True
                else:
                    message = self.__gestSocket.get_message_form_client()
                    self.__gestNeuron.ninterface.neurone(message)
                    self.__listOut = self.__gestNeuron.ninterface.getListSortie()
                    self.__valeurOut = self.__gestNeuron.ninterface.getValeurSortie()
                    return True
            else :
                return False
        else :
            return False
