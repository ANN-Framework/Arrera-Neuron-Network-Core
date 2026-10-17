from fnc.fncBase import fncBase, gestionnaire
import webbrowser as wb
from objet.CHsearchDoc import CHsearchDoc


class fncCodehelp(fncBase):
    def __init__(self, gestionnaire: gestionnaire) -> None:
        super().__init__(gestionnaire)
        self.__searchDoc = CHsearchDoc()
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

    def setGUICodeHelp(self, gui: str):
        """
        GUIColorSelector
        GUIGithubGestion
        GUILibrairy
        GUIOrgaVar
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

    def openGUIOrgaVar(self):
        if self._gestionnaire.getGestGUI().setGUIActive("GUIOrgaVar"):
            return self._gestionnaire.getGestGUI().launch_gui()
        return False