from abc import abstractmethod

class IGestGui:
    @abstractmethod
    def get_prompt(self):
        pass

    @abstractmethod
    def setGUIActive(self, gui: str, parms=None):
        pass

    @abstractmethod
    def launch_gui(self):
        pass

    @abstractmethod
    def textOut(self):
        pass

    @abstractmethod
    def activeAgenda(self):
        pass

    @abstractmethod
    def activeTache(self):
        pass

    @abstractmethod
    def activeHelp(self, texte: str):
        pass

    @abstractmethod
    def active_morning_brief(self):
        pass

    @abstractmethod
    def active_afternoon_brief(self):
        pass

    @abstractmethod
    def active_evening_brief(self):
        pass

    @abstractmethod
    def active_actu_all(self):
        pass

    @abstractmethod
    def active_actu_main(self):
        pass

    @abstractmethod
    def active_actu_tech(self):
        pass

    @abstractmethod
    def active_actu_culture(self):
        pass

    @abstractmethod
    def active_actu_sport(self):
        pass

    @abstractmethod
    def active_actu_science(self):
        pass

    @abstractmethod
    def activeMail(self):
        pass

    @abstractmethod
    def is_gui_available(self) -> bool:
        """Indique si une interface graphique réelle est connectée."""
        pass