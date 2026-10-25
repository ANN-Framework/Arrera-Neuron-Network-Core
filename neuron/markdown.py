from neuron.CNeuronBase import neuronBase, gestionnaire


class neuroneMarkdown(neuronBase):
    def __init__(self, gestionnaire: gestionnaire):
        super().__init__(gestionnaire)
        self.__socket = self._gestionnaire.getSocketObjet()
        self.__gestIA = self._gestionnaire.getGestIA()

    def neurone(self, requette: str):
        self._listSortie = ["", ""]
        self._valeurOut = 0
        if self.__socket is not None:
            if "corection" in requette:
                if not self.__gestIA.get_ia_is_enable():
                    self._valeurOut = 1
                    self._listSortie = ["Le modèle IA n'est pas activé pour corriger le document.", ""]
                else:
                    self._valeurOut = 1
                    text = "\"" + requette.replace("corection", "").strip() + "\""
                    if self.__gestIA.correted_text(text) and self.__gestIA.get_state_ia_reponse():
                        out_ia = self.__gestIA.get_reponse_ia()
                        if self.__socket.send_data_with_server_to("arrera_markdown", "text " + out_ia):
                            self._listSortie = [
                                self.__gestIA.generate_final_response(
                                    "", "La correction du document dans Arrera Markdown est terminée et envoyée."
                                ),
                                ""
                            ]
                        else:
                            self._listSortie = ["Erreur lors de l'envoi du texte corrigé à Arrera Markdown.", ""]
                    else:
                        self._listSortie = ["Une erreur s'est produite lors de la correction du texte.", ""]