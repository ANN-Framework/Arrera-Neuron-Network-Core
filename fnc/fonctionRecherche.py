from fnc.fncBase import fncBase,gestionnaire
import webbrowser
import requests
import time
import urllib.parse

class fncArreraSearch(fncBase) :
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire)
        self.__objNetwork = self._gestionnaire.getNetworkObjet()
        
    def __verifConnexion(self):
        self.__etatConnexion = self.__objNetwork.getEtatInternet()

    def search(self, query: str):
        self.__verifConnexion()
        if self.__etatConnexion:
            moteurUser = self._gestionnaire.getUserConf().getMoteurRecherche()
            if moteurUser == "google":
                return self.googleSearch(query)
            elif moteurUser == "brave":
                return self.braveSearch(query)
            elif moteurUser == "duckduckgo":
                return self.duckduckgoSearch(query)
            elif moteurUser == "qwant":
                return self.qwantSearch(query)
            elif moteurUser == "ecosia":
                return self.ecosiaSearch(query)
            elif moteurUser == "bing":
                return self.bingSearch(query)
            elif moteurUser == "perplexity":
                return self.perplexitySearch(query)
            else:
                moteurDefault = self._gestionnaire.getConfigFile().moteurderecherche
                if moteurDefault == "google":
                    return self.googleSearch(query)
                elif moteurDefault == "brave":
                    return self.braveSearch(query)
                elif moteurDefault == "duckduckgo":
                    return self.duckduckgoSearch(query)
                elif moteurDefault == "qwant":
                    return self.qwantSearch(query)
                elif moteurDefault == "ecosia":
                    return self.ecosiaSearch(query)
                elif moteurDefault == "bing":
                    return self.bingSearch(query)
                elif moteurDefault == "perplexity":
                    return self.perplexitySearch(query)
                else:
                    return self.googleSearch(query)
        else:
            return False

    def braveSearch(self,query:str):
        self.__verifConnexion()
        if self.__etatConnexion:
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://search.brave.com/search?q={encoded_query}&source=web"
            webbrowser.open(url)
            return True
        else :
            return False

    def amazonSearch(self,query:str):
        self.__verifConnexion()
        if self.__etatConnexion:
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://www.amazon.fr/s?k={encoded_query}"
            webbrowser.open(url)
            return True
        else :
            return False

    def googleSearch(self,query:str):
        self.__verifConnexion()
        if self.__etatConnexion:
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            webbrowser.open(url)
            return True
        else :
            return False

    def duckduckgoSearch(self,query:str):
        self.__verifConnexion()
        if self.__etatConnexion:
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://duckduckgo.com/?q={encoded_query}"
            webbrowser.open(url) 
            return True
        else :
            return False 

    def qwantSearch(self,query:str):
        self.__verifConnexion()
        if self.__etatConnexion:
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://www.qwant.com/?l=fr&q={encoded_query}"
            webbrowser.open(url)
            return True
        else :
            return False


    def ecosiaSearch(self,query:str):
        self.__verifConnexion()
        if self.__etatConnexion:
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://www.ecosia.org/search?q={encoded_query}"
            webbrowser.open(url) 
            return True
        else :
            return False

    def bingSearch(self,query:str):
        self.__verifConnexion()
        if self.__etatConnexion:
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://www.bing.com/search?q={encoded_query}"
            webbrowser.open(url)
            return True
        else :
            return False
    
    def perplexitySearch(self,query:str):
        self.__verifConnexion()
        if self.__etatConnexion:
            encoded_query = urllib.parse.quote_plus(query + ". Repond en francais")
            url = f"https://www.perplexity.ai/search/new?q={encoded_query}"
            webbrowser.open(url)
            return True
        else :
            return False
    
    def bigRecherche(self,query:str):
        self.__verifConnexion()
        if self.__etatConnexion:
            search_methods = [
                self.googleSearch,
                self.qwantSearch,
                self.duckduckgoSearch,
                self.bingSearch,
                self.perplexitySearch
            ]
            for method in search_methods:
                method(query)
                time.sleep(1.5)
            return True
        else :
            return False