# 📋 Plan d'Action : Séparation Core (Headless) & Frontend Tkinter

Ce document détaille la feuille de route pour isoler **Arrera Neuron Network Core** en moteur 100% *Headless*, ainsi que la structure cible du projet et le fichier `pyproject.toml`.

---

## 1. Arborescence du Projet Core (`ArreraNeuronNetwork`)

Voici la vue d'ensemble du projet Core une fois nettoyé de Tkinter :

```text
ArreraNeuronNetwork/                    # Dépôt Core (Headless)
├── pyproject.toml                      # [NOUVEAU] Déclaration du package pip 'ann-core'
├── requirements.txt                    # [MODIFIÉ] Dépendances Headless uniquement (sans Tkinter / GTK)
├── main.py                             # [MODIFIÉ] Lanceur mode Headless (Console / Vocal / Démon)
├── readme.md                           # Documentation Core
│
├── brain/                              # Inchangé : Cerveau logique & orchestration
│   └── brain.py
├── neuron/                             # Inchangé : Classification & routeurs IA
│   ├── core_neuron.py
│   ├── IARouter.py
│   ├── interface.py
│   ├── CNeuronBase.py
│   └── markdown.py
│
├── fnc/                                # Logique métier
│   ├── fncBase.py
│   ├── fonctionGPS.py
│   ├── fonctionMeteo.py
│   ├── fonctionHorloge.py
│   ├── fonctionCalculatrice.py
│   ├── fonctionArreraWork.py           # [MODIFIÉ] Retrait des imports filedialog / messagebox Tkinter
│   └── ...
│
├── objet/                              # Objets métier
│   ├── CArreraDownload.py              # [MODIFIÉ] Retrait des popups Tkinter résiduelles
│   ├── arreradocument.py
│   └── arreratableur.py
│
├── gestionnaire/                       # Gestionnaires système & logique
│   ├── gestion.py                      # [MODIFIÉ] self.__gui = None + méthode set_gui_manager()
│   ├── gestIA.py                       # [MODIFIÉ] Méthode pour charger des prompts IA de GUI
│   ├── gestGUI.py                      # [REMPLACÉ] Devient une interface abstraite (contrat IGuiManager)
│   ├── gestFNC.py
│   ├── gestLangue.py
│   ├── gestUserSetting.py
│   ├── gestSocket.py
│   └── ...
│
├── instruction_ia/                     # Prompts IA du Core
│   ├── prompt_dedoublonnage.txt
│   ├── prompt_mail_reponse.txt
│   └── ...
│
├── config/                             # Configuration système
├── keyword/                            # Fichiers de mots-clés
├── language/                           # Fichiers de langues
├── librairy/                           # Utilitaires (Réseau, Détection OS, Voix...)
│
├── asset/                              # Assets non graphiques
│   ├── sound/                          # Sons
│   └── theme/
│
└── ❌ ÉLÉMENTS DÉPLACÉS VERS ann-tkinter :
    ├── gui/                            # ➡️ Déplacé vers ann-tkinter (GUIAgenda, GUICalculatrice, etc.)
    ├── src/GUIOpale.py                 # ➡️ Déplacé vers ann-tkinter (Fenêtre principale Tkinter)
    ├── test-gui.py                     # ➡️ Déplacé vers ann-tkinter
    ├── compilation_mac/test-gui.spec   # ➡️ Déplacé vers ann-tkinter
    └── asset/(calendar, horloge...)    # ➡️ Déplacé vers ann-tkinter (icônes d'interfaces)
```

---

## 2. Fichier `pyproject.toml` pour le Core

