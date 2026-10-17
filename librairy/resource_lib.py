# Objet pour gerer les ressource sur mac os
import sys, os
from librairy.dectectionOS import OS


class resource_lib:
    def __init__(self):
        osDect = OS()
        if osDect.osLinux():
            self.__os = "linux"
        elif osDect.osMac():
            self.__os = "mac"
        elif osDect.osWindows():
            self.__os = "windows"
        # Racine du package ArreraNeuronNetwork (ann-core)
        self.__core_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def resource_path(self, relative_path: str):
        # 1. Mode compilé PyInstaller
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        # 2. Si le fichier/dossier existe dans le répertoire d'exécution courant
        local_path = os.path.join(os.path.abspath("."), relative_path)
        if os.path.exists(local_path):
            return local_path
        # 3. Sinon, on le cherche à la racine du package Core (ArreraNeuronNetwork)
        core_path = os.path.join(self.__core_root, relative_path)
        if os.path.exists(core_path):
            return core_path
        return relative_path

    def tmp_directory(self):
        if self.__os == "linux" or self.__os == "mac":
            home = os.path.expanduser("~")
            return str(home) + "/.tmp"
        else:
            home = os.path.expanduser("~")
            return str(home) + "/AppData/Local/tmp"