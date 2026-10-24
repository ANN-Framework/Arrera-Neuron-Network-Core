from collections import deque
from typing import List, Dict, Optional


class gestSession:
    def __init__(self, gestionnaire, max_turns: int = 6):
        self.__gestionnaire = gestionnaire
        self.__max_turns = max(1, max_turns)
        self.__history: deque = deque(maxlen=self.__max_turns)

    def setMaxTurns(self, max_turns: int) -> bool:
        if max_turns > 0:
            self.__max_turns = max_turns
            self.__history = deque(self.__history, maxlen=self.__max_turns)
            return True
        return False

    def getMaxTurns(self) -> int:
        return self.__max_turns

    def addTurn(self, user_input: str, assistant_output: str, action: str = "") -> bool:
        u = str(user_input).strip()
        a = str(assistant_output).strip()
        if not u and not a:
            return False

        self.__history.append({
            "user": u,
            "assistant": a,
            "action": action
        })
        return True

    def getHistory(self) -> List[Dict[str, str]]:
        return list(self.__history)

    def getLastTurn(self) -> Optional[Dict[str, str]]:
        if self.__history:
            return self.__history[-1]
        return None

    def getLastUserQuery(self) -> str:
        last = self.getLastTurn()
        return last["user"] if last else ""

    def getLastAssistantResponse(self) -> str:
        last = self.getLastTurn()
        return last["assistant"] if last else ""

    def clearSession(self) -> bool:
        self.__history.clear()
        return True

    def isEmpty(self) -> bool:
        return len(self.__history) == 0

    def getPromptContext(self) -> str:
        if not self.__history:
            return ""

        lignes = []
        for turn in self.__history:
            user_text = turn.get("user", "")
            assistant_text = turn.get("assistant", "")
            # Nettoyer les sauts de ligne multiples et tronquer si trop long
            assistant_clean = " ".join(assistant_text.split())
            if len(assistant_clean) > 250:
                assistant_clean = assistant_clean[:247].rsplit(" ", 1)[0] + "..."
            if user_text:
                lignes.append(f"Utilisateur : {user_text}")
            if assistant_clean:
                lignes.append(f"Assistant : {assistant_clean}")

        if not lignes:
            return ""

        return (
            "\n=== CONTEXTE RÉCENT DE LA CONVERSATION (SESSION EN COURS) ===\n"
            + "\n".join(lignes)
            + "\n============================================================\n"
        )
