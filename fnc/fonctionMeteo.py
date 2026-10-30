from fnc.fncBase import fncBase,gestionnaire
from datetime import datetime, timedelta,date
from meteofrance_api import MeteoFranceClient
from fnc.fonctionGPS import fncGPS

class fncMeteo(fncBase) :
    def __init__(self,gestionnaire:gestionnaire,gpsFnc:fncGPS):
        super().__init__(gestionnaire)
        if self._gestionnaire.getNetworkObjet().getEtatInternet():
            self.__client = MeteoFranceClient()
            self.__dictWarning = self.__client.get_warning_dictionary("fr")
        self.__fncGPS = gpsFnc
        self.__nameTown = None
        self.__temperature = None
        self.__humidity = None
        self.__description = None
        self.__date = None
        self.__icon = None
        self.__redAlert = []
        self.__orangeAlert = []
        self.__yellowAlert = []
        self.__greenAlert = []

        self.__place = None

    def __set_lieu(self, emplacment:str, town:str= ""):
        valeurs_autorisees = {"work", "home", "locate", "custom"}
        if emplacment in valeurs_autorisees:
            ville = ""
            if emplacment == "work":
                ville = self._gestionnaire.getUserConf().get_town_work()
            elif emplacment == "home":
                ville = self._gestionnaire.getUserConf().get_town_home()
            elif emplacment == "locate":
                if self.__fncGPS.locate():
                    ville = self.__fncGPS.getTown()
                else:
                    ville = ""
            elif emplacment == "custom":
                ville = town

            if ville:
                try :
                    self.__nameTown = ville
                    list_places = self.__client.search_places(ville)
                    self.__place = list_places[0]
                    return True
                except Exception as e:
                    #print(e)
                    return False
            else:
                return False
        else:
            return False

    def weather_current(self,emplacment:str,town:str=""):
        if self.__set_lieu(emplacment, town):
            try :
                forecast = self.__client.get_forecast_for_place(self.__place)
                meteo_en_cours = forecast.current_forecast
                self.__nameTown = self.__place.name
                self.__temperature = meteo_en_cours['T']['value']
                self.__humidity = meteo_en_cours["humidity"]
                self.__description = meteo_en_cours['weather']['desc']
                self.__icon = meteo_en_cours['weather']['icon']
                return True
            except Exception as e:
                #print(e)
                return False
        else:
            return False

    def weather_tomorrow(self,emplacment:str,town:str=""):
        if self.__set_lieu(emplacment, town):
            try :
                forecast = self.__client.get_forecast_for_place(self.__place)
                meteo_lendemain = forecast.daily_forecast[1]
                self.__nameTown = self.__place.name
                self.__temperature = f"Min: {meteo_lendemain.get('T', {}).get('min')} / Max: {meteo_lendemain.get('T', {}).get('max')}"
                #self.__humidity = "Non disponible en journalier"  # À adapter si besoin
                self.__description = meteo_lendemain.get('weather12H', {}).get('desc', 'Inconnu')
                self.__icon = meteo_lendemain.get('weather12H', {}).get('icon', 'meteo-error')
                return True
            except Exception as e:
                #print(e)
                return False
        else:
            return False

    def __get_data_for_weather(self,emplacment:str,town:str=""):
        if self.__set_lieu(emplacment, town):
            try :
                return self.__client.get_forecast_for_place(self.__place)
            except Exception as e:
                #print(e)
                return None
        else:
            return None

    def weather_afternoon(self,emplacment:str,town:str=""):
        forecast = self.__get_data_for_weather(emplacment,town)
        if forecast is None:
            return False
        try :
            meteo_apres_midi = []
            for f in forecast.forecast:
                dt = datetime.fromtimestamp(f["dt"])
                if 12 <= dt.hour < 18 and dt.date() == date.today():
                    meteo_apres_midi.append(f)

            if meteo_apres_midi:
                prevision = meteo_apres_midi[0]

                self.__temperature = prevision['T']['value']
                self.__humidity = prevision["humidity"]
                self.__description = prevision['weather']['desc']
                self.__icon = prevision['weather']['icon']
                return True
            else:
                return False
        except Exception as e:
            #print(e)
            return False

    def weather_morning(self,emplacment:str,town:str=""):
        forecast = self.__get_data_for_weather(emplacment, town)
        if forecast is None:
            return False
        try:
            meteo_matin = []
            for f in forecast.forecast:
                dt = datetime.fromtimestamp(f["dt"])
                if 6 <= dt.hour < 12 and dt.date() == date.today():
                    meteo_matin.append(f)

            if meteo_matin:
                prevision = meteo_matin[0]

                self.__temperature = prevision['T']['value']
                self.__humidity = prevision["humidity"]
                self.__description = prevision['weather']['desc']
                self.__icon = prevision['weather']['icon']
                return True
            else:
                return False
        except Exception as e:
            #print(e)
            return False

    def weather_evening(self,emplacment:str,town:str=""):
        forecast = self.__get_data_for_weather(emplacment, town)
        if forecast is None:
            return False
        try:
            meteo_soir = []
            for f in forecast.forecast:
                dt = datetime.fromtimestamp(f["dt"])
                if 18 <= dt.hour < 22 and dt.date() == date.today():
                    meteo_soir.append(f)

            if meteo_soir:
                prevision = meteo_soir[0]

                self.__temperature = prevision['T']['value']
                self.__humidity = prevision["humidity"]
                self.__description = prevision['weather']['desc']
                self.__icon = prevision['weather']['icon']
                return True
            else:
                return False
        except Exception as e:
            #print(e)
            return False

    def weather_night(self,emplacment:str,town:str=""):
        forecast = self.__get_data_for_weather(emplacment, town)
        if forecast is None:
            return False
        try:
            meteo_nuit = []
            for f in forecast.forecast:
                dt = datetime.fromtimestamp(f["dt"])
                # La nuit : >= 22h aujourd'hui, ou < 6h aujourd'hui/demain
                if (dt.hour >= 22 and dt.date() == date.today()) or \
                   (dt.hour < 6 and (dt.date() == date.today() or dt.date() == date.today() + timedelta(days=1))):
                    meteo_nuit.append(f)

            if meteo_nuit:
                prevision = meteo_nuit[0]

                self.__temperature = prevision['T']['value']
                self.__humidity = prevision["humidity"]
                self.__description = prevision['weather']['desc']
                self.__icon = prevision['weather']['icon']
                return True
            else:
                return False
        except Exception as e:
            #print(e)
            return False

    def set_alerte(self):
        self.__redAlert = []
        self.__orangeAlert = []
        self.__yellowAlert = []
        self.__greenAlert = []

        try:
            alertes_data = self.__client.get_warning_current_phenomenons(self.__place.admin2)
            alertes = alertes_data.phenomenons_max_colors
        except Exception as e:
            print(f"Erreur lors de la récupération des alertes : {e}")
            return  False

        for alerte in alertes:
            idColor = int(alerte.get('phenomenon_max_color_id', 1))
            idPhenomenon = int(alerte.get('phenomenon_id'))

            nameWarning = self.__dictWarning.get_phenomenon_by_id(idPhenomenon).get('name', 'Inconnu')

            # Rangement dans les attributs de la classe
            if idColor == 1:
                self.__greenAlert.append(nameWarning)
            elif idColor == 2:
                self.__yellowAlert.append(nameWarning)
            elif idColor == 3:
                self.__orangeAlert.append(nameWarning)
            elif idColor == 4:
                self.__redAlert.append(nameWarning)
        return True

    def getNameTown(self):
        return self.__nameTown

    def getTemperature(self):
        return self.__temperature

    def getHumidity(self):#permet de recuperé le taux d'humiditer en %
        return self.__humidity

    def getDescription(self):
        return self.__description

    def getIcon(self):
        return self.__icon

    def getRedAlert(self):
        return self.__redAlert

    def getOrangeAlert(self):
        return self.__orangeAlert

    def getYellowAlert(self):
        return self.__yellowAlert

    def getGreenAlert(self):
        return self.__greenAlert