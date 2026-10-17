import yt_dlp

class CArreraDownload :
    def __init__(self):
        self.__url = ""
        self.__urlSet = False
        self.__downloadFolderSet = False
        self.__ydlOpts = {}
        self.__mode = 1
        
    def setMode(self,m:int):
        """
        1 -> Video 
        2 -> Juste Sons2
        3 -> Juste Video
        """
        if m == 1 or m == 2 or m == 3:
            self.__mode = m
            return True
        else :
            return False

    def setDownloadFolderDur(self, folder: str):
        if folder == "":
            self.__downloadFolderSet = False
            return False
        else:
            self.__downloadFolderSet = True
            self.__ydlOpts = {
                'format': '',  # Sélectionne la meilleure qualité disponible
                'outtmpl': folder + "/" + '%(title)s.%(ext)s',  # Définit le chemin de sortie
                'quiet': True,  # Désactive les messages de la console
                'no_warnings': True,  # Supprime les avertissements
            }
            return True
    
    def setURL(self,url:str):
        if (url != ""):
            self.__url = url
            self.__urlSet = True
            return True
        else :
            self.__urlSet = False
            return False
      
    def download(self):
        if ((self.__downloadFolderSet == True) and (self.__urlSet == True)):
            match self.__mode :
                case 1 :
                    self.__ydlOpts['format'] = "best"
                case 2 :
                    self.__ydlOpts['format'] = "bestaudio"
                case 3 :
                    self.__ydlOpts['format'] = "bestvideo"
        
            with yt_dlp.YoutubeDL(self.__ydlOpts) as ydl:
                ydl.download([self.__url])
            self.__urlSet = False
            self.__url = ""
            return True
        else :
            return False

    def getMode(self):
        return {"1":"best","2":"bestaudio","3":"bestvideo"}
        