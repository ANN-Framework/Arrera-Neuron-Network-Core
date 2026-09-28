import json
import os
import queue
import threading
from gestionnaire.gestion import gestionnaire
from librairy.ArreraIALoad import ArreraIALoad
from librairy.model_downloader import *

class gestIA :
    def __init__(self,gestionnaire:gestionnaire):

        self.__gestionnaire =  gestionnaire

        self.__ia_mode_enabled = False
        self.__ia_loader : ArreraIALoad = None

        self.__reponse_ia = ""

        self.__model_reponse_ok = False

        self.__downloader_model = model_downloader()

        self.__gest_user = gestionnaire.getUserConf()

        self.__dir_ia_instruction = "instruction_ia/"

        self.__dict_help_file = {"orthographe":"prompt_orthographe.txt",
                                 "dedoublonnage":"prompt_dedoublonnage.txt",
                                 "mail_creation":"prompt_mail_creation.txt",
                                 "mail_correction":"prompt_mail_correction.txt",
                                 "mail_reponse":"prompt_mail_reponse.txt"}

        self.__additional_instructions: list[str] = []

        # Gestion de la file d'attente et du multi-threading pour l'IA
        self.__task_queue = queue.Queue()
        self.__ia_lock = threading.Lock()
        self.__worker_thread = None
        self.__running = False
        self.__is_processing = False

    def __start_worker(self):
        if not self.__running:
            self.__running = True
            self.__worker_thread = threading.Thread(target=self.__worker_loop, daemon=True)
            self.__worker_thread.start()

    def stop_worker(self):
        self.__running = False
        self.__task_queue.put(None)
        if self.__worker_thread and self.__worker_thread.is_alive():
            self.__worker_thread.join(timeout=1.0)
            self.__worker_thread = None

    def __worker_loop(self):
        while self.__running:
            try:
                task = self.__task_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if task is None:
                self.__task_queue.task_done()
                break

            func, args, kwargs, result_holder, completion_event = task
            self.__is_processing = True
            try:
                with self.__ia_lock:
                    res = func(*args, **kwargs)
                    result_holder['result'] = res
                    result_holder['success'] = True
            except Exception as e:
                result_holder['exception'] = e
                result_holder['success'] = False
                print(f"Erreur worker gestIA : {e}")
            finally:
                self.__is_processing = False
                completion_event.set()
                self.__task_queue.task_done()

    def __submit_task(self, func, *args, **kwargs):
        if not self.__ia_mode_enabled:
            return func(*args, **kwargs)

        if not self.__running:
            self.__start_worker()

        result_holder = {}
        completion_event = threading.Event()
        self.__task_queue.put((func, args, kwargs, result_holder, completion_event))
        completion_event.wait()

        if result_holder.get('success'):
            return result_holder['result']
        elif 'exception' in result_holder:
            raise result_holder['exception']
        else:
            return None

    def get_queue_size(self):
        return self.__task_queue.qsize() + (1 if self.__is_processing else 0)

    def is_busy(self):
        return self.__is_processing or not self.__task_queue.empty()

    def unloadIA(self):
        """Désinstancie proprement le worker et le modèle IA en mémoire."""
        self.stop_worker()
        if self.__ia_loader is not None:
            self.__ia_loader.unload_model()
            del self.__ia_loader
            self.__ia_loader = None
        self.__ia_mode_enabled = False

    def loadIA(self):
        user_conf = self.__gestionnaire.getUserConf()
        model_name = user_conf.get_ia_model()
        if model_name != "":
            try:
                if model_name in self.get_list_model_download():
                    # Si un modèle est déjà chargé, on le désinstancie d'abord
                    if self.__ia_loader is not None or self.__ia_mode_enabled:
                        self.unloadIA()

                    self.__ia_loader = ArreraIALoad()
                    self.__ia_loader.load_model_gguf(
                        model_path=self.__downloader_model.get_path_model(model_name),
                        n_ctx=8192
                    )

                    prompt_dynamique = self.__generate_main_prompt()
                    if self.__ia_loader.add_system_instruction(prompt_dynamique):
                        self.__ia_mode_enabled = True
                        self.__start_worker()
                        return True
                    else:
                        self.unloadIA()
                        return False
                else:
                    self.unloadIA()
                    return False
            except Exception as e:
                #print(f"Erreur fatale dans loadIA : {e}")
                self.unloadIA()
                return False
        else :
            self.unloadIA()
            return False

    def load_help(self,help:str):
        if self.__ia_mode_enabled:
             if help in self.__dict_help_file.keys():
                 return self.__ia_loader.load_help_file(self.__dir_ia_instruction+self.__dict_help_file[help])
             else :
                 return False
        else :
            return False

    def load_additional_instructions(self, prompt_text_or_path: str) -> bool:
        """
        Permet d'injecter des instructions ou des règles système supplémentaires dans le prompt
        principal de l'IA (par exemple les définitions d'interfaces GUI ou règles de dialogue).

        :param prompt_text_or_path: Chaîne contenant directement les instructions ou chemin vers un fichier texte (.txt).
        :return: True si l'instruction a été ajoutée (et appliquée si l'IA est active), False sinon.
        """
        if not prompt_text_or_path or not isinstance(prompt_text_or_path, str):
            return False

        content = ""
        # 1. Vérifie si l'argument est un chemin de fichier existant
        if os.path.isfile(prompt_text_or_path):
            try:
                with open(prompt_text_or_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
            except Exception as e:
                print(f"Erreur lecture fichier instructions supplémentaires ({prompt_text_or_path}) : {e}")
                return False
        else:
            # 2. Sinon, on considère que c'est directement une chaîne de texte
            content = prompt_text_or_path.strip()

        if not content:
            return False

        # 3. Évite les doublons
        if content not in self.__additional_instructions:
            self.__additional_instructions.append(content)

        # 4. Si l'IA est déjà active, recharger l'instruction système
        if self.__ia_mode_enabled and self.__ia_loader is not None:
            return self.__submit_task(self.__internal_reload_main_prompt)

        return True

    def __internal_reload_main_prompt(self) -> bool:
        try:
            self.__ia_loader.unload_help()
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
                return True
            return False
        except Exception as e:
            print(f"Erreur mise à jour instructions système IA : {e}")
            return False

    def send_request_ia(self, requette: str):
        if not self.__ia_mode_enabled:
            self.__model_reponse_ok = False
            return False
        return self.__submit_task(self.__internal_send_request_ia, requette)

    def __internal_send_request_ia(self, requette: str):
        try:
            self.__reponse_ia = self.__ia_loader.send_request(requette)

            if self.__reponse_ia is not None:
                self.__model_reponse_ok = True
                return True
            else:
                self.__model_reponse_ok = False
                return False

        except Exception as e:
            self.__model_reponse_ok = False
            print(f"Erreur lors de l'appel IA : {e}")
            return False

    def __extract_json_dict(self, raw_reponse: str):
        if not raw_reponse or not isinstance(raw_reponse, str):
            return None
        try:
            start_idx = raw_reponse.find('{')
            end_idx = raw_reponse.rfind('}')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = raw_reponse[start_idx:end_idx + 1]
                return json.loads(json_str)
            return json.loads(raw_reponse)
        except Exception as e:
            print(f"Erreur decodage JSON IA : {e}")
            return None

    def correted_text(self,text:str):
        if not self.__ia_mode_enabled:
            self.__model_reponse_ok = False
            return False
        return self.__submit_task(self.__internal_correted_text, text)

    def __internal_correted_text(self,text:str):
        self.__ia_loader.unload_help()

        try:
            with open(self.__dir_ia_instruction+"prompt_orthographe.txt", 'r', encoding='utf-8') as f:
                content = f.read()
            raw_reponse = self.__ia_loader.send_request(content+"\n"+text, False)
            try:
                parsed = json.loads(raw_reponse)
                if "texte_corrige" in parsed:
                    self.__reponse_ia = parsed["texte_corrige"]
                else:
                    self.__reponse_ia = raw_reponse
            except json.JSONDecodeError:
                self.__reponse_ia = raw_reponse

            self.__model_reponse_ok = True
            self.__ia_loader.unload_help()
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            return True

        except Exception as e:
            self.__model_reponse_ok = False
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            print(e)
            return False

    def create_mail(self, objet: str, instructions: str = "", signature: str = ""):
        if not self.__ia_mode_enabled:
            self.__model_reponse_ok = False
            return None
        return self.__submit_task(self.__internal_create_mail, objet, instructions, signature)

    def __internal_create_mail(self, objet: str, instructions: str = "", signature: str = ""):
        self.__ia_loader.unload_help()
        try:
            with open(self.__dir_ia_instruction + "prompt_mail_creation.txt", 'r', encoding='utf-8') as f:
                instruction = f.read()

            prompt = f"Objet souhaité : {objet}\n"
            if instructions:
                prompt += f"Consignes / Détails : {instructions}\n"
            if signature:
                prompt += f"Expéditeur / Signature : {signature}\n"

            raw_reponse = self.__ia_loader.send_request(instruction + "\n\n" + prompt, False, True)
            data = self.__extract_json_dict(raw_reponse)
            self.__reponse_ia = data
            self.__model_reponse_ok = True if data is not None else False
            self.__ia_loader.unload_help()
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            return data
        except Exception as e:
            self.__model_reponse_ok = False
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            print(f"Erreur create_mail IA : {e}")
            return None

    def correct_mail(self, objet: str, mail: str):
        if not self.__ia_mode_enabled:
            self.__model_reponse_ok = False
            return None
        return self.__submit_task(self.__internal_correct_mail, objet, mail)

    def __internal_correct_mail(self, objet: str, mail: str):
        self.__ia_loader.unload_help()
        try:
            with open(self.__dir_ia_instruction + "prompt_mail_correction.txt", 'r', encoding='utf-8') as f:
                instruction = f.read()

            prompt = f"Objet : {objet}\n\nCorps du mail :\n{mail}"
            raw_reponse = self.__ia_loader.send_request(instruction + "\n\n" + prompt, False, True)
            data = self.__extract_json_dict(raw_reponse)
            self.__reponse_ia = data
            self.__model_reponse_ok = True if data is not None else False
            self.__ia_loader.unload_help()
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            return data
        except Exception as e:
            self.__model_reponse_ok = False
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            print(f"Erreur correct_mail IA : {e}")
            return None

    def reply_mail(self, objet: str, mail_recu: str, consigne_reponse: str, signature: str = ""):
        if not self.__ia_mode_enabled:
            self.__model_reponse_ok = False
            return None
        return self.__submit_task(self.__internal_reply_mail, objet, mail_recu, consigne_reponse, signature)

    def __internal_reply_mail(self, objet: str, mail_recu: str, consigne_reponse: str, signature: str = ""):
        self.__ia_loader.unload_help()
        try:
            with open(self.__dir_ia_instruction + "prompt_mail_reponse.txt", 'r', encoding='utf-8') as f:
                instruction = f.read()

            prompt = f"Objet du mail reçu : {objet}\n\nContenu du mail reçu :\n{mail_recu}\n\nConsigne de réponse : {consigne_reponse}\n"
            if signature:
                prompt += f"Expéditeur / Signature : {signature}\n"

            raw_reponse = self.__ia_loader.send_request(instruction + "\n\n" + prompt, False, True)
            data = self.__extract_json_dict(raw_reponse)
            self.__reponse_ia = data
            self.__model_reponse_ok = True if data is not None else False
            self.__ia_loader.unload_help()
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            return data
        except Exception as e:
            self.__model_reponse_ok = False
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            print(f"Erreur reply_mail IA : {e}")
            return None

    def deduplicate_actu(self, articles: list) -> list:
        if not articles or not isinstance(articles, list):
            return articles
        if not self.__ia_mode_enabled:
            self.__model_reponse_ok = False
            return articles
        return self.__submit_task(self.__internal_deduplicate_actu, articles)

    def __internal_deduplicate_actu(self, articles: list) -> list:
        self.__ia_loader.unload_help()

        try:
            with open(self.__dir_ia_instruction + "prompt_dedoublonnage.txt", 'r', encoding='utf-8') as f:
                content = f.read()

            truncated_articles = []
            for art in articles:
                new_art = art.copy()
                if "description" in new_art and isinstance(new_art["description"], str):
                    if len(new_art["description"]) > 150:
                        new_art["description"] = new_art["description"][:147] + "..."
                truncated_articles.append(new_art)

            articles_json = json.dumps(truncated_articles, ensure_ascii=False)
            
            if len(articles_json) > 10000:
                articles_json = articles_json[:10000] + '...}]'
                
            request_text = f"{content}\n\n{articles_json}"

            raw_reponse = self.__ia_loader.send_request(request_text, False)

            start_idx = raw_reponse.find('[')
            end_idx = raw_reponse.rfind(']')

            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = raw_reponse[start_idx:end_idx + 1]
                clean_articles = json.loads(json_str)
                if isinstance(clean_articles, list):
                    self.__reponse_ia = raw_reponse
                    self.__model_reponse_ok = True
                    self.__ia_loader.unload_help()
                    if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                        self.__ia_mode_enabled = True
                    return clean_articles

        except Exception as e:
            print(f"Erreur lors du dédoublonnage par l'IA : {e}")

        self.__model_reponse_ok = False
        self.__ia_loader.unload_help()
        if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
            self.__ia_mode_enabled = True
        return articles

    def __generate_main_prompt(self):
        conf = self.__gestionnaire.getConfigFile()

        prompt = f"""Tu es {conf.name}, un assistant virtuel créé par {conf.createur}. Ton but est : {conf.bute}.
            Tu fonctionnes comme le routeur principal du système.
            Tu DOIS IMPÉRATIVEMENT répondre UNIQUEMENT par un objet JSON valide. Ne génère aucun texte avant ou après le JSON.
        
            Format JSON attendu :
            {{
                "action": "nom_de_la_fonction",
                "args": ["argument_1", "argument_2"],
                "reponse": "À UTILISER UNIQUEMENT SI action='reponse_simple'. Texte de réponse conversationnelle."
            }}
        
            Voici la liste stricte des actions autorisées selon la configuration active :
            """
        prompt += self.__gestionnaire.getGestFNC().get_prompt()
        prompt += self.__gestionnaire.getGestGUI().get_prompt()

        for add_prompt in self.__additional_instructions:
            prompt += "\n" + add_prompt

        prompt += """
            Règles strictes :
            1. Choisis l'action la plus pertinente en fonction de la demande de l'utilisateur.
            2. Si une action nécessite des arguments, fournis-les dans le tableau "args". Sinon, laisse le tableau vide [].
            3. NE REMPLIS la clé "reponse" QUE SI l'action choisie est "reponse_simple".
            """
        return prompt

    def classify_intent(self, requete: str) -> str:
        if not self.__ia_mode_enabled:
            return "COMPLEXE"
        return self.__submit_task(self.__internal_classify_intent, requete)

    def __internal_classify_intent(self, requete: str) -> str:
        self.__ia_loader.unload_help()
        
        prompt_classification = f"""Tu es un classificateur d'intention ultra-rapide.
            Analyse la phrase suivante et réponds STRICTEMENT avec l'un des formats suivants (en majuscules, séparé par des espaces) :
            
            1. Météo : METEO [MOMENT] [LIEU]
               - MOMENT : MAINTENANT ou DEMAIN
               - LIEU : LOCATE, DOMICILE, TRAVAIL, ou le nom d'une ville précise (ex: PARIS)
               - Exemple : METEO MAINTENANT LOCATE
            
            2. Température : TEMPERATURE [MOMENT] [LIEU]
               - MOMENT : MAINTENANT ou DEMAIN
               - LIEU : LOCATE, DOMICILE, TRAVAIL, ou le nom d'une ville (ex: LYON)
               - Exemple : TEMPERATURE DEMAIN DOMICILE
            
            3. Actualité : ACTU [THEME]
               - THEME : TOUT, TECH, GENERALISTE, SCIENCE, SPORT, ou CULTURE
               - Exemple : ACTU TECH
            
            4. Radio : RADIO [ACTION/NOM]
               - Pour arrêter : RADIO STOP
               - Pour écouter, choisis dans cette liste : EUROPE 1, EUROPE 2, FRANCE INFO, FRANCE INTER, FRANCE MUSIQUE, FRANCE CULTURE, FRANCE BLEU, FUN RADIO, NRJ, RFM, NOSTALGIE, SKYROCK, RTL
               - Exemple : RADIO NRJ
            
            5. Heure et Date : HEURE
               - S'il demande l'heure, le jour ou la date.
               - Exemple : HEURE
            
            6. Minuteur : MINUTEUR
               - S'il demande un minuteur ou un chronomètre.
               - Exemple : MINUTEUR
            
            7. Arrêt / Au revoir : ARRET
               - S'il veut éteindre, se fermer ou dit au revoir (ex: "Arrête-toi", "Éteins", "Au revoir").
               - ATTENTION : Ne confonds pas "Arrera" (le nom de l'organisation) avec "Arrêt".
               - Exemple : ARRET
            
            8. Interface / GUI : GUI [NOM_GUI]
               - S'il veut ouvrir une interface graphique.
               - NOM_GUI doit être parmi : CALCULATRICE, LECTURE, ORTHOGRAPHE, TRADUCTEUR, AGENDA, TACHE, WORK, TACHE_PROJET, DOWNLOAD.
               - ATTENTION : Si l'utilisateur demande de lister ses projets, de créer, ou d'ouvrir un projet PRÉCIS (ex: "Ouvre le projet Alpha"), ce n'est PAS une ouverture d'interface globale. Tu DOIS répondre COMPLEXE.
               - Exemple : GUI CALCULATRICE
            
            9. Autre : COMPLEXE
               - Pour toute autre demande (ouvrir un projet, calculer, chercher sur internet, traduire, etc.) ou si tu n'es pas sûr.
            
            Phrase à classer : "{requete}"
            
            Règle absolue : Ne réponds RIEN D'AUTRE que la pseudo-commande choisie. Aucun point, aucune phrase. Juste les mots-clés demandés.
        """

        try:
            reponse = self.__ia_loader.send_request(prompt_classification, False, False)
            mot_cle = reponse.strip().upper()
            
            self.__ia_loader.unload_help()
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
                
            premier_mot = mot_cle.split(" ")[0]
            mots_autorises = ["METEO", "TEMPERATURE", "ACTU", "RADIO", "HEURE", "ARRET", "MINUTEUR", "GUI"]
            
            if premier_mot in mots_autorises:
                if mot_cle == "GUI WORK":
                    mots_work_complexe = ["projet", "project", "tableur", "excel",
                                          "word", "docx", "ferme", "crée", "cree",
                                          "créer", "creer", "liste", "lister",
                                          "fichier", "ouvre le projet", "ferme le projet",
                                          "ouvre un", "ouvrir le projet", "ouvrir un"]
                    requete_lower = requete.lower()
                    for mot in mots_work_complexe:
                        if mot in requete_lower:
                            return "COMPLEXE"
                return mot_cle
            else:
                requete_lower = requete.lower()

                # Garde-fou ACTU : si l'IA n'a pas reconnu une demande d'actus
                mots_actu = ["actualité", "actualite", "actualités", "actualites",
                             "actu", "actus", "news", "info", "infos",
                             "journal", "nouvelles", "presse",
                             "quoi de neuf", "quoi de nouveau"]
                theme_map = {
                    "tech": "TECH", "techno": "TECH", "technologie": "TECH",
                    "science": "SCIENCE", "scientifique": "SCIENCE",
                    "sport": "SPORT", "sportif": "SPORT", "sportive": "SPORT",
                    "culture": "CULTURE", "culturel": "CULTURE", "culturelle": "CULTURE",
                    "généraliste": "GENERALISTE", "generaliste": "GENERALISTE", "général": "GENERALISTE", "general": "GENERALISTE"
                }
                for mot_actu in mots_actu:
                    if mot_actu in requete_lower:
                        theme_found = "TOUT"
                        for mot_theme, code_theme in theme_map.items():
                            if mot_theme in requete_lower:
                                theme_found = code_theme
                                break
                        return f"ACTU {theme_found}"

                # Garde-fou GUI : si l'IA n'a pas reconnu une demande d'ouverture d'interface
                mots_declencheurs_gui = ["ouvre", "ouvrir", "montre", "montrer",
                                          "affiche", "afficher", "lance", "lancer",
                                          "démarre", "demarrer", "démarrer",
                                          "active", "activer"]
                gui_map = {
                    # Calculatrice
                    "calculatrice": "CALCULATRICE", "calculette": "CALCULATRICE", "calcul": "CALCULATRICE",
                    # Lecture
                    "lecture": "LECTURE", "lecteur": "LECTURE",
                    # Orthographe
                    "orthographe": "ORTHOGRAPHE", "correcteur": "ORTHOGRAPHE",
                    # Traducteur
                    "traducteur": "TRADUCTEUR", "traduction": "TRADUCTEUR",
                    # Agenda
                    "agenda": "AGENDA", "calendrier": "AGENDA",
                    # Tâches
                    "tache": "TACHE", "tâche": "TACHE", "taches": "TACHE", "tâches": "TACHE",
                    "gestionnaire de tache": "TACHE", "gestionnaire de tâche": "TACHE",
                    # Work
                    "arrera work": "WORK", "interface de travail": "WORK", "espace de travail": "WORK",
                    # Download
                    "download": "DOWNLOAD", "téléchargement": "DOWNLOAD", "telechargement": "DOWNLOAD",
                    "arrera download": "DOWNLOAD",
                }

                # Vérifier qu'un mot déclencheur est présent
                has_trigger = any(mot in requete_lower for mot in mots_declencheurs_gui)
                if has_trigger:
                    # Chercher le nom de GUI le plus long en premier (pour matcher "arrera work" avant "work")
                    for gui_name, gui_code in sorted(gui_map.items(), key=lambda x: len(x[0]), reverse=True):
                        if gui_name in requete_lower:
                            return f"GUI {gui_code}"

                return "COMPLEXE"
            
        except Exception as e:
            print(f"Erreur lors de la classification IA : {e}")
            self.__ia_loader.unload_help()
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            return "COMPLEXE"

    def generate_final_response(self, requete: str, donnees_systeme: str) -> str:
        if not self.__ia_mode_enabled:
            return ""
        return self.__submit_task(self.__internal_generate_final_response, requete, donnees_systeme)

    def __internal_generate_final_response(self, requete: str, donnees_systeme: str) -> str:
        self.__ia_loader.unload_help()

        first_name_user = self.__gest_user.getFirstnameUser()
        last_name_user = self.__gest_user.getLastnameUser()
        gender = self.__gest_user.getGenre()

        personnalite = self.__gestionnaire.getLanguageObjet().getPersonnalite()

        if requete.strip():
            contexte_requete = f'L\'utilisateur t\'a demandé : "{requete}"\nLe système a exécuté l\'action et a retourné le résultat suivant : \n"{donnees_systeme}"'
            tache = "Ta tâche : Formule une réponse naturelle et conversationnelle pour l'utilisateur pour lui transmettre ce résultat."
        else:
            contexte_requete = f'Directive système : "{donnees_systeme}"'
            tache = "Ta tâche : Rédige ce que tu vas dire spontanément à l'utilisateur en accomplissant cette directive."

        prompt_passe2 = f"""Tu es {self.__gestionnaire.getConfigFile().name}, l'assistant virtuel. 

            === L'UTILISATEUR ===
            Prénom : {first_name_user}
            Nom : {last_name_user}
            Genre : {gender}
            =====================

            === TA PERSONNALITÉ ===
            {personnalite}
            =======================
            
            {contexte_requete}
                        
            {tache}
            N'invente pas de fausses informations techniques, mais sois fluide, poli et humain. Ne génère pas de JSON, réponds directement en texte brut.
            """
        
        try:
            reponse = self.__ia_loader.send_request(prompt_passe2, False, False)
            self.__ia_loader.unload_help()
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            return reponse.strip().replace('"',"")
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse finale : {e}")
            self.__ia_loader.unload_help()
            if self.__ia_loader.add_system_instruction(self.__generate_main_prompt()):
                self.__ia_mode_enabled = True
            return "Une erreur est survenue lors de la formulation de la réponse."

    def get_state_ia_reponse(self):
        return self.__model_reponse_ok

    def get_reponse_ia(self):
        return self.__reponse_ia

    def get_ia_is_enable(self):
        return self.__ia_mode_enabled

    def get_list_model_available(self):
        return self.__downloader_model.get_model_list()

    def get_list_model_on_dir(self):
        return self.__downloader_model.get_model_on_dir()

    def gest_data_model(self,model:str):
        if model in self.get_list_model_available():
            return self.__downloader_model.get_data_model(model)
        else :
            return None,None,None

    def get_list_model_download(self):
        return self.__downloader_model.get_model_download()

    def download_model(self,model:str):
        return self.__downloader_model.download_model(model)

    def del_model(self,model:str):
        return self.__downloader_model.del_model(model)
