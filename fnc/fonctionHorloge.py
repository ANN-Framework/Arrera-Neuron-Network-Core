import time
import threading as th
from fnc.fncBase import fncBase,gestionnaire
from librairy.audio_data import get_bip_sound_stream


class fncHorloge(fncBase):
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire)
        # Librairy
        self.__arrVoice = self._gestionnaire.getArrVoice()
        # Chronometre
        self.__isRunningChrono = False
        self.__currentTimeChrono = float
        self.__startTimeChrono = float
        self.__elapsedTimeChrono = float
        # Minuteur
        self.__runningMinuteur = False
        self.__durationMinuterie = 0
        self.__currentTimeMinuteur = 0
        self.__startTimeMinuteur = 0
        self.__elapsedTimeMinuteur = 0
        self.__thMinuteur = th.Thread(target=self.__updateHorlogeMinuteur, daemon=True)
        self.__thMinuteur.daemon = True

    def startChrono(self):
        if not self.__isRunningChrono:
            self.__startTimeChrono = time.time()
            self.__isRunningChrono = True
            self.getTimeChrono()
            return True
        else :
            return False

    def stopChrono(self):
        if self.__isRunningChrono:
            self.__isRunningChrono = False
            return True
        else:
            return False

    def resetChrono(self):
        self.__currentTimeChrono = 0
        self.__startTimeChrono = 0
        self.__elapsedTimeChrono = 0
        return True

    def getTimeChrono(self):
        if self.__isRunningChrono:
            self.__currentTimeChrono = time.time()
            self.__elapsedTimeChrono = round(self.__currentTimeChrono - self.__startTimeChrono,2)
            return self.__elapsedTimeChrono
        else:
            return 0.00

    def getStatChrono(self):
        return self.__isRunningChrono

    def startMinuteur(self, duration: int):
        if not self.__runningMinuteur:
            self.__durationMinuterie = duration
            self.__currentTimeMinuteur = 0
            self.__startTimeMinuteur = time.time()
            self.__elapsedTimeMinuteur = 0
            self.__runningMinuteur = True
            if not self.__thMinuteur.is_alive():
                self.__thMinuteur = th.Thread(target=self.__runMinuteur)
                self.__thMinuteur.daemon = True
                self.__thMinuteur.start()
            return True
        else:
            return False

    def stopMinuteur(self):
        self.__runningMinuteur = False

    def __runMinuteur(self):
        while self.__runningMinuteur:
            self.__updateHorlogeMinuteur()
            time.sleep(0.1)  # met à jour toutes les 0.1 sec

    def __updateHorlogeMinuteur(self):
        if self.__runningMinuteur:
            self.__currentTimeMinuteur = time.time()
            self.__elapsedTimeMinuteur = self.__currentTimeMinuteur - self.__startTimeMinuteur
            remaining_time = self.__durationMinuterie - self.__elapsedTimeMinuteur
            if remaining_time <= 0:
                self.__runningMinuteur = False
                self.__arrVoice.playFile(get_bip_sound_stream())
                self.stopMinuteur()

    def getStatMinuteur(self):
        return self.__runningMinuteur

    def getTimeMinuteur(self):
        if self.__runningMinuteur:
            self.__currentTimeMinuteur = time.time()
            return self.formatTemps(self.__currentTimeMinuteur - self.__startTimeMinuteur)
        return None

    def getHorloge(self) -> str:
        current_time = time.strftime("%H:%M:%S")
        return current_time

    def formatTemps(self, t: float) -> str:
        minutes, seconds = divmod(t, 60)
        return f"{int(minutes):02d}:{int(seconds):02d}"