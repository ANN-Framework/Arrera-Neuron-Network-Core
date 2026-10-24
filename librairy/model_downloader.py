import requests
import os
import json
from librairy.dectectionOS import OS


class model_downloader:
    def __init__(self, ia_os_directory: bool = False):

        self.__dictModel = {
            "leger-gemma": {
                "name": "Gemma 4 E2B Q4_K_M",
                "url": "https://huggingface.co/bartowski/google_gemma-4-E2B-it-GGUF/resolve/main/google_gemma-4-E2B-it-Q4_K_M.gguf?download=true",
                "description": "Le tout dernier petit modèle 'Edge' Google Gemma 4. Ultra-rapide et parfait pour tourner de manière fluide sur le processeur (CPU) d'un PC sans carte graphique."
            },
            "moyen-gemma": {
                "name": "Gemma 3 12B Q4_K_M",
                "url": "https://huggingface.co/unsloth/gemma-3-12b-it-GGUF/resolve/main/gemma-3-12b-it-Q4_K_M.gguf?download=true",
                "description": "Modèle Google Gemma 3 très équilibré. Idéal pour exploiter un PC équipé d'une carte graphique classique (entre 8 et 12 Go de VRAM)."
            },
            "lourd-gemma": {
                "name": "Gemma 4 31B Q4_K_M",
                "url": "https://huggingface.co/bartowski/google_gemma-4-31B-it-GGUF/resolve/main/google_gemma-4-31B-it-Q4_K_M.gguf?download=true",
                "description": "Le nouveau fleuron de Google (Gemma 4). Très lourd et puissant, il nécessite une grosse carte graphique (16 à 24 Go de VRAM minimum) ou beaucoup de RAM vive."
            },
            "leger-mistral": {
                "name": "Ministral 3B Instruct Q4_K_M",
                "url": "https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512-GGUF/resolve/main/Ministral-3-3B-Instruct-2512-Q4_K_M.gguf?download=true",
                "description": "Petit modèle de la startup française Mistral. Très vif, parfait pour tourner de manière fluide sur un PC sans carte graphique dédiée (sur le CPU)."
            },
            "moyen-mistral": {
                "name": "Mistral Nemo 12B Instruct Q4_K_M",
                "url": "https://huggingface.co/bartowski/Mistral-Nemo-Instruct-2407-GGUF/resolve/main/Mistral-Nemo-Instruct-2407-Q4_K_M.gguf?download=true",
                "description": "Excellent modèle de 12 Milliards de paramètres. Le compromis idéal pour un PC équipé d'une carte graphique de milieu de gamme (8 à 12 Go de VRAM)."
            },
            "lourd-mistral": {
                "name": "Mistral Small 3 (24B) Instruct Q4_K_M",
                "url": "https://huggingface.co/bartowski/Mistral-Small-24B-Instruct-2501-GGUF/resolve/main/Mistral-Small-24B-Instruct-2501-Q4_K_M.gguf?download=true",
                "description": "Modèle avancé et très performant. Lourd, il nécessite une bonne carte graphique (au moins 16 Go de VRAM) ou beaucoup de RAM vive pour tourner confortablement."
            },
            "leger-llama": {
                "name": "LLaMA 3.2 3B Instruct Q4_K_M",
                "url": "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf?download=true",
                "description": "Petit modèle Meta très intelligent. Parfait pour tourner sur le processeur (CPU) d'un PC sans carte graphique, avec une excellente rapidité."
            },
            "moyen-llama": {
                "name": "LLaMA 3.1 8B Instruct Q4_K_M",
                "url": "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf?download=true",
                "description": "Le classique incontournable de Meta. Taille moyenne, tourne parfaitement sur un PC avec une carte graphique standard (8 Go de VRAM)."
            },
            "lourd-llama": {
                "name": "LLaMA 3.3 70B Instruct Q3_K_M",
                "url": "https://huggingface.co/bartowski/Llama-3.3-70B-Instruct-GGUF/resolve/main/Llama-3.3-70B-Instruct-Q3_K_M.gguf?download=true",
                "description": "Un modèle massif aux performances comparables à GPT-4. Attention : très lourd ! Nécessite au moins 32 Go de mémoire (VRAM + RAM combinées) pour fonctionner."
            }
        }

        self.__os_detector = OS()
        # ia_os_directory est actif UNIQUEMENT sous Linux (ignoré sur Windows et macOS)
        self.__use_os_dir = bool(ia_os_directory) and self.__os_detector.osLinux()

        if self.__use_os_dir:
            self.__modelDir = "/arrera/ia_model/"
        elif self.__os_detector.osLinux() or self.__os_detector.osMac():
            self.__modelDir = os.path.join(os.path.expanduser("~"), ".config", "arrera-model") + os.sep
        elif self.__os_detector.osWindows():
            self.__modelDir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "arrera-model") + os.sep
        else:
            self.__modelDir = os.path.join(os.path.expanduser("~"), ".config", "arrera-model") + os.sep

        self.__init_model_directory()

    def __set_shared_permissions(self, path: str, is_dir: bool = False):
        """
        Applique les permissions partagées (777 sur dossier, 666 sur fichier)
        lorsque le mode OS Linux (/arrera/ia_model) est actif afin que tous
        les utilisateurs Linux puissent lire/écrire sans conflit d'umask.
        """
        if not self.__use_os_dir:
            return
        try:
            os.chmod(path, 0o777 if is_dir else 0o666)
        except OSError:
            pass

    def __init_model_directory(self):
        """
        Initialise le dossier de modèles et le fichier model_download.json.
        Si /arrera/ia_model n'est pas accessible en création/écriture (ex: dossier
        parent /arrera non créé par root), bascule proprement sur ~/.config/arrera-model/.
        """
        try:
            os.makedirs(self.__modelDir, exist_ok=True)
            self.__set_shared_permissions(self.__modelDir, is_dir=True)
            self.__modelDownloadFile = os.path.join(self.__modelDir, "model_download.json")

            if not os.path.isfile(self.__modelDownloadFile):
                with open(self.__modelDownloadFile, "w", encoding="utf-8") as f:
                    json.dump({"models": []}, f, ensure_ascii=False, indent=2)
                self.__set_shared_permissions(self.__modelDownloadFile, is_dir=False)
        except PermissionError:
            if self.__use_os_dir:
                print(
                    "Attention : Permission refusée sur /arrera/ia_model/ "
                    "(vérifiez que 'sudo mkdir -p /arrera/ia_model && sudo chmod 777 /arrera/ia_model' a été exécuté). "
                    "Repli sur ~/.config/arrera-model/."
                )
                self.__use_os_dir = False
                self.__modelDir = os.path.join(os.path.expanduser("~"), ".config", "arrera-model") + os.sep
                os.makedirs(self.__modelDir, exist_ok=True)
                self.__modelDownloadFile = os.path.join(self.__modelDir, "model_download.json")
                if not os.path.isfile(self.__modelDownloadFile):
                    with open(self.__modelDownloadFile, "w", encoding="utf-8") as f:
                        json.dump({"models": []}, f, ensure_ascii=False, indent=2)

    def get_model_list(self):
        return list(self.__dictModel.keys())

    def get_model_on_dir(self):
        list_model = []
        if not os.path.isdir(self.__modelDir):
            return None
        for dossier_racine, sous_dossiers, fichiers in os.walk(self.__modelDir):
            for fichier in fichiers:
                if fichier.endswith(".gguf"):
                    list_model.append(fichier)

        if len(list_model) == 0:
            return None
        else:
            return list_model

    def get_data_model(self, key: str):
        data = self.__dictModel[key]
        return data["name"], data["url"], data["description"]

    def get_model_download(self):
        models_in_json = []
        if os.path.isfile(self.__modelDownloadFile):
            try:
                with open(self.__modelDownloadFile, 'r', encoding='utf-8') as openfile:
                    models_in_json = list(json.load(openfile).get("models", []))
            except Exception:
                models_in_json = []

        updated = False
        for key in self.__dictModel.keys():
            gguf_path = os.path.join(self.__modelDir, f"{key}.gguf")
            if os.path.isfile(gguf_path) and key not in models_in_json:
                models_in_json.append(key)
                updated = True
            elif not os.path.isfile(gguf_path) and key in models_in_json:
                models_in_json.remove(key)
                updated = True

        if updated:
            self.__save_model_download_list(models_in_json)

        return models_in_json

    def __save_model_download_list(self, models_list: list):
        try:
            with open(self.__modelDownloadFile, 'w', encoding='utf-8') as writeFile:
                json.dump({"models": models_list}, writeFile, ensure_ascii=False, indent=2)
            self.__set_shared_permissions(self.__modelDownloadFile, is_dir=False)
        except PermissionError:
            pass

    def download_model(self, key: str):
        url = self.get_data_model(key)[1]
        if key in self.get_model_download():
            return False

        try:
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                full_path = os.path.join(self.__modelDir, f"{key}.gguf")

                with open(full_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                self.__set_shared_permissions(full_path, is_dir=False)

                models = self.get_model_download()
                if key not in models:
                    models.append(key)
                self.__save_model_download_list(models)
                return True
            else:
                return False
        except Exception:
            return False

    def del_model(self, model: str):
        if model in self.get_model_download():
            file = self.get_path_model(model)
            if file and os.path.isfile(file):
                try:
                    os.remove(file)
                except PermissionError:
                    return False
                models = self.get_model_download()
                if model in models:
                    models.remove(model)
                self.__save_model_download_list(models)
                return True
            else:
                return False
        return False

    def get_path_model(self, key: str):
        if key in self.get_model_download():
            return os.path.join(self.__modelDir, f"{key}.gguf")
        else:
            return None