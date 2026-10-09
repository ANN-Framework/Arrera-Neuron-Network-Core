# 📋 Plan d'Action 2 : Sécurisation Headless, Découplage GUI & Stratégie "Data Fallback"

Ce document fait suite à l'audit de code du Core (`ArreraNeuronNetwork`). Il détaille les étapes concrètes pour :
1. Rendre le Core 100% robuste en mode *Headless* (sans crash `NoneType`).
2. Mettre en place la bascule intelligente **Headless (Data / Texte) vs GUI (Fenêtre graphique)** pour les tâches, briefs, agenda, actualités.
3. Découpler le Core des dépendances Tkinter résiduelles.
4. Adapter `test-gui.py`.

---

## 🎯 Objectifs

1. **Zéro crash en mode Headless** : Tout appel graphique échoue gracieusement via le *Null Object Pattern*.
2. **Bascule intelligente Headless / GUI ("Fallback Data")** :
   * **Avec GUI** : Les demandes d'interfaces ouvrent les fenêtres graphiques (`TkinterGuiManager`).
   * **Sans GUI (Headless)** : Le Core bascule automatiquement sur les données brutes (`fncTask`, `fncAgenda`, `fncNews`, `fncMeteo`...) et génère une réponse textuelle/vocale enrichie avec l'IA.
3. **Découplage strict du Core** : Supprimer toute dépendance directe à `tkinter`, `customtkinter` et `gui/` dans `fnc/`, `objet/`, `gestionnaire/`.
4. **Préservation du banc de test Tkinter** (`test-gui.py`).

---

## 🧠 Principe Clé : La Détection de GUI (`is_gui_available`)

Le contrat [`IGestGui`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/gestionnaire/IGestGui.py) définit une méthode essentielle : `is_gui_available() -> bool`.

```text
                                Demande Utilisateur
                        (ex: "Donne-moi mon brief / mes tâches")
                                        │
                                        ▼
                         Vérification : has_gui() ?
                                   /         \
                             OUI  /           \  NON (Headless)
                                 ▼             ▼
                       [ Mode Graphique ]    [ Mode Data / Synthèse ]
                     Ouvre la fenêtre GUI    Extrait les données (fnc)
                     (Tkinter / GTK...)      Génère la synthèse IA
                     Sortie = 5 (GUI)        Sortie = 1 (Texte/Vocal)
```

---

## 🏗️ Détail de la Bascule par Domaine (Headless vs GUI)

### 1. Le Brief (Matin, Après-midi, Soir)
* **Mode GUI** :
  `active_morning_brief()` ouvre la fenêtre `GuiBrief` avec les 3 blocs visuels.
* **Mode Headless (Data)** :
  Le Core collecte les données métier :
  * Météo : `fnc.getFNCMeteo()`
  * Tâches du jour : `fnc.getFNCTask().getListTaskToday()`
  * Actualités : `fnc.getFNCNews().getResumeNews()`
  Il transmet ces données à l'IA (`gestIA.generate_final_response()`) qui produit un résumé vocal/texte naturel :
  > *"Bonjour Monsieur Pauchet ! Il fait 18°C avec un ciel dégagé. Vous avez 2 tâches aujourd'hui : Finaliser le rapport et Appeler le support. Côté actualités : Lancement réussi de la mission Artemis. Bonne journée !"*

### 2. Les Tâches & L'Agenda
* **Mode GUI** :
  `"ouvre mes tâches"` -> `gui.activeTache()` ouvre la fenêtre Tkinter des tâches.
* **Mode Headless (Data)** :
  `"ouvre mes tâches"` ou `"quelles sont mes tâches ?"` :
  Comme aucune GUI n'est disponible, le routeur appelle directement `fnc.getFNCTask().getListTaskToday()` (ou `getNoFinishTask()`), formate la liste et répond en texte/voix :
  > *"Voici vos tâches en cours : 1. ..., 2. ... Souhaitez-vous en marquer une comme terminée ?"*

### 3. Les Actualités
* **Mode GUI** :
  `"affiche les actualités"` -> `gui.active_actu_*()` ouvre l'interface des news.
* **Mode Headless (Data)** :
  Le Core interroge le flux RSS / `fncNews` et synthétise les titres principaux via l'IA.

### 4. La Calculatrice & Outils
* **Mode GUI** :
  Ouvre la fenêtre graphique de la calculatrice.
* **Mode Headless (Data)** :
  Résout directement le calcul via `fncCalculatrice` ou l'IA et donne le résultat en texte : *"Le résultat est 42."*

---

## 📝 Étapes d'Implémentation

### Étape 1 : Enrichir le contrat `IGestGui` et implémenter `HeadlessGuiManager`

* **Fichier :** [`gestionnaire/IGestGui.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/gestionnaire/IGestGui.py)
  Ajouter `is_gui_available(self) -> bool:` au contrat abstrait.

* **Fichier :** [`gestionnaire/gestGUI.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/gestionnaire/gestGUI.py)
  Remplacer l'ancien code Tkinter par `HeadlessGuiManager` (Null Object Pattern) :

```python
# gestionnaire/gestGUI.py
from gestionnaire.IGestGui import IGestGui


class gestGUI(IGestGui):
    """
    Gestionnaire GUI par défaut (Headless / Null Object).
    Indique au Core qu'aucune interface graphique n'est présente,
    permettant aux routeurs de basculer sur les réponses de données (texte/voix).
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


HeadlessGuiManager = gestGUI
```