Ce fichier permet d'installer le Core avec `pip install -e .` en mode développement, rendant tous les modules disponibles immédiatement pour `ann-tkinter` et les autres projets.

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "ann-core"
version = "4.0.0"
description = "Moteur logique et IA d'Arrera Neuron Network (Headless Core)"
readme = "readme.md"
requires-python = ">=3.11"
authors = [
    { name = "Arrera Software" }
]
dependencies = [
    "requests",
    "gTTS",
    "translate",
    "python-docx",
    "odfpy",
    "openpyxl",
    "PyGithub",
    "pyperclip",
    "websocket-client",
    "websockets",
    "numpy",
    "sounddevice",
    "soundfile",
    "piper-tts",
    "speechRecognition",
    "meteofrance_api",
    "pyradios",
    "python-vlc",
    "llama_cpp_python",
    "feedparser",
    "yt_dlp",
    "winsdk ; sys_platform == 'win32'",
    "pyobjc-framework-CoreLocation ; sys_platform == 'darwin'",
    "pydbus ; sys_platform == 'linux'"
]

[tool.setuptools.packages.find]
where = ["."]
include = [
    "brain*",
    "config*",
    "fnc*",
    "gestionnaire*",
    "librairy*",
    "neuron*",
    "objet*",
    "keyword*",
    "language*"
]

[tool.setuptools.package-data]
"*" = ["*.json", "*.txt"]
```

---

## 3. Plan d'Action Étape par Étape

### Phase 1 : Préparation & Abstraction du Core (`ArreraNeuronNetwork`)
1. **Créer `pyproject.toml`** à la racine de `ArreraNeuronNetwork`.
2. **Nettoyer `requirements.txt`** dans le Core :
   * Supprimer `customtkinter`, `arrera-tk`, `pillow`, `PyGObject`.
3. **Transformer `gestGUI.py` en contrat abstrait (`IGuiManager`)** :
   * Définir l'interface que toute GUI (Tkinter, GTK) devra respecter.
   * Aucune référence directe à des classes de `gui/`.
4. **Adapter `gestionnaire/gestion.py`** :
   * Remplacer `self.__gui = gestGUI(self)` par `self.__gui = None`.
   * Ajouter les méthodes :
     ```python
     def set_gui_manager(self, gui_manager):
         self.__gui = gui_manager

     def get_gui_manager(self):
         return self.__gui
     ```
5. **Permettre l'injection d'instructions IA** :
   * Dans `gestionnaire/gestIA.py`, ajouter une méthode `load_additional_instructions(prompt_text_or_path)` pour que les GUI puissent ajouter leurs règles de dialogue.
6. **Nettoyer les imports Tkinter résiduels** dans `fnc/fonctionArreraWork.py` et `objet/CArreraDownload.py`.

---

### Phase 2 : Configuration du projet `ann-tkinter`
1. **Conserver dans `ann-tkinter`** :
   * Le dossier `gui/` (toutes les fenêtres Tkinter).
   * Le fichier `src/GUIOpale.py` (ou à la racine).
   * L'implémentation concrète `TkinterGuiManager` (l'ancien `gestGUI.py` adapté pour implémenter l'interface abstraite).
   * Les prompts spécifiques à l'interface dans `instruction_ia/`.
2. **Supprimer de `ann-tkinter` les doublons du Core** :
   * Supprimer `brain/`, `neuron/`, `fnc/`, `objet/`, etc. car ils viendront du package `ann-core`.
3. **Créer le `requirements.txt` de `ann-tkinter`** :
   ```text
   # Dépendance Core (en dev local : pip install -e ../ArreraNeuronNetwork)
   ann-core @ git+https://github.com/ANN-Framework/Arrera-Neuron-Network-Core.git@main
   customtkinter
   arrera-tk
   pillow
   ```
4. **Adapter le `main.py` de `ann-tkinter`** :
   * Initialise le Core `gestionnaire`.
   * Enregistre le gestionnaire Tkinter : `core.set_gui_manager(TkinterGuiManager(core))`.
   * Lance `GUIOpale(core).active()`.

---

### Phase 3 : Validation & Tests
1. **Test Core Headless** : Lancer le Core en ligne de commande pure pour valider qu'aucune erreur d'import Tkinter ne survient.
2. **Liaison locale** : Dans le venv de `ann-tkinter`, exécuter `pip install -e ../ArreraNeuronNetwork`.
3. **Test Tkinter** : Lancer `main.py` dans `ann-tkinter` et tester l'ouverture des fenêtres (Horloge, Agenda, Calculatrice) via la commande vocale ou texte.
