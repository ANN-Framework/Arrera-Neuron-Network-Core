from gestionnaire.IGestGui import IGestGui


class HeadlessGuiManager(IGestGui):
    """
    Gestionnaire GUI par défaut (Headless / Null Object).
    Indique au Core qu'aucune interface graphique n'est présente,
    permettant aux routeurs de basculer sans crash sur les réponses de données (texte/voix).
    """
    def __init__(self, gest=None):
        self._gest = gest

    def is_gui_available(self) -> bool:
        return False

    def get_prompt(self) -> str:
        return ""

    def setGUIActive(self, gui: str, parms=None) -> bool:
        return False

    def launch_gui(self) -> bool:
        return False

    def textOut(self) -> str:
        return ""

    def activeAgenda(self) -> bool:
        return False

    def activeTache(self) -> bool:
        return False

    def activeHelp(self, texte: str) -> bool:
        return False

    def active_morning_brief(self) -> bool:
        return False

    def active_afternoon_brief(self) -> bool:
        return False

    def active_evening_brief(self) -> bool:
        return False

    def active_actu_all(self) -> bool:
        return False

    def active_actu_main(self) -> bool:
        return False

    def active_actu_tech(self) -> bool:
        return False

    def active_actu_culture(self) -> bool:
        return False

    def active_actu_sport(self) -> bool:
        return False

    def active_actu_science(self) -> bool:
        return False

    def activeMail(self) -> bool:
        return False


gestGUI = HeadlessGuiManager
