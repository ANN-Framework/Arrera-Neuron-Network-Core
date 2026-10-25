"""
Lanceur console / headless pour Arrera Neuron Network (Opale)
Ce module permet d'exécuter l'assistant Opale en mode terminal sans aucune dépendance Tkinter.
"""
from config.confNeuron import confNeuron
from brain.brain import ABrain
from librairy.dectectionOS import OS
import sys
import os
import time
import threading
from datetime import datetime


class Opale:
    def __init__(self, mode_langue: int = 1, voice_assistant: bool = False):
        """
        Initialise l'assistant Opale en mode console (Headless).
        :param mode_langue: 1 pour Vouvoiement, 2 pour Tutoiement
        :param voice_assistant: Activation ou non de la synthèse vocale
        """
        self.__emplacementLangue = "language/vouvoiment/" if mode_langue == 1 else "language/tutoiment/"
        self.__voice_assistant = voice_assistant
        self.__objOS = OS()
        self.__logContent = ""
        self.__config = None
        self.__assistantBrain = None
        self.__running = False
        self.__lock = threading.Lock()
        self.__updateThread = None

    def active(self):
        """
        Démarre l'assistant Opale dans la console.
        """
        print("==================================================")
        print("    Arrera Neuron Network - Assistant Opale       ")
        print("              (Mode Headless / Console)           ")
        print("==================================================")

        if not self.__setConfig():
            print("Erreur : Impossible de créer la configuration d'Opale.")
            return

        if not self.__startAssistantBrain():
            print("Erreur : Impossible de démarrer le cerveau de l'assistant (ABrain).")
            return

        self.__bootAssistant()
        self.__consoleLoop()

    def __setConfig(self):
        try:
            self.__config = confNeuron(
                name="Opale",
                lang="fr",
                asset="asset/",
                icon="asset/icon.png",
                bute="developper un algo de ChatBot qui sera inclut dans SIX et Ryley",
                createur="Pauchet Baptiste",
                listFonction=[
                    "ouvrir une application",
                    "aider sur les recherches de internet",
                    "donner la meteo",
                    "faire un résumer des actualités"
                ],
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
                brief_enable=1,
                lienDoc="www.google.com",
                fichierLangue=str(self.__emplacementLangue),
                fichierKeyword="keyword/",
                voiceAssistant=self.__voice_assistant
            )
            return True
        except Exception as e:
            print(f"Erreur lors de la configuration de l'assistant : {e}")
            return False

    def __startAssistantBrain(self):
        try:
            self.__assistantBrain = ABrain(config=self.__config)
            return True
        except Exception as e:
            print(f"Erreur lors du démarrage d'ABrain : {e}")
            return False

    def __bootAssistant(self):
        try:
            boot_msg = self.__assistantBrain.boot()
            print(f"\n[Opale] : {boot_msg}\n")
        except Exception as e:
            print(f"\n[Opale] : Erreur lors du boot ({e})\n")

    def __updateLoop(self):
        """
        Boucle de mise à jour en arrière-plan (équivalent du timer GUI)
        pour traiter les événements Socket (Arrera-Interface & Arrera Markdown) en mode Headless.
        """
        while self.__running:
            try:
                with self.__lock:
                    if not self.__running or self.__assistantBrain is None:
                        break
                    has_event = self.__assistantBrain.updateAssistant()
                    if has_event:
                        nb = self.__assistantBrain.getValeurSortie()
                        texte = self.__assistantBrain.getListSortie()
                        reponse = texte[0] if texte and len(texte) > 0 else ""

                        if reponse:
                            print(f"\r\n[Opale (Socket)] : {reponse}\nVous > ", end="", flush=True)
                        self.__addLog(nb, reponse, "[Socket/Update]")

                        if nb == 15:
                            print("\r\nArrêt de l'assistant demandé via Socket...")
                            self.__close()
                            os._exit(0)
            except Exception as e:
                print(f"\r\n[Erreur updateAssistant] : {e}\nVous > ", end="", flush=True)
            time.sleep(0.2)

    def __consoleLoop(self):
        self.__running = True
        self.__updateThread = threading.Thread(target=self.__updateLoop, daemon=True)
        self.__updateThread.start()

        print("Entrez votre message ci-dessous (ou tapez 'stop' / 'quitter' pour fermer) :\n")

        while self.__running:
            try:
                requette = input("Vous > ").strip()
                if not requette:
                    continue

                if requette.lower() in ["quitter", "exit", "quit"] or self.__assistantBrain.is_stop_assistant_requette(requette):
                    print("\nArrêt demandé...")
                    with self.__lock:
                        self.__close()
                    break

                with self.__lock:
                    self.__assistantBrain.neuron(requette)
                    nb = self.__assistantBrain.getValeurSortie()
                    texte = self.__assistantBrain.getListSortie()
                    reponse = texte[0] if texte and len(texte) > 0 else ""

                print(f"\n[Opale] : {reponse}\n")
                self.__addLog(nb, reponse, requette)

                if nb == 15:
                    print("\nArrêt de l'assistant...")
                    with self.__lock:
                        self.__close()
                    break

            except (KeyboardInterrupt, EOFError):
                print("\nInterruption détectée.")
                with self.__lock:
                    self.__close()
                break
            except Exception as e:
                print(f"Erreur pendant l'exécution : {e}")

    def __close(self):
        if not self.__running:
            return
        self.__running = False
        if self.__assistantBrain is not None:
            try:
                self.__assistantBrain.shutdown()
            except Exception as e:
                print(f"Erreur lors de l'arrêt de l'assistant : {e}")

        if self.__logContent:
            self.__saveLog()

    def __addLog(self, nbOut: int, outTexte: str, inTexte: str):
        self.__logContent += f"{inTexte} -> {nbOut} : {outTexte}\n"

    def __saveLog(self):
        date = datetime.now().strftime("%d-%m-%Y-%H-%M")
        if self.__objOS.osLinux() or self.__objOS.osMac():
            home = os.path.expanduser("~")
            file = os.path.join(home, "log_assistant", f"log_{date}.txt")
        else:
            home = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
            file = os.path.join(home, "log_assistant", f"log_{date}.txt")

        if not os.path.isfile(file):
            os.makedirs(os.path.dirname(file), exist_ok=True)

        try:
            with open(file, "w", encoding="utf-8") as f:
                f.write(self.__logContent)
            print(f"Log sauvegardé dans : {file}")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du log : {e}")
            return False


# Alias de compatibilité
GUIOpale = Opale


if __name__ == "__main__":
    opale = Opale()
    opale.active()