---

### Étape 2 : Mettre à jour `gestionnaire/gestion.py`

* **Fichier :** [`gestionnaire/gestion.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/gestionnaire/gestion.py)
  * Instancier `self.__gui = gestGUI(self)` par défaut.
  * Ajouter la méthode d'aide `has_gui() -> bool` :
    ```python
    def has_gui(self) -> bool:
        return self.__gui is not None and self.__gui.is_gui_available()
    ```

---

### Étape 3 : Implémenter le "Fallback Data" dans les routeurs et le cerveau

#### 1. Brief dans [`brain/brain.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/brain/brain.py) (`updateAssistant`)
```python
# Exemple pour le brief du matin :
if self.__gestionnaire.has_gui():
    self.__gestionnaire.getGestGUI().active_morning_brief()
    self.__valeurOut = 5  # Sortie GUI
else:
    # Mode Headless : compilation des données météo + tâches + actu
    meteo = self.__gestionnaire.getGestFNC().getFNCMeteo().get_resume_today()
    taches = self.__gestionnaire.getGestFNC().getFNCTask().getListTaskToday()
    donnees = f"Météo: {meteo} | Tâches: {taches}"
    reponse = self.__gestIA.generate_final_response("", f"Fais le brief du matin avec ces données : {donnees}")
    self.__listOut = [reponse, ""]
    self.__valeurOut = 1  # Sortie texte / vocale
```

#### 2. Brief dans [`neuron/IARouter.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/neuron/IARouter.py) (`__handle_brief`)
```python
def __handle_brief(self, args):
    moment = self.__arg(args, 0, "morning")
    
    # 1. Si une GUI est connectée, on l'ouvre
    if self.__gestionnaire.has_gui():
        gui_name = f"{moment}_brief"
        if self.__gestGUI.setGUIActive(gui_name):
            return f"Interface de brief {moment} ouverte.", 5

    # 2. Sinon, en mode Headless : on compile les données et on répond en texte
    meteo = self.__gestFNC.getFNCMeteo().get_resume_today()
    taches = self.__gestFNC.getFNCTask().getListTaskToday()
    donnees = f"Brief {moment} - Météo: {meteo}, Tâches: {taches}"
    reponse = self.__gestIA.generate_final_response("", f"Présente le brief {moment} à l'utilisateur : {donnees}")
    return reponse, 1
```

#### 3. Tâches et Agenda dans [`neuron/core_neuron.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/neuron/core_neuron.py) et [`neuron/interface.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/neuron/interface.py)
* Si l'utilisateur demande d'ouvrir l'agenda ou les tâches (`mots[0] == "GUI"` ou `keyword == "task"`/`"agenda"`) :
  * Si `self._gestionnaire.has_gui()` est `True` : ouverture de la GUI (`valeurOut = 5`).
  * Sinon (`has_gui() == False`) : récupération des données via `fncTask` ou `fncAgenda` et synthèse vocale/texte (`valeurOut = 1`).

---

### Étape 4 : Découplage du Core logique (`fnc/` et `objet/`)

1. **[`fnc/fonctionCodeHelp.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/fnc/fonctionCodeHelp.py)** :
   * Supprimer les imports statiques `from gui.codehelp.*`.
   * Déléguer l'ouverture au gestionnaire GUI si disponible.
2. **[`fnc/fonctionArreraWork.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/fnc/fonctionArreraWork.py)** :
   * Retirer les imports `filedialog` et `messagebox`.
3. **[`objet/CArreraDownload.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/objet/CArreraDownload.py)** :
   * Retirer `from tkinter import filedialog`.

---

### Étape 5 : Créer `TkinterGuiManager` et adapter `test-gui.py`

1. Déplacer l'ancienne logique de `gestGUI.py` dans [`gui/TkinterGuiManager.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/gui/TkinterGuiManager.py).
   * Implémente `is_gui_available(self) -> bool: return True`.
2. Dans [`test-gui.py`](file:///Users/baptistep/Documents/ANN/ArreraNeuronNetwork/test-gui.py) :
   ```python
   from gui.TkinterGuiManager import TkinterGuiManager

   gest = gestionnaire(conf)
   gest.set_gui_manager(TkinterGuiManager(gest))  # Active le mode GUI !
   gest_gui = gest.getGestGUI()
   ```

---

## 🧪 Validation & Tests

- [ ] **Test 1 : Headless - Demande de tâches** :
  Dire `"quelles sont mes tâches ?"` en console -> Réponse avec la liste textuelle des tâches, sans crash, sans chercher à ouvrir de fenêtre.
- [ ] **Test 2 : Headless - Demande de brief** :
  Dire `"donne-moi mon brief"` en console -> L'IA énonce la météo et les tâches du jour.
- [ ] **Test 3 : GUI - Test avec `test-gui.py`** :
  Lancer `python test-gui.py` -> Les fenêtres graphiques s'ouvrent bien grâce à `TkinterGuiManager`.
- [ ] **Test 4 : Zero Tkinter dans `main.py`** :
  Vérifier que `main.py` tourne sans importer un seul module Tkinter.
