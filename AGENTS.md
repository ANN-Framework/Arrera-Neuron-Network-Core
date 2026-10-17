# AGENTS.md — Arrera Neuron Network (`ann-core`)

Ce dépôt contient **`ann-core`**, le moteur logique, neuronal et vocal **100 % Headless** d'Arrera Neuron Network (utilisé par les assistants Opale, SIX et Ryley).

---

## 1. Règle d'or : Zéro dépendance GUI (100 % Headless)

- **Interdiction absolue d'importer `tkinter`, `customtkinter`, `arrera_tk` ou `PIL`** dans ce dépôt.
- Aucune boîte de dialogue (`filedialog`, `messagebox`) ne doit être ouverte depuis `ann-core`. Les méthodes de configuration ou d'ouverture de fichiers (dans `gestionnaire/gestUserSetting.py`, `fnc/fonctionArreraWork.py`, `fnc/fonctionArreraDownload.py`, etc.) reçoivent directement les chemins en paramètres (`str`).
- Toutes les interactions avec une interface graphique passent exclusivement par le contrat abstrait `gestionnaire/IGestGui.py` via `self._gestionnaire.getGestGUI()`.

---

## 2. Architecture du projet

- **`brain/brain.py` (`ABrain`)** : Point d'entrée haut niveau du moteur. Initialise le `gestionnaire` (`gestionnaire/gestion.py`), le routeur IA (`neuron/IARouter.py`) et les services d'arrière-plan.
- **`gestionnaire/`** :
  - `gestion.py` (`gestionnaire`) : Conteneur central d'injection de dépendances (configurations, fonctions `gestFNC`, historique, sockets, mots-clés, langue et gestionnaire GUI).
  - `IGestGui.py` : Interface abstraite définissant toutes les actions graphiques invocables par le moteur.
  - `HeadlessGuiManager.py` : Implémentation par défaut de `IGestGui` (`has_gui() -> False`) utilisée en mode console/serveur.
  - `gestIA.py` : Gestion du modèle LLM local (`llama_cpp_python`) et construction dynamique du prompt système (`reload_main_prompt()` adapte les outils `INTERFACE` et `CODEHELP` selon `getGestGUI().has_gui()`).
  - `gestFNC.py` : Registre de toutes les classes métier situées dans `fnc/`.
- **`neuron/`** :
  - `IARouter.py` : Routeur principal qui analyse la requête, interroge l'IA ou les neurones spécialisés (`API`, `service`, `time`, `open`, `search`, `work`, `codehelp`, `chatBots`, `interface`) et génère la réponse finale.
  - `core_neuron.py` : Exécuteur des actions déclenchées par les marqueurs de l'IA. En mode Headless (`has_gui() == False`), il retourne les données textuelles (météo, actualités, tâches, agenda, etc.) au lieu d'ouvrir une fenêtre.
- **`fnc/` & `objet/`** : Logique métier pure (météo, agenda, tâches, bureautique Word/Tableur, téléchargement `yt_dlp`, traduction, calculatrice, horloge/minuteur, orthographe, CodeHelp).
- **`librairy/resource_lib.py`** : Résolution des fichiers internes du package (`config/listFete.json`, `instruction_ia/`, `language/`, `keyword/`) relativement à la racine de `ann-core`, même lorsque `ann-core` est importé depuis un projet externe comme `ann-tkinter`.
- **`src/opale.py` & `main.py`** : Lanceur de l'assistant Opale en mode console (Headless).

---

## 3. Lien avec les frontends externes (ex. `ann-tkinter`)

`ann-core` est packagé via `pyproject.toml` (nom du package : `ann-core`).
Lorsqu'un frontend graphique l'utilise :
1. Le frontend installe `ann-core` (ex. `pip install -e ../ArreraNeuronNetwork`).
2. Le frontend instancie `ABrain(config)` ou `gestionnaire(config)`.
3. Le frontend crée sa propre classe héritant de `IGestGui` (avec `has_gui() -> True`) et l'injecte via `gest.set_gui_manager(mon_gui_manager)`, ce qui met à jour le gestionnaire GUI et recharge automatiquement le prompt IA.

---

## 4. Commandes utiles et tests

- **Lancer l'assistant en mode console (Headless)** :
  ```bash
  python main.py
  ```
- **Tests fonctionnels (sans interface graphique)** :
  - `python test-fnc.py` : Teste les fonctions métier (`fnc/`).
  - `python test-user-setting.py` : Teste la lecture/écriture des paramètres utilisateur.
  - `python test-voice.py` : Teste la synthèse et la reconnaissance vocale.
- **Ressources `asset/`** : Seuls les sons système (`asset/sound/micro.mp3`, `asset/horloge/bip.mp3`) et `asset/icon.png` sont conservés dans `ann-core`. Toutes les images d'interface appartiennent au dépôt frontend.
