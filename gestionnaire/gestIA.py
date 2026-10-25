import json
import os
import re
import time
import queue
import threading
from gestionnaire.gestion import gestionnaire
from librairy.ArreraIALoad import ArreraIALoad
from librairy.model_downloader import *
from librairy.resource_lib import resource_lib

class gestIA :
    def __init__(self,gestionnaire:gestionnaire):

        self.__gestionnaire =  gestionnaire

        self.__ia_mode_enabled = False
        self.__ia_loader : ArreraIALoad = None

        self.__reponse_ia = ""

        self.__model_reponse_ok = False

        ia_os_dir = bool(getattr(gestionnaire.getConfigFile(), "ia_os_directory", False))
        self.__downloader_model = model_downloader(ia_os_directory=ia_os_dir)

        self.__gest_user = gestionnaire.getUserConf()

        self.__dir_ia_instruction = resource_lib().resource_path("instruction_ia") + "/"

        self.__dict_help_file = {"orthographe":"prompt_orthographe.txt",
                                 "dedoublonnage":"prompt_dedoublonnage.txt",
                                 "mail_creation":"prompt_mail_creation.txt",
                                 "mail_correction":"prompt_mail_correction.txt",
                                 "mail_reponse":"prompt_mail_reponse.txt"}

        self.__additional_instructions: list[str] = []

        # Gestion de la file d'attente, du Lazy Loading et de l'Auto-Unload
        self.__task_queue = queue.Queue()
        self.__ia_lock = threading.Lock()
        self.__worker_thread = None
        self.__running = False
        self.__is_processing = False
        self.__active_model_path = None
        self.__idle_timeout = 180
        self.__last_used_time = 0.0

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

    def __ensure_model_loaded(self):
        if self.__ia_loader is not None and not self.__ia_loader.is_model_loaded():
            if self.__active_model_path and os.path.isfile(self.__active_model_path):
                self.__ia_loader.load_model_gguf(
                    model_path=self.__active_model_path,
                    n_ctx=3072
                )

    def set_idle_timeout(self, seconds: int):
        self.__idle_timeout = max(0, int(seconds))

    def __worker_loop(self):
        while self.__running:
            try:
                task = self.__task_queue.get(timeout=0.5)
            except queue.Empty:
                # Auto-Unload : si le modèle est chargé et inactif depuis __idle_timeout secondes
                if (
                    self.__idle_timeout > 0
                    and self.__ia_loader is not None
                    and self.__ia_loader.is_model_loaded()
                    and self.__last_used_time > 0
                    and (time.time() - self.__last_used_time) >= self.__idle_timeout
                ):
                    with self.__ia_lock:
                        self.__ia_loader.unload_model(keep_instructions=True)
                        self.__last_used_time = 0.0
                continue
            if task is None:
                self.__task_queue.task_done()
                break
            func, args, kwargs, result_holder, completion_event = task
            self.__is_processing = True
            try:
                with self.__ia_lock:
                    self.__ensure_model_loaded()
                    res = func(*args, **kwargs)
                    self.__last_used_time = time.time()
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
        self.stop_worker()
        if self.__ia_loader is not None:
            self.__ia_loader.unload_model(keep_instructions=False)
            del self.__ia_loader
            self.__ia_loader = None
        self.__active_model_path = None
        self.__last_used_time = 0.0
        self.__ia_mode_enabled = False

    def loadIA(self):
        user_conf = self.__gestionnaire.getUserConf()
        model_name = user_conf.get_ia_model()
        if model_name != "":
            try:
                if model_name in self.get_list_model_download():
                    model_path = self.__downloader_model.get_path_model(model_name)
                    if not model_path or not os.path.isfile(model_path):
                        self.unloadIA()
                        return False
                    # Si un modèle est déjà configuré, on le nettoie d'abord
                    if self.__ia_loader is not None or self.__ia_mode_enabled:
                        self.unloadIA()
                    self.__active_model_path = model_path
                    self.__ia_loader = ArreraIALoad()
                    # Lazy Loading : on prépare uniquement le prompt système au boot.
                    # Les poids GGUF seront chargés automatiquement à la 1ère requête dans __worker_loop.
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
            except Exception:
                self.unloadIA()
                return False
        else:
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

    def reload_main_prompt(self) -> bool:
        """Recharge le prompt système principal (utile après l'ajout d'un GuiManager)."""
        if self.__ia_mode_enabled and self.__ia_loader is not None:
            return self.__submit_task(self.__internal_reload_main_prompt)
        return False

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

        # Inclure le contexte récent de la session pour résoudre les pronoms et références
        session_ctx = self.__gestionnaire.getGestSession().getPromptContext()
        if session_ctx:
            requete_avec_contexte = f"{session_ctx}\nDemande actuelle de l'utilisateur : {requette}"
        else:
            requete_avec_contexte = requette

        return self.__submit_task(self.__internal_send_request_ia, requete_avec_contexte)

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

    def __internal_correted_text(self, text: str):
        try:
            with open(self.__dir_ia_instruction + "prompt_orthographe.txt", 'r', encoding='utf-8') as f:
                content = f.read()
            raw_reponse = self.__ia_loader.send_request(
                content + "\n" + text, False, True, max_tokens=512, use_system_context=False
            )
            try:
                parsed = json.loads(raw_reponse)
                if "texte_corrige" in parsed:
                    self.__reponse_ia = parsed["texte_corrige"]
                else:
                    self.__reponse_ia = raw_reponse
            except json.JSONDecodeError:
                self.__reponse_ia = raw_reponse

            self.__model_reponse_ok = True
            return True

        except Exception as e:
            self.__model_reponse_ok = False
            print(e)
            return False

    def create_mail(self, objet: str, instructions: str = "", signature: str = ""):
        if not self.__ia_mode_enabled:
            self.__model_reponse_ok = False
            return None
        return self.__submit_task(self.__internal_create_mail, objet, instructions, signature)

    def __internal_create_mail(self, objet: str, instructions: str = "", signature: str = ""):
        try:
            with open(self.__dir_ia_instruction + "prompt_mail_creation.txt", 'r', encoding='utf-8') as f:
                instruction = f.read()

            prompt = f"Objet souhaité : {objet}\n"
            if instructions:
                prompt += f"Consignes / Détails : {instructions}\n"
            if signature:
                prompt += f"Expéditeur / Signature : {signature}\n"

            raw_reponse = self.__ia_loader.send_request(
                instruction + "\n\n" + prompt, False, True, max_tokens=512, use_system_context=False
            )
            data = self.__extract_json_dict(raw_reponse)
            self.__reponse_ia = data
            self.__model_reponse_ok = True if data is not None else False
            return data
        except Exception as e:
            self.__model_reponse_ok = False
            print(f"Erreur create_mail IA : {e}")
            return None

    def correct_mail(self, objet: str, mail: str):
        if not self.__ia_mode_enabled:
            self.__model_reponse_ok = False
            return None
        return self.__submit_task(self.__internal_correct_mail, objet, mail)

    def __internal_correct_mail(self, objet: str, mail: str):
        try:
            with open(self.__dir_ia_instruction + "prompt_mail_correction.txt", 'r', encoding='utf-8') as f:
                instruction = f.read()

            prompt = f"Objet : {objet}\n\nCorps du mail :\n{mail}"
            raw_reponse = self.__ia_loader.send_request(
                instruction + "\n\n" + prompt, False, True, max_tokens=512, use_system_context=False
            )
            data = self.__extract_json_dict(raw_reponse)
            self.__reponse_ia = data
            self.__model_reponse_ok = True if data is not None else False
            return data
        except Exception as e:
            self.__model_reponse_ok = False
            print(f"Erreur correct_mail IA : {e}")
            return None

    def reply_mail(self, objet: str, mail_recu: str, consigne_reponse: str, signature: str = ""):
        if not self.__ia_mode_enabled:
            self.__model_reponse_ok = False
            return None
        return self.__submit_task(self.__internal_reply_mail, objet, mail_recu, consigne_reponse, signature)

    def __internal_reply_mail(self, objet: str, mail_recu: str, consigne_reponse: str, signature: str = ""):
        try:
            with open(self.__dir_ia_instruction + "prompt_mail_reponse.txt", 'r', encoding='utf-8') as f:
                instruction = f.read()

            prompt = f"Objet du mail reçu : {objet}\n\nContenu du mail reçu :\n{mail_recu}\n\nConsigne de réponse : {consigne_reponse}\n"
            if signature:
                prompt += f"Expéditeur / Signature : {signature}\n"

            raw_reponse = self.__ia_loader.send_request(
                instruction + "\n\n" + prompt, False, True, max_tokens=512, use_system_context=False
            )
            data = self.__extract_json_dict(raw_reponse)
            self.__reponse_ia = data
            self.__model_reponse_ok = True if data is not None else False
            return data
        except Exception as e:
            self.__model_reponse_ok = False
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
            raw_reponse = self.__ia_loader.send_request(
                request_text, False, True, max_tokens=512, use_system_context=False
            )

            start_idx = raw_reponse.find('[')
            end_idx = raw_reponse.rfind(']')

            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = raw_reponse[start_idx:end_idx + 1]
                clean_articles = json.loads(json_str)
                if isinstance(clean_articles, list):
                    self.__reponse_ia = raw_reponse
                    self.__model_reponse_ok = True
                    return clean_articles

        except Exception as e:
            print(f"Erreur lors du dédoublonnage par l'IA : {e}")

        self.__model_reponse_ok = False
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
        gui = self.__gestionnaire.getGestGUI()
        if gui is not None:
            prompt += gui.get_prompt()

        for add_prompt in self.__additional_instructions:
            prompt += "\n" + add_prompt

        prompt += "\n" + self.__gestionnaire.getGestMemoire().getPromptContext()

        prompt += """
            Règles strictes de décision :
            1. Pour TOUTE question générale, demande d'information, question de culture générale, explication, discussion ou question de suivi de conversation (ex: "qui est...", "quelle est...", "quel âge...", "comment...", "pourquoi..."), choisis TOUJOURS "action": "reponse_simple" et rédige ta réponse complète et précise directement dans la clé "reponse".
            2. N'utilise l'action "recherche" QUE si l'utilisateur demande explicitement de faire une recherche sur internet ou d'ouvrir un navigateur web (ex: "cherche sur Google", "recherche sur le net").
            3. Choisis une action spécifique (tache, meteo, work, calculatrice, etc.) uniquement si la demande correspond directement aux outils disponibles.
            4. Si une action nécessite des arguments, fournis-les dans le tableau "args". Sinon, laisse le tableau vide [].
            5. NE REMPLIS la clé "reponse" QUE SI l'action choisie est "reponse_simple".
            """
        return prompt

    def __fast_preclassify(self, requete: str):
        """
        Pré-classification déterministe en Python pur (0 ms, 0 appel LLM).
        Retourne l'intent directement si la demande est non-ambiguë, ou None s'il faut interroger le LLM.
        """
        req_lower = requete.lower().strip()
        # 1. Commandes PROJET ou MÉMOIRE déjà gérées par les pré-filtres de IARouter -> direct COMPLEXE sans Passe 0 LLM
        mots_prefiltre_complexe = [
            "ouvre le projet", "ouvrir le projet", "ouvre mon projet", "lance le projet",
            "ferme le projet", "fermer le projet", "quitte le projet",
            "crée le projet", "créer le projet", "cree le projet", "creer le projet",
            "crée un projet", "créer un projet", "cree un projet", "creer un projet", "nouveau projet",
            "liste mes projets", "lister mes projets", "liste les projets", "mes projets", "quels sont mes projets",
            "liste mes souvenirs", "lister mes souvenirs", "mes souvenirs", "quels sont mes souvenirs",
            "qu'as tu retenu", "qu as tu retenu", "qu'est ce que tu sais sur moi", "que sais tu sur moi",
            "efface toute ta memoire", "efface toute ta mémoire", "vide ta memoire", "vide ta mémoire", "oublie tout",
            "retiens que ", "retiens qu'", "rappelle toi que ", "rappelle-toi que ",
            "garde en memoire", "garde en mémoire", "memorise que ", "mémorise que ",
            "oublie le souvenir ", "supprime le souvenir ", "efface le souvenir ",
            "ouvre le fichier arrera markdown", "ouvrir le fichier arrera markdown",
            "ouvre le markdown du projet", "ouvrir le markdown du projet",
            "ouvre l'arrera markdown du projet", "ouvre arrera markdown du projet",
            "ouvre dans arrera markdown", "ouvrir dans arrera markdown"
        ]
        if any(m in req_lower for m in mots_prefiltre_complexe):
            return "COMPLEXE"
        # 2. Détection directe HEURE (si formulation explicite sans faux positifs)
        patterns_heure_directe = [
            "quelle heure est il", "quelle heure est-il", "il est quelle heure",
            "donne moi l'heure", "donne-moi l'heure", "donne l'heure",
            "quel jour sommes nous", "quel jour sommes-nous", "quel jour on est",
            "quelle est la date", "la date d'aujourd'hui", "la date du jour"
        ]
        if any(p in req_lower for p in patterns_heure_directe):
            return "HEURE"
        # 3. Détection directe ACTU (avec mots entiers et sans mots d'exclusion ni questions encyclopédiques)
        mots_exclusion_actu = [
            "presse-papier", "presse papier", "projet", "fichier", "tache", "tâche",
            "tableur", "word", "sur le langage", "sur python", "sur linux", "comment", "pourquoi", "qui est"
        ]
        if not any(excl in req_lower for excl in mots_exclusion_actu):
            if re.search(r"\b(actualit[eé]s?|actus?|news|journal|nouvelles|presse)\b|quoi de neuf|quoi de nouveau", req_lower):
                theme_map = {
                    "tech": "TECH", "techno": "TECH", "technologie": "TECH",
                    "science": "SCIENCE", "scientifique": "SCIENCE",
                    "sport": "SPORT", "sportif": "SPORT", "sportive": "SPORT",
                    "culture": "CULTURE", "culturel": "CULTURE", "culturelle": "CULTURE",
                    "généraliste": "GENERALISTE", "generaliste": "GENERALISTE", "général": "GENERALISTE", "general": "GENERALISTE"
                }
                theme_found = "TOUT"
                for mot_theme, code_theme in theme_map.items():
                    if re.search(rf"\b{re.escape(mot_theme)}\b", req_lower):
                        theme_found = code_theme
                        break
                return f"ACTU {theme_found}"
        # 4. Détection directe GUI (verbe d'ouverture + nom d'interface, sans mots complexes de projet/fichier)
        mots_declencheurs_gui = [
            "ouvre", "ouvrir", "montre", "montrer", "affiche", "afficher",
            "lance", "lancer", "démarre", "demarrer", "démarrer", "active", "activer"
        ]
        mots_work_complexe = [
            "projet", "project", "tableur", "excel", "word", "docx", "ferme",
            "crée", "cree", "créer", "creer", "liste", "lister", "fichier", "dossier",
            "repertoire", "code", "commande", "script", "terminal", "git", "commit",
            "init", "dépôt", "depot", "status", "main", "python", "retiens", "souvenir",
            "memoire", "rappelle", "oublie", "noter", "note", "enregistre"
        ]
        if any(mot in req_lower for mot in mots_declencheurs_gui) and not any(m in req_lower for m in mots_work_complexe):
            gui_map = {
                "calculatrice": "CALCULATRICE", "calculette": "CALCULATRICE",
                "lecture": "LECTURE", "lecteur": "LECTURE",
                "orthographe": "ORTHOGRAPHE", "correcteur": "ORTHOGRAPHE",
                "traducteur": "TRADUCTEUR", "traduction": "TRADUCTEUR",
                "agenda": "AGENDA", "calendrier": "AGENDA",
                "gestionnaire de tache": "TACHE", "gestionnaire de tâche": "TACHE",
                "arrera work": "WORK", "interface de travail": "WORK", "espace de travail": "WORK",
                "arrera download": "DOWNLOAD",
            }
            for gui_name, gui_code in sorted(gui_map.items(), key=lambda x: len(x[0]), reverse=True):
                if gui_name in req_lower:
                    return f"GUI {gui_code}"
        return None
    def classify_intent(self, requete: str) -> str:
        if not self.__ia_mode_enabled:
            return "COMPLEXE"
        fast_intent = self.__fast_preclassify(requete)
        if fast_intent is not None:
            return fast_intent
        return self.__submit_task(self.__internal_classify_intent, requete)

    def __internal_classify_intent(self, requete: str) -> str:
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
                - ATTENTION : Si l'utilisateur demande de lister ses projets, de créer ou ouvrir un projet, de créer un dossier, d'écrire/lire un fichier, ou d'exécuter une commande, ce n'est PAS une ouverture d'interface. Tu DOIS répondre STRICTEMENT COMPLEXE.
               - Exemple : GUI CALCULATRICE
            
            9. Autre : COMPLEXE
               - Pour toute autre demande (ouvrir un projet, calculer, chercher sur internet, traduire, etc.) ou si tu n'es pas sûr.
            
            Phrase à classer : "{requete}"
            
            Règle absolue : Ne réponds RIEN D'AUTRE que la pseudo-commande choisie. Aucun point, aucune phrase. Juste les mots-clés demandés.
        """

        try:
            reponse = self.__ia_loader.send_request(
                prompt_classification, False, False, max_tokens=20, use_system_context=False
            )
            mot_cle = reponse.strip().upper()

            premier_mot = mot_cle.split(" ")[0]
            mots_autorises = ["METEO", "TEMPERATURE", "ACTU", "RADIO", "HEURE", "ARRET", "MINUTEUR", "GUI"]
            requete_lower = requete.lower().strip()

            if premier_mot in mots_autorises:
                # Garde-fou ARRET : éviter l'extinction sur une question ("comment arrêter une boucle...")
                if premier_mot == "ARRET":
                    mots_questions_code = [
                        "comment", "pourquoi", "quand", "quel", "quelle", "qui",
                        "boucle", "python", "script", "code", "programme", "fonction",
                        "erreur", "processus", "service", "serveur"
                    ]
                    if any(m in requete_lower for m in mots_questions_code):
                        return "COMPLEXE"
                    mots_arret_requis = [
                        "arret", "arrêt", "arrete", "arrête", "arreter", "arrêter",
                        "stop", "stoppe", "eteins", "éteins", "eteindre", "éteindre",
                        "ferme", "fermer", "quitte", "quitter", "au revoir", "aurevoir",
                        "bye", "ciao", "adieu", "bonne nuit", "bonne soiree", "bonne soirée"
                    ]
                    if not any(m in requete_lower for m in mots_arret_requis):
                        return "COMPLEXE"

                # Garde-fou HEURE : rejeter les questions de durée ou d'horaires d'ouverture
                elif premier_mot == "HEURE":
                    faux_positifs_heure = [
                        "combien d'heure", "combien d heure", "combien de jour",
                        "ouvre", "ferme", "commence", "finit", "termine",
                        "naissance", "création", "creation", "histoire", "km/h", "par heure"
                    ]
                    mots_temps = ["heure", "jour", "date", "aujourd'hui", "aujourd hui"]
                    if any(fp in requete_lower for fp in faux_positifs_heure) or not any(
                            m in requete_lower for m in mots_temps):
                        return "COMPLEXE"

                # Garde-fou METEO / TEMPERATURE : rejeter les questions scientifiques/cuisine/hardware
                elif premier_mot in ("METEO", "TEMPERATURE"):
                    faux_positifs_meteo = [
                        "fusion", "ébullition", "ebullition", "corps", "humain", "fièvre", "fievre",
                        "four", "cuisson", "recette", "cpu", "gpu", "processeur", "carte graphique", "eau"
                    ]
                    mots_meteo = [
                        "meteo", "météo", "temps", "temperature", "température",
                        "froid", "chaud", "pluie", "pleut", "pleuvoir", "neige",
                        "soleil", "vent", "orage", "degre", "degré", "dehors",
                        "prevision", "prévision", "alerte", "vigilance"
                    ]
                    if any(fp in requete_lower for fp in faux_positifs_meteo) or not any(
                            m in requete_lower for m in mots_meteo):
                        return "COMPLEXE"

                # Garde-fou RADIO : rejeter les questions encyclopédiques ou "radioactivité"
                elif premier_mot == "RADIO":
                    faux_positifs_radio = [
                        "radioactiv", "radiolog", "radiograph", "bouton radio",
                        "qui a", "comment", "pourquoi", "qu'est-ce", "qu est ce", "histoire", "invent"
                    ]
                    mots_radio = [
                        "radio", "nrj", "rtl", "rfm", "skyrock", "nostalgie", "fun radio",
                        "europe 1", "europe 2", "france info", "france inter",
                        "france musique", "france culture", "france bleu"
                    ]
                    if any(fp in requete_lower for fp in faux_positifs_radio) or not any(
                            m in requete_lower for m in mots_radio):
                        return "COMPLEXE"

                # Garde-fou MINUTEUR : si une durée chiffrée ou un contrôle chrono est demandé, envoyer vers IARouter
                elif premier_mot == "MINUTEUR":
                    mots_minuteur = ["minuteur", "chrono", "chronomètre", "chronometre", "compte à rebours",
                                     "compte a rebours", "timer"]
                    if not any(m in requete_lower for m in mots_minuteur):
                        return "COMPLEXE"
                    if any(c.isdigit() for c in requete_lower) or "chrono" in requete_lower:
                        return "COMPLEXE"

                # Garde-fou ACTU (quand prédit par l'IA) : vérifier que ce n'est pas "actuellement" / "informatique"
                elif premier_mot == "ACTU":
                    if not re.search(
                            r"\b(actualit[eé]s?|actus?|news|infos?|journal|nouvelles|presse)\b|quoi de neuf|quoi de nouveau",
                            requete_lower):
                        return "COMPLEXE"
                    if "presse-papier" in requete_lower or "presse papier" in requete_lower:
                        return "COMPLEXE"

                # Garde-fou GUI
                elif premier_mot == "GUI":
                    mots_declencheurs_gui = ["ouvre", "ouvrir", "montre", "montrer",
                                             "affiche", "afficher", "lance", "lancer",
                                             "démarre", "demarrer", "démarrer",
                                             "active", "activer", "interface"]
                    if not any(mot in requete_lower for mot in mots_declencheurs_gui):
                        return "COMPLEXE"

                    mots_work_complexe = ["projet", "project", "tableur", "excel",
                                          "word", "docx", "ferme", "crée", "cree",
                                          "créer", "creer", "liste", "lister",
                                          "fichier", "dossier", "repertoire", "code",
                                          "commande", "script", "terminal", "git",
                                          "commit", "init", "dépôt", "depot", "status",
                                          "main", "python",
                                          "retiens", "souvenir", "souvenirs", "memoire", "memoires",
                                          "rappelle", "oublie", "noter", "note", "enregistre", "enregistrer",
                                          "ouvre le projet", "ferme le projet",
                                          "ouvre un", "ouvrir le projet", "ouvrir un"]
                    for mot in mots_work_complexe:
                        if mot in requete_lower:
                            return "COMPLEXE"

                return mot_cle
            else:
                # Garde-fou ACTU : mots entiers uniquement (\b) et pas d'action projet/système
                mots_exclusion_actu = ["presse-papier", "presse papier", "projet", "fichier", "tache", "tâche",
                                       "tableur", "word"]
                if not any(excl in requete_lower for excl in mots_exclusion_actu):
                    if re.search(
                            r"\b(actualit[eé]s?|actus?|news|infos?|journal|nouvelles|presse)\b|quoi de neuf|quoi de nouveau",
                            requete_lower):
                        theme_map = {
                            "tech": "TECH", "techno": "TECH", "technologie": "TECH",
                            "science": "SCIENCE", "scientifique": "SCIENCE",
                            "sport": "SPORT", "sportif": "SPORT", "sportive": "SPORT",
                            "culture": "CULTURE", "culturel": "CULTURE", "culturelle": "CULTURE",
                            "généraliste": "GENERALISTE", "generaliste": "GENERALISTE", "général": "GENERALISTE",
                            "general": "GENERALISTE"
                        }
                        theme_found = "TOUT"
                        for mot_theme, code_theme in theme_map.items():
                            if re.search(rf"\b{re.escape(mot_theme)}\b", requete_lower):
                                theme_found = code_theme
                                break
                        return f"ACTU {theme_found}"

                # Garde-fou GUI : si l'IA n'a pas reconnu une demande d'ouverture d'interface
                mots_declencheurs_gui = ["ouvre", "ouvrir", "montre", "montrer",
                                         "affiche", "afficher", "lance", "lancer",
                                         "démarre", "demarrer", "démarrer",
                                         "active", "activer"]
                gui_map = {
                    "calculatrice": "CALCULATRICE", "calculette": "CALCULATRICE", "calcul": "CALCULATRICE",
                    "lecture": "LECTURE", "lecteur": "LECTURE",
                    "orthographe": "ORTHOGRAPHE", "correcteur": "ORTHOGRAPHE",
                    "traducteur": "TRADUCTEUR", "traduction": "TRADUCTEUR",
                    "agenda": "AGENDA", "calendrier": "AGENDA",
                    "tache": "TACHE", "tâche": "TACHE", "taches": "TACHE", "tâches": "TACHE",
                    "gestionnaire de tache": "TACHE", "gestionnaire de tâche": "TACHE",
                    "arrera work": "WORK", "interface de travail": "WORK", "espace de travail": "WORK",
                    "download": "DOWNLOAD", "téléchargement": "DOWNLOAD", "telechargement": "DOWNLOAD",
                    "arrera download": "DOWNLOAD",
                }

                has_trigger = any(mot in requete_lower for mot in mots_declencheurs_gui)
                if has_trigger:
                    for gui_name, gui_code in sorted(gui_map.items(), key=lambda x: len(x[0]), reverse=True):
                        if gui_name in requete_lower:
                            return f"GUI {gui_code}"

                return "COMPLEXE"
        except Exception as e:
            print(f"Erreur lors de la classification IA : {e}")
            return "COMPLEXE"

    def generate_final_response(self, requete: str, donnees_systeme: str) -> str:
        if not self.__ia_mode_enabled:
            return ""
        return self.__submit_task(self.__internal_generate_final_response, requete, donnees_systeme)

    def __clean_final_text(self, text: str) -> str:
        """Nettoie les préfixes de rôles et hallucinations de tours suivants sur les petits modèles."""
        if not text or not isinstance(text, str):
            return ""
        cleaned = text.strip().strip('"')

        # Couper si le modèle tente de générer la suite du dialogue ou répète une balise système
        for stop_marker in ["\nUtilisateur :", "\nUtilisateur:", "\nUser :", "\nUser:", "\n===", "=== "]:
            if stop_marker in cleaned:
                cleaned = cleaned.split(stop_marker, 1)[0].strip()

        # Retirer les préfixes parasites (ex: "Assistant : ", "Opale : ", "Réponse : ")
        conf_name = self.__gestionnaire.getConfigFile().name
        prefixes = [
            f"{conf_name} :", f"{conf_name}:",
            "Assistant :", "Assistant:",
            "Réponse :", "Réponse:", "Reponse :", "Reponse:"
        ]
        for pref in prefixes:
            if cleaned.lower().startswith(pref.lower()):
                cleaned = cleaned[len(pref):].strip()

        return cleaned.strip('"').strip()

    def __internal_generate_final_response(self, requete: str, donnees_systeme: str) -> str:
        if isinstance(donnees_systeme, list):
            donnees_systeme = "\n".join(str(x) for x in donnees_systeme if x and str(x).strip() and str(x) != "error")
        elif donnees_systeme is not None and not isinstance(donnees_systeme, str):
            donnees_systeme = str(donnees_systeme)

        first_name_user = self.__gest_user.getFirstnameUser()
        last_name_user = self.__gest_user.getLastnameUser()
        gender = self.__gest_user.getGenre()

        personnalite = self.__gestionnaire.getLanguageObjet().getPersonnalite()

        if requete.strip():
            if donnees_systeme and donnees_systeme.strip():
                contexte_requete = f'L\'utilisateur t\'a demandé : "{requete}"\nInformations ou résultat retourné par le système : \n"{donnees_systeme}"'
                tache = (
                    "Ta tâche : Formule une réponse naturelle, conversationnelle et complète pour l'utilisateur "
                    "en te basant STRICTEMENT sur le résultat retourné par le système ci-dessus. "
                    "Si ce résultat indique une erreur, une indisponibilité ou qu'il n'y a aucun élément (ex: aucune tâche, aucun événement), "
                    "dis-le fidèlement sans JAMAIS inventer de données ni réutiliser d'anciens résultats de l'historique."
                )
            else:
                contexte_requete = f'L\'utilisateur t\'a demandé : "{requete}"'
                tache = "Ta tâche : Réponds directement à la question ou remarque de l'utilisateur avec tes connaissances de manière naturelle, complète et polie."
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
            
            {self.__gestionnaire.getGestMemoire().getPromptContext()}
            
            {self.__gestionnaire.getGestSession().getPromptContext()}
            
            {contexte_requete}
                        
            {tache}
            RÈGLES STRICTES :
            - N'utilise les souvenirs de l'utilisateur que s'ils ont un rapport direct avec sa demande.
            - N'invente pas de fausses informations techniques, mais sois fluide, poli et humain.
            - Ne génère pas de JSON et ne préfixe pas ta réponse par ton nom, réponds directement en texte brut.
            """
        
        try:
            reponse = self.__ia_loader.send_request(
                prompt_passe2, False, False, max_tokens=384, use_system_context=False
            )
            return self.__clean_final_text(reponse)
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse finale : {e}")
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
        return self.__downloader_model.get_data_model(model)

    def get_list_model_download(self):
        return self.__downloader_model.get_model_download()

    def download_model(self,model:str):
        return self.__downloader_model.download_model(model)

    def del_model(self,model:str):
        return self.__downloader_model.del_model(model)

    def download_custom_model(self, name: str, url: str, description: str = "") -> bool:
        return self.__downloader_model.download_custom_model(name, url, description)

    def get_recommended_model(self) -> str:
        return self.__downloader_model.get_recommended_model()

    def get_hardware_recommendation(self) -> dict:
        return self.__downloader_model.get_hardware_recommendation()
