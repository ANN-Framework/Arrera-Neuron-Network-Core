import os
import json
import re


class gestMemoire:
    """
    Gestionnaire de mémoire explicite à long terme pour ArreraNeuronNetwork.
    Stocke les faits et préférences dans ~/.config/arrera-assistant/user-memory.json.
    Toutes les méthodes d'action renvoient un simple bool (True/False).
    """

    def __init__(self, gestionnaire):
        self.__gestionnaire = gestionnaire
        self.__osDect = gestionnaire.getOSObjet()
        self.__memories: list[str] = []
        self.__lastMessage = ""

        # 1. Définition du chemin multiplateforme
        if self.__osDect.osLinux() or self.__osDect.osMac():
            home = os.path.expanduser("~")
            self.__memoryFilePath = os.path.join(home, ".config/arrera-assistant/user-memory.json")
        elif self.__osDect.osWindows():
            home = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
            self.__memoryFilePath = os.path.join(home, "arrera-assistant/user-memory.json")
        else:
            self.__memoryFilePath = "user-memory.json"

        # 2. Création automatique du fichier s'il n'existe pas
        if not os.path.isfile(self.__memoryFilePath):
            try:
                os.makedirs(os.path.dirname(self.__memoryFilePath), exist_ok=True)
                with open(self.__memoryFilePath, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
            except Exception as e:
                self.__lastMessage = str(e)

        # 3. Chargement initial
        self.loadMemories()

    def getLastMessage(self) -> str:
        """Retourne le dernier message ou erreur."""
        return self.__lastMessage

    def loadMemories(self) -> list[str]:
        """Charge les souvenirs depuis le fichier JSON."""
        if os.path.isfile(self.__memoryFilePath):
            try:
                with open(self.__memoryFilePath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.__memories = data
                    else:
                        self.__memories = []
            except Exception as e:
                self.__lastMessage = f"Erreur lecture mémoire : {e}"
                self.__memories = []
        return self.__memories

    @staticmethod
    def _normalize_str(text: str) -> str:
        s = str(text).lower().strip()
        replacements = {
            "é": "e", "è": "e", "ê": "e", "ë": "e",
            "à": "a", "â": "a", "ä": "a",
            "î": "i", "ï": "i",
            "ô": "o", "ö": "o",
            "ù": "u", "û": "u", "ü": "u",
            "ç": "c", "-": " ", "_": " ", "'": " ", "’": " "
        }
        for orig, rep in replacements.items():
            s = s.replace(orig, rep)
        return " ".join(s.split())

    def saveMemories(self) -> bool:
        """Sauvegarde les souvenirs dans le fichier JSON et recharge le prompt système de l'IA."""
        try:
            with open(self.__memoryFilePath, "w", encoding="utf-8") as f:
                json.dump(self.__memories, f, ensure_ascii=False, indent=2)
            try:
                self.__gestionnaire.getGestIA().reload_main_prompt()
            except Exception:
                pass
            return True
        except Exception as e:
            self.__lastMessage = f"Erreur sauvegarde mémoire : {e}"
            return False

    def addMemory(self, text: str) -> bool:
        """Ajoute un fait ou une préférence en mémoire."""
        nettoye = str(text).strip()
        # Retrait des guillemets éventuels
        if (nettoye.startswith('"') and nettoye.endswith('"')) or (nettoye.startswith("'") and nettoye.endswith("'")):
            nettoye = nettoye[1:-1].strip()

        # Retrait des préfixes conversationnels superflus
        for prefix in ["que ", "qu'", "qu’", "de ", "d'", "d’"]:
            if nettoye.lower().startswith(prefix):
                nettoye = nettoye[len(prefix):].strip()

        if not nettoye:
            self.__lastMessage = "Le souvenir ne peut pas être vide."
            return False

        # Vérification des doublons (tolérant aux variations de casse/accents)
        norm_nouveau = self._normalize_str(nettoye)
        for souvenir in self.__memories:
            if self._normalize_str(souvenir) == norm_nouveau:
                self.__lastMessage = "Cette information est déjà enregistrée."
                return True

        self.__memories.append(nettoye)
        return self.saveMemories()

    def listMemories(self) -> str:
        """Retourne la liste lisible des souvenirs sous forme de chaîne de caractères."""
        self.loadMemories()
        if not self.__memories:
            return "Je n'ai actuellement aucun souvenir enregistré sur vous."
        lignes = [f"{i + 1}. {souvenir}" for i, souvenir in enumerate(self.__memories)]
        return "Voici ce que j'ai retenu sur vous :\n" + "\n".join(lignes)

    def deleteMemory(self, query: str) -> bool:
        """Supprime un souvenir par son numéro d'index (ex: '1', 'souvenir 1') ou par mot-clé."""
        self.loadMemories()
        query = str(query).strip()
        if not self.__memories:
            self.__lastMessage = "La mémoire est vide."
            return False

        # Nettoyage des guillemets et préfixes
        if (query.startswith('"') and query.endswith('"')) or (query.startswith("'") and query.endswith("'")):
            query = query[1:-1].strip()

        for prefix in ["que ", "qu'", "qu’", "le souvenir numero ", "le souvenir n° ", "le souvenir ", "souvenir "]:
            if query.lower().startswith(prefix):
                query = query[len(prefix):].strip()

        # Cas 1 : suppression par numéro d'index (ex: '1', 'le souvenir 1')
        match_digit = re.search(r'\b\d+\b', query)
        if match_digit:
            idx = int(match_digit.group()) - 1
            if 0 <= idx < len(self.__memories):
                self.__memories.pop(idx)
                return self.saveMemories()
            self.__lastMessage = "Numéro de souvenir invalide."
            return False

        # Cas 2 : suppression par mot-clé (comparaison normalisée)
        query_norm = self._normalize_str(query)
        for souvenir in list(self.__memories):
            s_norm = self._normalize_str(souvenir)
            if query_norm in s_norm or s_norm in query_norm:
                self.__memories.remove(souvenir)
                return self.saveMemories()

        # Cas 3 : suppression par correspondance des mots signifiants (>= 3 lettres)
        mots_cles = [m for m in query_norm.split() if len(m) >= 3]
        if mots_cles:
            for souvenir in list(self.__memories):
                s_norm = self._normalize_str(souvenir)
                if all(mot in s_norm for mot in mots_cles):
                    self.__memories.remove(souvenir)
                    return self.saveMemories()

        self.__lastMessage = f"Aucun souvenir correspondant à '{query}' trouvé."
        return False

    def clearMemories(self) -> bool:
        """Efface l'intégralité de la mémoire."""
        self.__memories = []
        return self.saveMemories()

    def getPromptContext(self) -> str:
        """Formate les souvenirs pour les injecter dans le prompt de l'IA."""
        if not self.__memories:
            return ""
        lignes = [f"- {m}" for m in self.__memories]
        return "\n=== CE QUE TU SAIS SUR L'UTILISATEUR (MÉMOIRE PERSISTANTE) ===\n" + "\n".join(lignes) + "\n=============================================================\n"