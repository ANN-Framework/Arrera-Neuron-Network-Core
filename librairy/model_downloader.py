import ctypes
import glob
import json
import os
import platform
import re
import shutil
import subprocess
import requests
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
                "name": "Gemma 4 E4B Q4_K_M",
                "url": "https://huggingface.co/bartowski/google_gemma-4-E4B-it-GGUF/resolve/main/google_gemma-4-E4B-it-Q4_K_M.gguf?download=true",
                "description": "Modèle Google Gemma 4 très équilibré. Idéal pour exploiter un PC équipé d'une carte graphique classique (entre 6 et 8 Go de VRAM) ou de 16 Go de RAM."
            },
            "lourd-gemma": {
                "name": "Gemma 4 31B Q4_K_M",
                "url": "https://huggingface.co/bartowski/google_gemma-4-31B-it-GGUF/resolve/main/google_gemma-4-31B-it-Q4_K_M.gguf?download=true",
                "description": "Le nouveau fleuron de Google (Gemma 4). Très lourd et puissant, il nécessite une grosse carte graphique (16 à 24 Go de VRAM minimum) ou beaucoup de RAM vive."
            },
            "leger-mistral": {
                "name": "Ministral 3 3B Instruct Q4_K_M",
                "url": "https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512-GGUF/resolve/main/Ministral-3-3B-Instruct-2512-Q4_K_M.gguf?download=true",
                "description": "Petit modèle de la startup française Mistral AI. Très vif, parfait pour tourner de manière fluide sur un PC sans carte graphique dédiée (sur le CPU)."
            },
            "moyen-mistral": {
                "name": "Ministral 3 14B Instruct Q4_K_M",
                "url": "https://huggingface.co/bartowski/mistralai_Ministral-3-14B-Instruct-2512-GGUF/resolve/main/mistralai_Ministral-3-14B-Instruct-2512-Q4_K_M.gguf?download=true",
                "description": "Excellent modèle de 14 milliards de paramètres signé Mistral AI. Le compromis idéal pour un PC équipé d'une carte graphique de milieu de gamme (10 à 12 Go de VRAM)."
            },
            "lourd-mistral": {
                "name": "Mistral Small 3.2 (24B) Instruct Q4_K_M",
                "url": "https://huggingface.co/bartowski/mistralai_Mistral-Small-3.2-24B-Instruct-2506-GGUF/resolve/main/mistralai_Mistral-Small-3.2-24B-Instruct-2506-Q4_K_M.gguf?download=true",
                "description": "Modèle avancé et très performant de Mistral AI. Lourd, il nécessite une bonne carte graphique (au moins 16 Go de VRAM) ou beaucoup de RAM vive pour tourner confortablement."
            },
            "leger-qwen": {
                "name": "Qwen 2.5 3B Instruct Q4_K_M",
                "url": "https://huggingface.co/bartowski/Qwen2.5-3B-Instruct-GGUF/resolve/main/Qwen2.5-3B-Instruct-Q4_K_M.gguf?download=true",
                "description": "Petit modèle d'Alibaba très précis en français et en programmation. Parfait pour tourner sur le processeur (CPU) d'un PC sans carte graphique avec une excellente rapidité."
            },
            "moyen-qwen": {
                "name": "Qwen 2.5 7B Instruct Q4_K_M",
                "url": "https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/resolve/main/Qwen2.5-7B-Instruct-Q4_K_M.gguf?download=true",
                "description": "Modèle 7B très polyvalent, excellent en logique, en code et en français. Tourne parfaitement sur un PC avec une carte graphique standard (6 à 8 Go de VRAM)."
            },
            "lourd-qwen": {
                "name": "Qwen 2.5 32B Instruct Q4_K_M",
                "url": "https://huggingface.co/bartowski/Qwen2.5-32B-Instruct-GGUF/resolve/main/Qwen2.5-32B-Instruct-Q4_K_M.gguf?download=true",
                "description": "Un modèle massif de 32 milliards de paramètres redoutable en programmation et en raisonnement complexe. Nécessite une grosse carte graphique (16 à 24 Go de VRAM) ou 32 Go de RAM."
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
                    json.dump({"models": [], "custom_models": {}}, f, ensure_ascii=False, indent=2)
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
                        json.dump({"models": [], "custom_models": {}}, f, ensure_ascii=False, indent=2)

    def __read_json_metadata(self) -> dict:
        if os.path.isfile(self.__modelDownloadFile):
            try:
                with open(self.__modelDownloadFile, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        data.setdefault("models", [])
                        data.setdefault("custom_models", {})
                        return data
            except Exception:
                pass
        return {"models": [], "custom_models": {}}

    def __write_json_metadata(self, data: dict):
        try:
            with open(self.__modelDownloadFile, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.__set_shared_permissions(self.__modelDownloadFile, is_dir=False)
        except PermissionError:
            pass

    def get_all_models_dict(self) -> dict:
        """Retourne le dictionnaire combinant les modèles officiels et les modèles personnalisés."""
        combined = dict(self.__dictModel)
        meta = self.__read_json_metadata()
        custom_models = meta.get("custom_models", {})
        if isinstance(custom_models, dict):
            for k, v in custom_models.items():
                if k not in combined and isinstance(v, dict):
                    combined[k] = v
        return combined

    def get_model_list(self):
        return list(self.get_all_models_dict().keys())

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
        all_models = self.get_all_models_dict()
        if key not in all_models:
            return None, None, None
        data = all_models[key]
        return data.get("name", key), data.get("url", ""), data.get("description", "")

    def get_model_download(self):
        meta = self.__read_json_metadata()
        models_in_json = list(meta.get("models", []))
        custom_models = dict(meta.get("custom_models", {}))
        updated = False

        # 1. Vérifier tous les fichiers .gguf présents dans le dossier (officiels ou copiés manuellement)
        if os.path.isdir(self.__modelDir):
            for filename in os.listdir(self.__modelDir):
                if filename.endswith(".gguf"):
                    key = filename[:-5]
                    full_path = os.path.join(self.__modelDir, filename)
                    if os.path.isfile(full_path):
                        if key not in models_in_json:
                            models_in_json.append(key)
                            updated = True
                        if key not in self.__dictModel and key not in custom_models:
                            custom_models[key] = {
                                "name": f"{key} (Personnalisé)",
                                "url": "",
                                "description": "Modèle GGUF personnalisé détecté localement."
                            }
                            updated = True

        # 2. Nettoyer les entrées dont le fichier .gguf a été supprimé du disque
        for key in list(models_in_json):
            gguf_path = os.path.join(self.__modelDir, f"{key}.gguf")
            if not os.path.isfile(gguf_path):
                models_in_json.remove(key)
                updated = True

        if updated:
            meta["models"] = models_in_json
            meta["custom_models"] = custom_models
            self.__write_json_metadata(meta)

        return models_in_json

    def __normalize_direct_url(self, url: str) -> str:
        """
        Convertit automatiquement les liens web HuggingFace (/blob/main/)
        en liens de téléchargement direct (/resolve/main/).
        """
        clean_url = url.strip()
        if "huggingface.co/" in clean_url and "/blob/" in clean_url:
            clean_url = clean_url.replace("/blob/", "/resolve/", 1)
            if "?download=" not in clean_url:
                clean_url += "?download=true"
        return clean_url

    def __download_gguf_file(self, url: str, target_path: str) -> bool:
        """
        Télécharge un fichier GGUF en vérifiant :
        1. L'espace disque disponible (via Content-Length)
        2. La signature binaire GGUF (les 4 premiers octets doivent être b'GGUF')
        """
        direct_url = self.__normalize_direct_url(url)
        tmp_path = target_path + ".part"

        try:
            response = requests.get(direct_url, stream=True, timeout=30)
            if response.status_code != 200:
                return False

            # 1. Vérification de l'espace disque libre
            content_length = int(response.headers.get("Content-Length", 0) or 0)
            if content_length > 0:
                free_bytes = shutil.disk_usage(self.__modelDir).free
                if content_length + (200 * 1024 * 1024) > free_bytes:
                    print("Erreur téléchargement : Espace disque insuffisant.")
                    response.close()
                    return False

            first_chunk_checked = False
            with open(tmp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if not chunk:
                        continue
                    if not first_chunk_checked:
                        # 2. Vérification des Magic Bytes 'GGUF'
                        if len(chunk) < 4 or chunk[:4] != b"GGUF":
                            print("Erreur téléchargement : Le lien ne pointe pas vers un fichier GGUF valide.")
                            f.close()
                            if os.path.isfile(tmp_path):
                                os.remove(tmp_path)
                            response.close()
                            return False
                        first_chunk_checked = True
                    f.write(chunk)

            if not first_chunk_checked:
                if os.path.isfile(tmp_path):
                    os.remove(tmp_path)
                return False

            os.replace(tmp_path, target_path)
            self.__set_shared_permissions(target_path, is_dir=False)
            return True

        except Exception as e:
            print(f"Erreur téléchargement modèle GGUF : {e}")
            if os.path.isfile(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            return False

    def download_model(self, key: str):
        if key not in self.get_all_models_dict():
            return False
        if key in self.get_model_download():
            return False

        url = self.get_data_model(key)[1]
        if not url:
            return False

        full_path = os.path.join(self.__modelDir, f"{key}.gguf")
        if self.__download_gguf_file(url, full_path):
            self.get_model_download()
            return True
        return False

    def download_custom_model(self, name: str, url: str, description: str = "") -> bool:
        """
        Télécharge un modèle GGUF externe à partir d'un lien direct (ex: HuggingFace)
        et l'enregistre dans le catalogue local sous l'identifiant normalisé `name`.
        """
        if not name or not url or not isinstance(name, str) or not isinstance(url, str):
            return False

        clean_key = name.strip().lower()
        if clean_key.endswith(".gguf"):
            clean_key = clean_key[:-5]
        clean_key = re.sub(r"[^a-z0-9_-]+", "-", clean_key).strip("-")

        if not clean_key:
            return False

        if clean_key in self.get_model_download():
            return False

        full_path = os.path.join(self.__modelDir, f"{clean_key}.gguf")
        if not self.__download_gguf_file(url, full_path):
            return False

        meta = self.__read_json_metadata()
        if clean_key not in meta["models"]:
            meta["models"].append(clean_key)

        if clean_key not in self.__dictModel:
            meta["custom_models"][clean_key] = {
                "name": name.strip(),
                "url": self.__normalize_direct_url(url),
                "description": description.strip() or "Modèle GGUF personnalisé téléchargé via lien direct."
            }

        self.__write_json_metadata(meta)
        return True

    def del_model(self, model: str):
        if model in self.get_model_download():
            file = self.get_path_model(model)
            if file and os.path.isfile(file):
                try:
                    os.remove(file)
                except PermissionError:
                    return False
                meta = self.__read_json_metadata()
                if model in meta["models"]:
                    meta["models"].remove(model)
                if model in meta.get("custom_models", {}):
                    del meta["custom_models"][model]
                self.__write_json_metadata(meta)
                return True
            else:
                return False
        return False

    def get_path_model(self, key: str):
        if key in self.get_model_download():
            return os.path.join(self.__modelDir, f"{key}.gguf")
        else:
            return None

    # ==========================================================================
    # DÉTECTION MATÉRIELLE MULTI-OS & RECOMMANDATION DE MODÈLE
    # ==========================================================================

    def __get_ram_gb(self) -> float:
        """Retourne la RAM totale de la machine en Go (compatible Linux, Windows, macOS)."""
        try:
            if self.__os_detector.osLinux():
                with open("/proc/meminfo", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("MemTotal:"):
                            kb = int(line.split()[1])
                            return round(kb / (1024 * 1024), 1)
            elif self.__os_detector.osMac():
                out = subprocess.check_output(["sysctl", "-n", "hw.memsize"], stderr=subprocess.DEVNULL)
                return round(int(out.strip()) / (1024 ** 3), 1)
            elif self.__os_detector.osWindows():
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(stat)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                return round(stat.ullTotalPhys / (1024 ** 3), 1)
        except Exception:
            pass
        return 8.0

    def __get_vram_gb(self, ram_gb: float) -> float:
        """
        Détecte la mémoire vidéo dédiée (VRAM) en Go :
        - GPU NVIDIA (Linux / Windows) via nvidia-smi
        - GPU AMD (Linux) via /sys/class/drm/card*/device/mem_info_vram_total
        - Apple Silicon (macOS arm64) via mémoire unifiée (~75% de la RAM)
        """
        # 1. Test NVIDIA (Linux / Windows)
        try:
            out = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
                stderr=subprocess.DEVNULL,
                timeout=2
            ).decode("utf-8").strip()
            if out:
                max_vram_mb = max(int(line.strip()) for line in out.splitlines() if line.strip().isdigit())
                return round(max_vram_mb / 1024.0, 1)
        except Exception:
            pass

        # 2. Test AMD sous Linux (/sys/class/drm)
        if self.__os_detector.osLinux():
            try:
                vram_files = glob.glob("/sys/class/drm/card*/device/mem_info_vram_total")
                max_bytes = 0
                for vf in vram_files:
                    with open(vf, "r", encoding="utf-8") as f:
                        val = int(f.read().strip())
                        if val > max_bytes:
                            max_bytes = val
                # On ignore les petits tampons iGPU (< 2 Go) qui partagent la RAM système
                if max_bytes >= 2 * (1024 ** 3):
                    return round(max_bytes / (1024 ** 3), 1)
            except Exception:
                pass

        # 3. Test Apple Silicon (Mémoire unifiée sur macOS arm64)
        if self.__os_detector.osMac() and platform.machine().lower() in ("arm64", "aarch64"):
            return round(ram_gb * 0.75, 1)

        return 0.0

    def get_hardware_recommendation(self) -> dict:
        """
        Analyse le matériel de la machine (RAM, VRAM, CPU) et retourne un dictionnaire
        contenant la catégorie optimale, le meilleur modèle recommandé et la liste des modèles compatibles.
        """
        ram_gb = self.__get_ram_gb()
        vram_gb = self.__get_vram_gb(ram_gb)
        cpu_cores = os.cpu_count() or 4

        # Palier LOURD (24B - 32B) : GPU >= 16 Go VRAM ou RAM >= 32 Go avec GPU >= 12 Go / Apple Silicon
        if vram_gb >= 16.0 or (ram_gb >= 32.0 and vram_gb >= 12.0):
            category = "lourd"
            recommended = "lourd-mistral"
            compatible = [
                "leger-gemma", "leger-qwen", "leger-mistral",
                "moyen-qwen", "moyen-gemma", "moyen-mistral",
                "lourd-mistral", "lourd-gemma", "lourd-qwen"
            ]

        # Palier MOYEN+ (14B) : GPU >= 10 Go VRAM ou RAM >= 24 Go
        elif vram_gb >= 10.0 or ram_gb >= 24.0:
            category = "moyen"
            recommended = "moyen-mistral"
            compatible = [
                "leger-gemma", "leger-qwen", "leger-mistral",
                "moyen-gemma", "moyen-qwen", "moyen-mistral"
            ]

        # Palier MOYEN (E4B / 7B) : GPU >= 6 Go VRAM ou (RAM >= 16 Go et CPU >= 6 threads)
        elif vram_gb >= 6.0 or (ram_gb >= 16.0 and cpu_cores >= 6):
            category = "moyen"
            recommended = "moyen-gemma"
            compatible = [
                "leger-gemma", "leger-qwen", "leger-mistral",
                "moyen-gemma", "moyen-qwen"
            ]

        # Palier LÉGER (2B - 3B) : PC sans GPU dédié ou <= 12 Go RAM
        else:
            category = "leger"
            recommended = "leger-gemma"
            compatible = [
                "leger-gemma", "leger-qwen", "leger-mistral"
            ]

        return {
            "ram_gb": ram_gb,
            "vram_gb": vram_gb,
            "cpu_cores": cpu_cores,
            "category": category,
            "recommended_model": recommended,
            "compatible_models": compatible
        }

    def get_recommended_model(self) -> str:
        """Retourne directement l'identifiant du meilleur modèle adapté à la machine."""
        return self.get_hardware_recommendation()["recommended_model"]