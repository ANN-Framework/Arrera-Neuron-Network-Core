import subprocess
import shutil
import os


class CHGit:

    def __init__(self):
        self.__lastOutput = ""

    def getLastOutput(self) -> str:
        return self.__lastOutput

    def checkGitInstalled(self) -> bool:
        return shutil.which("git") is not None

    def isGitRepo(self, repo_path: str) -> bool:
        if not os.path.isdir(repo_path):
            self.__lastOutput = f"Le dossier '{repo_path}' n'existe pas."
            return False
        try:
            res = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return res.returncode == 0
        except Exception as e:
            self.__lastOutput = str(e)
            return False

    def initRepo(self, repo_path: str) -> bool:
        if not os.path.isdir(repo_path):
            self.__lastOutput = f"Le dossier '{repo_path}' n'existe pas."
            return False
        try:
            res = subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            self.__lastOutput = res.stdout.strip() or res.stderr.strip()
            return res.returncode == 0
        except Exception as e:
            self.__lastOutput = f"Erreur init Git : {e}"
            return False

    def getStatus(self, repo_path: str) -> str:
        if not self.isGitRepo(repo_path):
            return "Ce dossier n'est pas un dépôt Git."
        try:
            res = subprocess.run(
                ["git", "status", "--short"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            sortie = res.stdout.strip()
            return sortie if sortie else "Répertoire de travail propre (aucun changement)."
        except Exception as e:
            return f"Erreur status Git : {e}"

    def addFiles(self, repo_path: str, files: str = ".") -> bool:
        if not self.isGitRepo(repo_path):
            self.__lastOutput = "Ce dossier n'est pas un dépôt Git."
            return False
        try:
            res = subprocess.run(
                ["git", "add", files],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            self.__lastOutput = res.stderr.strip() if res.stderr else "OK"
            return res.returncode == 0
        except Exception as e:
            self.__lastOutput = f"Erreur add Git : {e}"
            return False

    def commit(self, repo_path: str, message: str) -> bool:
        if not self.isGitRepo(repo_path):
            self.__lastOutput = "Ce dossier n'est pas un dépôt Git."
            return False
        if not message.strip():
            self.__lastOutput = "Le message de commit ne peut pas être vide."
            return False
        try:
            res = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=15
            )
            self.__lastOutput = res.stdout.strip() or res.stderr.strip()
            return res.returncode == 0
        except Exception as e:
            self.__lastOutput = f"Erreur commit Git : {e}"
            return False

    def getBranches(self, repo_path: str) -> str:
        if not self.isGitRepo(repo_path):
            return "Ce dossier n'est pas un dépôt Git."
        try:
            res = subprocess.run(
                ["git", "branch"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return res.stdout.strip()
        except Exception as e:
            return f"Erreur branch Git : {e}"

    def getLastLogs(self, repo_path: str, limit: int = 5) -> str:
        if not self.isGitRepo(repo_path):
            return "Ce dossier n'est pas un dépôt Git."
        try:
            res = subprocess.run(
                ["git", "log", f"-n{limit}", "--oneline"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return res.stdout.strip() or "Aucun commit."
        except Exception as e:
            return f"Erreur log Git : {e}"

    def createBranch(self, repo_path: str, branch_name: str) -> bool:
        if not self.isGitRepo(repo_path):
            self.__lastOutput = "Ce dossier n'est pas un dépôt Git."
            return False
        if not branch_name.strip():
            self.__lastOutput = "Le nom de la branche ne peut pas être vide."
            return False
        try:
            res = subprocess.run(
                ["git", "checkout", "-b", branch_name.strip()],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            self.__lastOutput = res.stdout.strip() or res.stderr.strip()
            return res.returncode == 0
        except Exception as e:
            self.__lastOutput = f"Erreur création branche Git : {e}"
            return False

    def switchBranch(self, repo_path: str, branch_name: str) -> bool:
        if not self.isGitRepo(repo_path):
            self.__lastOutput = "Ce dossier n'est pas un dépôt Git."
            return False
        if not branch_name.strip():
            self.__lastOutput = "Le nom de la branche ne peut pas être vide."
            return False
        try:
            res = subprocess.run(
                ["git", "checkout", branch_name.strip()],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            self.__lastOutput = res.stdout.strip() or res.stderr.strip()
            return res.returncode == 0
        except Exception as e:
            self.__lastOutput = f"Erreur changement de branche Git : {e}"
            return False