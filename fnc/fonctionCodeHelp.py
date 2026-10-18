from fnc.fncBase import fncBase, gestionnaire
import webbrowser as wb
from objet.CHsearchDoc import CHsearchDoc
from objet.CHGit import CHGit


class fncCodehelp(fncBase):
    def __init__(self, gestionnaire: gestionnaire) -> None:
        super().__init__(gestionnaire)
        self.__searchDoc = CHsearchDoc()
        self.__git = CHGit()
        self.__guiLaunch = ""

    def searchDocInDevDoc(self, recherche: str) -> bool:
        if self._gestionnaire.getNetworkObjet().getEtatInternet():
            return self.__searchDoc.searchDevDoc(recherche)
        else:
            return False

    def searchDocInMicrosoft(self, recherche: str) -> bool:
        if self._gestionnaire.getNetworkObjet().getEtatInternet():
            return self.__searchDoc.searchMicrosoft(recherche)
        else:
            return False

    def searchDocInPython(self, recherche: str) -> bool:
        if self._gestionnaire.getNetworkObjet().getEtatInternet():
            return self.__searchDoc.searchPython(recherche)
        else:
            return False

    def searchGithub(self, requette: str):
        if self._gestionnaire.getNetworkObjet().getEtatInternet() and requette != "":
            return wb.open(f"https://github.com/search?q={requette}")
        else:
            return False

    def getGitObjet(self) -> CHGit:
        return self.__git

    def setGUICodeHelp(self, gui: str):
        """
        GUIColorSelector
        GUIGithubGestion
        GUILibrairy
        GUIGitGestion
        """
        self.__guiLaunch = gui
        self._gestionnaire.getGestGUI().setGUIActive(gui)

    def launchGui(self):
        return self._gestionnaire.getGestGUI().launch_gui()

    def openSiteGithub(self):
        wb.open("https://github.com/")

    def openGUIColorSelector(self):
        if self._gestionnaire.getGestGUI().setGUIActive("GUIColorSelector"):
            return self._gestionnaire.getGestGUI().launch_gui()
        return False

    def openGUIGithubGestion(self):
        if self._gestionnaire.getGestGUI().setGUIActive("GUIGithubGestion"):
            return self._gestionnaire.getGestGUI().launch_gui()
        return False

    def openGUILibrairy(self):
        if self._gestionnaire.getGestGUI().setGUIActive("GUILibrairy"):
            return self._gestionnaire.getGestGUI().launch_gui()
        return False

    def openGUIGitGestion(self):
        if self._gestionnaire.getGestGUI().setGUIActive("GUIGitGestion"):
            return self._gestionnaire.getGestGUI().launch_gui()
        return False

    def __get_target_path(self, path: str = "") -> str:
        if path and path.strip():
            return path.strip()
        work = self._gestionnaire.getGestFNC().getFNCWork()
        if work and work.getEtatProject():
            return work.getFolderProject()
        return ""

    def gitInit(self, path: str = "") -> tuple[bool, str]:
        cible = self.__get_target_path(path)
        if not cible:
            return False, "Aucun dossier ou projet actif spécifié pour Git."
        succes = self.__git.initRepo(cible)
        return succes, self.__git.getLastOutput()

    def gitStatus(self, path: str = "") -> str:
        cible = self.__get_target_path(path)
        if not cible:
            return "Aucun dossier ou projet actif spécifié pour Git."
        return self.__git.getStatus(cible)

    def gitAdd(self, path: str = "", files: str = ".") -> tuple[bool, str]:
        cible = self.__get_target_path(path)
        if not cible:
            return False, "Aucun dossier ou projet actif spécifié pour Git."
        succes = self.__git.addFiles(cible, files)
        return succes, self.__git.getLastOutput()

    def gitCommit(self, message: str, path: str = "") -> tuple[bool, str]:
        cible = self.__get_target_path(path)
        if not cible:
            return False, "Aucun dossier ou projet actif spécifié pour Git."
        self.__git.addFiles(cible)
        succes = self.__git.commit(cible, message)
        return succes, self.__git.getLastOutput()

    def gitLog(self, path: str = "") -> str:
        cible = self.__get_target_path(path)
        if not cible:
            return "Aucun dossier ou projet actif spécifié pour Git."
        return self.__git.getLastLogs(cible)