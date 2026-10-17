from objet.CArreraDownload import*
from fnc.fncBase import fncBase,gestionnaire

class fncArreraVideoDownload(fncBase) :
    def __init__(self, gestionnaire: gestionnaire):
        super().__init__(gestionnaire)
        self.__arrDownload = CArreraDownload()

    def refreshDirectory(self):
        emplacement = self._gestionnaire.getEmplacementDownload()
        if emplacement == "":
            return False
        else:
            return self.__arrDownload.setDownloadFolderDur(emplacement)

    def setMode(self,mode:int):
        """
        Args:
            mode (int): 1 -> Video 2 -> Juste Audio
        """
        return self.__arrDownload.setMode(mode)

    def getAllMode(self):
        return self.__arrDownload.getMode()

    def setUrl(self,url:str):
        return self.__arrDownload.setURL(url)

    def download(self):
        return self.__arrDownload.download()

    def downloadDirectely(self,mode:int = 1,url:str = ""):
        """
        Args:
            mode (int): 1 -> Video 2 -> Juste Audio
            url (str): Url de la video
        """
        if url == "":
            return False

        if self.refreshDirectory():
            self.setMode(mode)
            self.setUrl(url)
            return self.download()
        else :
            return False