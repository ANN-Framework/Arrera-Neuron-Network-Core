from fnc.fonctionTache import *
from objet.arreradocument import *
from objet.arreratableur import *
from librairy.travailJSON import *
import subprocess
import re
import os


class fncArreraWork(fncBase):
    def __init__(self,gestionnaire: gestionnaire):
        super().__init__(gestionnaire)
        # Objet
        self.__dectOs = self._gestionnaire.getOSObjet()
        self.__fncDate = CArreraDate()
        # Variable etat ouverture fichier
        self.__tableurOpen = False
        self.__wordOpen = False
        self.__projectOpen = False
        # Varriable des objet 
        self.__objTableur = None
        self.__objWord = None
        # File JSON Project
        self.__jsonFileProject = None
        # Varriable de nom du fichier
        self.__fileTableur = ""
        self.__fileWord = ""
        # Chargement des variable
        self.__nameAssistant = gestionnaire.getConfigFile().name
        self.__guiColor = "White"
        self.__textColor = "Black"
        # Varriable Projet
        self.__folderProject = ""
        self.__lastCreateFile = ""
        self.__pendingMarkdownFile = ""
        self.__listFileProjet = []
        self.__fncTaskProjet = None  # Correspont au tache du projet
        self.__listTaskProjetToday = []
        self.__listTaskProjetTowmorow = []
        self.__listTaskProjet = []
        self.__listReadTableur = []
        self.__contentWork = ""

    # Partie Tableur

    def openTableur(self, emplacementFile: str = ""):
        return self.openTableurDirectly(emplacementFile)

    def closeTableur(self):
        if self.__tableurOpen:
            self.__objTableur.saveFile()
            self.__objTableur.closeFile()
            del self.__objTableur
            self.__objTableur = None
            self.__fileTableur = ""
            self.__tableurOpen = False
            return True
        else:
            return False

    def readTableur(self):
        if self.__tableurOpen:
            self.__listReadTableur = []
            contenu = self.__objTableur.read()
            for cell_position, cell_value in contenu.items():
                self.__listReadTableur.append("Cellule " + str(cell_position) + " : " + str(cell_value))
            return True
        else:
            return False

    def getReadTableur(self):
        return self.__listReadTableur

    def addValeurOnTableur(self, case: str, valeur):
        if self.__tableurOpen  and (case != ""):

            try:
                valeur =  int(valeur)
            except ValueError:
                valeur = valeur

            if self.__objTableur.write(case, valeur):
                if self.__objTableur.saveFile():
                    return True
                else :
                    return False
            else :
                return False
        else:
            return False

    def getListFormuleTableur(self):
        return ["Somme","Moyenne","Comptage","Minimum","Maximum"]

    def addSommeOnTableur(self, case_start: str, case_stop: str, case_dest: str):
        if (self.__tableurOpen and case_start != "") and (case_stop != "") and (case_dest != ""):
            if self.__objTableur.somme(case1=case_start, case2=case_stop, caseDestination=case_dest):
                if self.__objTableur.saveFile() :
                    return True
                else :
                    return False
            else :
                return False
        else :
            return False

    def addMoyenneOnTableur(self, case_start: str, case_stop: str, case_dest: str):
        if (self.__tableurOpen and case_start != "") and (case_stop != "") and (case_dest != ""):
            if self.__objTableur.moyenne(case1=case_start, case2=case_stop, caseDestination=case_dest):
                if self.__objTableur.saveFile() :
                    return True
                else :
                    return False
            else :
                return False
        else :
            return False

    def addComptageOnTableur(self, case_start: str, case_stop: str, case_dest: str):
        if (self.__tableurOpen and case_start != "") and (case_stop != "") and (case_dest != ""):
            if self.__objTableur.comptage(case1=case_start, case2=case_stop, caseDestination=case_dest):
                if self.__objTableur.saveFile() :
                    return True
                else :
                    return False
            else :
                return False
        else :
            return False

    def addMinimumOnTableur(self, case_start: str, case_stop: str, case_dest: str):
        if (self.__tableurOpen and case_start != "") and (case_stop != "") and (case_dest != ""):
            if self.__objTableur.minimun(case1=case_start, case2=case_stop, caseDestination=case_dest):
                if self.__objTableur.saveFile():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def addMaximumOnTableur(self, case_start: str, case_stop: str, case_dest: str):
        if (self.__tableurOpen and case_start != "") and (case_stop != "") and (case_dest != ""):
            if self.__objTableur.maximun(case1=case_start, case2=case_stop, caseDestination=case_dest):
                if self.__objTableur.saveFile():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def delValeur(self, case: str):
        if self.__tableurOpen:
            if self.__verifTableurCase(case):
                if self.__objTableur.deleteValeur(case):
                    if self.__objTableur.saveFile():
                        return True
                    else:
                        return False
                else :
                    return False
            else:
                return False
        else:
            return False

    def __verifTableurCase(self, chaine):
        # Expression régulière pour vérifier la chaîne
        regex = r"^[A-Z]\d$"

        # Vérification de la chaîne avec l'expression régulière
        if re.match(regex, chaine):
            return True
        else:
            return False

    def openTableurDirectly(self, file: str):
        if (self.__tableurOpen == False and file != ""):
            self.__fileTableur = file
            self.__objTableur = CArreraTableur(file)
            self.__tableurOpen = True
            return True
        else:
            return False

    def openTableurOs(self):
        if self.__tableurOpen:
            if self.__dectOs.osLinux() and not self.__dectOs.osWindows() :
                subprocess.call(["xdg-open", self.__fileTableur])
                return True
            elif not self.__dectOs.osLinux() and self.__dectOs.osWindows() == True:
                    os.startfile(self.__fileTableur)
                    return True
            elif self.__dectOs.osMac():  # <-- Ajout du support MacOS
                subprocess.call(["open", self.__fileTableur])
                return True
            else:
                return False
        else:
            return False

    # Partie Word

    def openWord(self, emplacementFile: str = ""):
        return self.openWordDirectly(emplacementFile)

    def openWordDirectly(self, file: str):
        if self.__wordOpen == False and file != "":
            self.__fileWord = file
            self.__objWord = CArreraDocx(file)
            self.__wordOpen = True
            return True
        else:
            return False

    def closeWord(self):
        if self.__wordOpen:
            del self.__objWord
            self.__objWord = None
            self.__fileWord = ""
            self.__wordOpen = False
            return True
        else:
            return False

    def writeWordEcrase(self,texte:str):
        if self.__wordOpen:
            if self.__objWord.writeEcrase(texte) :
                return True
            else:
                return False
        else:
            return False

    def writeWord(self, texte:str):
        if self.__wordOpen:
            if self.__objWord.writeNoEcrase(texte):
                return True
            else:
                return False
        else :
            return False

    def readWord(self):
        if self.__wordOpen:
            self.__contentWork = ""
            self.__contentWork = self.__objWord.read()
            return True
        else:
            return False

    def getReadWord(self):
        return self.__contentWork

    def openWordOs(self):
        if self.__wordOpen:
            if self.__dectOs.osLinux() and not self.__dectOs.osWindows():
                subprocess.call(["xdg-open", self.__fileWord])
                return True
            elif not self.__dectOs.osLinux() and self.__dectOs.osWindows() == True:
                os.startfile(self.__fileWord)
                return True
            elif self.__dectOs.osMac():  # <-- Ajout du support MacOS
                subprocess.call(["open", self.__fileWord])
                return True
            else:
                return False
        else:
            return False

    # Partie Projet

    def getListProjet(self):
        wordEmplacement = self._gestionnaire.getWorkEmplacement()
        if wordEmplacement != "":
            try :
                return [d for d in os.listdir(wordEmplacement) if os.path.isdir(os.path.join(wordEmplacement, d))]
            except:
                return None
        else :
            return None

    def _ensureProjectMarkdownFile(self, project_name: str) -> str:
        if not self.__projectOpen or not self.__folderProject or not project_name:
            return ""
        amd_path = os.path.join(self.__folderProject, f"{project_name}.amd")
        if not os.path.isfile(amd_path):
            try:
                with open(amd_path, "w", encoding="utf-8") as f:
                    f.write(f"# {project_name}\n\n")
            except Exception:
                return ""
        return amd_path

    def openProjet(self, project: str):
        if not self.__projectOpen:
            wordEmplacement = self._gestionnaire.getWorkEmplacement()
            dossier = [d for d in os.listdir(wordEmplacement) if os.path.isdir(os.path.join(wordEmplacement, d))]
            for i in range(0, len(dossier)):
                if project == dossier[i]:
                    self.__folderProject = wordEmplacement + "/" + project
                    self.__jsonFileProject = jsonWork(
                        os.path.join(self.__folderProject + "/.arreraProjet", project + ".apr"))
                    self.__projectOpen = True
                    self.__fncTaskProjet = self._gestionnaire.getGestFNC().initTaskProject(self.__folderProject + "/.arreraProjet/TaskProjet.json")
                    self._ensureProjectMarkdownFile(project)
                    self.setlistFileProject()
                    return True
            return False
        else:
            return False

    def createProjet(self, name: str):
        wordEmplacement = self._gestionnaire.getWorkEmplacement()
        if (self.__projectOpen == False) and (wordEmplacement != ""):
            dataJson = {"name": "", "type": ""}
            folder = (wordEmplacement + "/" + name)
            dataJson["name"] = name
            try:
                # Creation du projet
                os.makedirs(folder, exist_ok=True)
                # Creation du sous dossier de config du projet
                os.makedirs(folder + "/.arreraProjet")
                # Enregistrement de l'emplacement du projet
                self.__folderProject = folder
                # Creation du fichier de config
                configPath = os.path.join(folder + "/.arreraProjet", name + ".apr")
                # Creation du fichier de tache
                taskPath = os.path.join(folder + "/.arreraProjet", "TaskProjet.json")
                try:
                    # Ecriture dans les deux fichier
                    with open(configPath, "w", encoding="utf-8") as file:
                        json.dump(dataJson, file, ensure_ascii=False, indent=4)
                    with open(taskPath, "w", encoding="utf-8") as file:
                        json.dump({}, file, ensure_ascii=False, indent=4)
                    # Ouverture du fichier de config
                    self.__jsonFileProject = jsonWork(configPath)
                    # Mise a true de la var de projet ouvert
                    self.__projectOpen = True
                    # Ouverture fichier de tache
                    self.__fncTaskProjet = self._gestionnaire.getGestFNC().initTaskProject(taskPath)
                    # Génération automatique du fichier <name>.amd du projet
                    self._ensureProjectMarkdownFile(name)
                    self.setlistFileProject()
                    return True
                except Exception as e:
                    return False
            except Exception as e:
                return False
        else:
            return False

    def closeProjet(self):
        if self.__projectOpen:
            self.__projectOpen = False
            self.__folderProject = ""
            self.__lastCreateFile = ""
            self.__jsonFileProject = None
            self.__fncTaskProjet = None
            self.__listFileProjet = []
            self.__listTaskProjetToday = []
            self.__listTaskProjetTowmorow = []
            return True
        else:
            return False

    def getViewTypeProjetAvailable(self):
        return ["Développement d'application web",
                 "Développement d'application desktop",
                 "Développement d'application mobile",
                 "Électronique",
                 "Électrique",
                 "Système embarqué",
                 "Développement de jeux vidéo",
                 "Écriture de livre"]


    def addTypeProjet(self, type: str):
        if (type != "") and self.__projectOpen == True and (type in self.getViewTypeProjetAvailable()):
            self.__jsonFileProject.setValeurJson("type", type)
            return True
        else:
            return False

    def getNameTypeFileWithExtension(self):
        return {"excel": "xlsx",
                "word": "docx",
                "Open Document Texte": "odt",
                "markdown": "md",
                "Arrera Markdown": "amd",
                "Arrera Postite": ".ab"}

    def getListTypeFileName(self):
        return list(self.getNameTypeFileWithExtension().keys())

    def getListTypeFileExtension(self):
        return list(self.getNameTypeFileWithExtension().values())

    def createFileProject(self, name: str, type: str):
        if self.__projectOpen and name != "" and type != "":
            type_clean = type.strip()
            if (
                    type_clean in self.getListTypeFileName()
                    or type_clean in self.getListTypeFileExtension()
                    or type_clean.lower() in ("arrera markdown", "arrera_markdown", "amd", ".amd")
            ):
                emplacement = self.__folderProject + "/"
                if type_clean == "excel" or type_clean == "xlsx":
                    try:
                        self.__lastCreateFile = name + ".xlsx"
                        wb = Workbook()
                        ws = wb.active
                        ws.title = name
                        ws['A1'] = ""
                        wb.save(emplacement + self.__lastCreateFile)
                        del ws
                        wb.close()
                        del wb
                        return True
                    except Exception:
                        return False
                elif type_clean == "word" or type_clean == "docx":
                    try:
                        self.__lastCreateFile = name + '.docx'
                        doc = Document()
                        doc.add_paragraph("")
                        doc.save(emplacement + self.__lastCreateFile)
                        return True
                    except Exception:
                        return False
                elif type_clean == "Open Document Texte" or type_clean == "odt":
                    try:
                        self.__lastCreateFile = name + ".odt"
                        doc = OpenDocumentText()
                        p1 = P(text="")
                        doc.text.addElement(p1)
                        doc.save(emplacement + self.__lastCreateFile)
                        return True
                    except Exception:
                        return False
                elif type_clean == "markdown" or type_clean == "md":
                    try:
                        self.__lastCreateFile = name + ".md"
                        filePath = os.path.join(emplacement, self.__lastCreateFile)
                        with open(filePath, "w", encoding="utf-8") as file:
                            file.write("File readme named " + name)
                        return True
                    except Exception:
                        return False
                elif type_clean.lower() in ("arrera markdown", "arrera_markdown", "amd", ".amd"):
                    try:
                        clean_name = name[:-4] if name.lower().endswith(".amd") else name
                        self.__lastCreateFile = clean_name + ".amd"
                        filePath = os.path.join(emplacement, self.__lastCreateFile)
                        with open(filePath, "w", encoding="utf-8") as file:
                            file.write(f"# {clean_name}\n\n")
                        self.setlistFileProject()
                        return True
                    except Exception:
                        return False
                elif type_clean == "Arrera Postite" or type_clean == ".ab":
                    try:
                        self.__lastCreateFile = name + ".ab"
                        filePath = os.path.join(emplacement, self.__lastCreateFile)
                        with open(filePath, "w", encoding="utf-8") as file:
                            file.write("# File Arrera Postiste named " + name)
                        return True
                    except Exception:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def getTypeProjet(self):
        if self.__projectOpen:
            return self.__jsonFileProject.getContentJsonFlag("type")
        else:
            return None

    def getNameProjet(self):
        if self.__projectOpen:
            return self.__jsonFileProject.getContentJsonFlag("name")
        else:
            return None

    def setlistFileProject(self):
        if self.__projectOpen:
            try:
                # Liste les fichiers et dossiers dans le répertoire
                self.__listFileProjet = os.listdir(self.__folderProject)
                self.__listFileProjet.remove(".arreraProjet")
                return True
            except FileNotFoundError:
                return False
            except PermissionError:
                return False
            except Exception as e:
                return False
        else:
            return False

    def getListFileProjet(self):
        return self.__listFileProjet

    def getFNCTaskProjet(self):
        return self.__fncTaskProjet

    def addTacheProjet(self,name: str, date: datetime = None, description: str = None):
        if self.__projectOpen:
            return self.__fncTaskProjet.addTask(name,date,description)
        else:
            return False

    def supprTacheProjet(self,name):
        if self.__projectOpen:
            return self.__fncTaskProjet.delTask(name)
        else:
            return False

    def finishTacheProjet(self,name:str):
        if self.__projectOpen:
            return self.__fncTaskProjet.finishTask(name)
        else:
            return False

    def checkTacheProjet(self,name):
        if self.__projectOpen:
            return self.__fncTaskProjet.checkDateTask(name)
        else:
            return False

    def setListTacheTodayProjet(self):
        if self.__projectOpen:
            self.__listTaskProjetToday = self.__fncTaskProjet.getListTaskToday()
            return True
        else:
            return False

    def getListTacheTodayProjet(self):
        return self.__listTaskProjetToday

    def setListTacheTowmorowProjet(self):
        if self.__projectOpen:
            self.__listTaskProjetTowmorow = self.__fncTaskProjet.getListTaskTowmorow()
            return True
        else:
            return False

    def getListTacheTowmorowProjet(self):
        return self.__listTaskProjetTowmorow

    def setListTacheNoFinishProjet(self):
        if self.__projectOpen:
            self.__listTaskProjet = self.__fncTaskProjet.getNoFinishTask()
            return True
        else:
            return False

    def getListTacheNoFinishProjet(self):
        return self.__listTaskProjet

    # Partie tool  IA

    def _resolve_safe_path(self, relative_path: str):
        """
        Vérifie et résout un chemin pour s'assurer qu'il reste confiné
        strictement dans le dossier du projet actif (anti-traversal et symlinks).
        """
        if not self.__projectOpen or not self.__folderProject:
            return None

        # Supprime les slashs initiaux pour éviter que join n'écrase la base
        cleaned_path = relative_path.strip().lstrip("/\\")
        target_path = os.path.realpath(os.path.join(self.__folderProject, cleaned_path))
        base_path = os.path.realpath(self.__folderProject)
        try:
            # Vérifie que base_path est bien le préfixe commun du chemin cible
            common = os.path.commonpath([base_path, target_path])
            if common == base_path:
                return target_path
            return None
        except ValueError:
            return None

    def createFolderProject(self, relative_path: str) -> bool:
        """
        Crée un dossier (et ses sous-dossiers) dans le projet de façon sécurisée.
        """
        safe_path = self._resolve_safe_path(relative_path)
        if not safe_path:
            return False
        try:
            os.makedirs(safe_path, exist_ok=True)
            self.setlistFileProject()
            return True
        except Exception:
            return False

    def writeFileProject(self, relative_path: str, content: str) -> bool:
        """
        Écrit du contenu dans un fichier du projet de façon sécurisée.
        Crée automatiquement les sous-dossiers parents si nécessaire.
        """
        safe_path = self._resolve_safe_path(relative_path)
        if not safe_path:
            return False
        try:
            parent_dir = os.path.dirname(safe_path)
            os.makedirs(parent_dir, exist_ok=True)
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.__lastCreateFile = os.path.basename(safe_path)
            self.setlistFileProject()
            return True
        except Exception:
            return False

    def readFileProject(self, relative_path: str, max_chars: int = 5000) -> str:
        """
        Lit le contenu d'un fichier du projet de manière sécurisée.
        Tronque le texte pour protéger la mémoire et le contexte de l'IA.
        """
        safe_path = self._resolve_safe_path(relative_path)
        if not safe_path:
            return "Erreur : Chemin invalide ou situé en dehors du projet."
        if not os.path.exists(safe_path):
            return f"Erreur : Le fichier '{relative_path}' n'existe pas."
        if not os.path.isfile(safe_path):
            return f"Erreur : '{relative_path}' n'est pas un fichier."

        try:
            # Sécurité : refuse la lecture des fichiers de plus de 2 Mo
            if os.path.getsize(safe_path) > 2 * 1024 * 1024:
                return "Erreur : Fichier trop volumineux pour être lu (> 2 Mo)."

            with open(safe_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(max_chars + 1)

            if len(content) > max_chars:
                return content[:max_chars] + "\n\n[... Contenu tronqué pour respecter la limite ...]"
            return content
        except Exception as e:
            return f"Erreur lors de la lecture du fichier : {e}"

    def executeCommandProject(self, command: str, timeout: int = 30) -> tuple[bool, str]:
        """
        Exécute une commande terminal confinée dans le dossier racine du projet.
        Applique des filtres de sécurité et un timeout strict.
        """
        if not self.__projectOpen or not self.__folderProject:
            return False, "Erreur : Aucun projet n'est ouvert."

        # Filtres anti-commandes dangereuses
        cmd_lower = command.strip().lower()
        forbidden_keywords = ["sudo", "su ", "pkexec", "doas", "rm -rf /", "rm -rf ~"]
        for forbidden in forbidden_keywords:
            if forbidden in cmd_lower:
                return False, f"Sécurité : Commande interdite détectée ('{forbidden}')."

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.__folderProject,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            output = result.stdout
            if result.stderr:
                output += ("\n" if output else "") + result.stderr

            success = (result.returncode == 0)
            return success, output.strip() if output.strip() else "(Aucune sortie console)"
        except subprocess.TimeoutExpired:
            return False, f"Erreur : La commande a dépassé le délai maximal de {timeout}s."
        except Exception as e:
            return False, f"Erreur lors de l'exécution : {e}"

    def popPendingMarkdownFile(self) -> str:
        """Récupère et consomme le fichier en attente d'ouverture dans Arrera Markdown."""
        pending = self.__pendingMarkdownFile
        self.__pendingMarkdownFile = ""
        return pending

    def openFileArreraMarkdown(self, file_name_or_path: str = "") -> tuple[bool, str]:
        target_path = None
        raw_arg = (file_name_or_path or "").strip()
        # 1. Résolution dans le projet actif si un projet est ouvert
        if self.__projectOpen and self.__folderProject:
            proj_name = self.getNameProjet() or os.path.basename(self.__folderProject)
            # Si aucun fichier n'est précisé ou si l'argument désigne le fichier du projet
            if not raw_arg or raw_arg.lower() in ("projet", "du projet", "markdown", "arrera markdown",
                                                  proj_name.lower()):
                target_path = self._ensureProjectMarkdownFile(proj_name)
            else:
                candidates = [raw_arg]
                if not raw_arg.lower().endswith((".amd", ".md")):
                    candidates.append(raw_arg + ".amd")
                    candidates.append(raw_arg + ".md")
                for cand in candidates:
                    safe = self._resolve_safe_path(cand)
                    if safe and os.path.isfile(safe):
                        target_path = safe
                        break
        # 2. Fallback hors projet (chemin direct ou dans le dossier de travail)
        if target_path is None and raw_arg:
            expanded = os.path.expanduser(raw_arg)
            if os.path.isfile(expanded):
                target_path = os.path.realpath(expanded)
            else:
                work_dir = self._gestionnaire.getWorkEmplacement()
                if work_dir:
                    for ext in ("", ".amd", ".md"):
                        cand_path = os.path.join(work_dir, raw_arg + ext)
                        if os.path.isfile(cand_path):
                            target_path = os.path.realpath(cand_path)
                            break
        if not target_path or not os.path.isfile(target_path):
            if not self.__projectOpen and not raw_arg:
                return False, "Erreur : Aucun projet n'est ouvert et aucun fichier n'a été précisé."
            return False, f"Erreur : Le fichier '{raw_arg}' est introuvable."
        # 3. Envoi via le serveur WebSocket (port 6780) si Arrera Markdown est connecté
        sock = self._gestionnaire.getSocketObjet()
        if sock is not None and sock.get_server_is_on():
            if sock.is_client_connected_to_server("arrera_markdown"):
                sock.send_data_with_server_to("arrera_markdown", f"openfile {target_path}")
                return True, f"Le fichier '{os.path.basename(target_path)}' a été ouvert dans Arrera Markdown."
            # 4. Si Arrera Markdown n'est pas encore lancé, on met le fichier en attente et on tente de lancer l'application
            self.__pendingMarkdownFile = target_path
            fnc_open = self._gestionnaire.getGestFNC().getFNCOpen()
            launched = False
            if fnc_open is not None:
                for soft_key in ("arrera_markdown", "arrera markdown", "arreramarkdown", "arrera-markdown", "markdown"):
                    if fnc_open.openSoft(soft_key):
                        launched = True
                        break
            if launched:
                return True, f"Lancement d'Arrera Markdown et ouverture du fichier '{os.path.basename(target_path)}'."
            return True, f"Le fichier '{os.path.basename(target_path)}' sera ouvert dès le lancement d'Arrera Markdown."
        return False, "Erreur : Le serveur Socket de l'assistant n'est pas actif."

    # Getteur

    def getEtatTableur(self):
        return self.__tableurOpen

    def getEtatWord(self):
        return self.__wordOpen

    def getEtatProject(self):
        return self.__projectOpen

    def getFolderProject(self):
        return self.__folderProject

    def getNameFileTableur(self):
        return self.__fileTableur

    def getNameFileWord(self):
        return self.__fileWord