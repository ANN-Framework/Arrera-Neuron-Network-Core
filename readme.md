# ℹ️ À propos du projet Arrera Neuron Network (`ann-core`)

![Baniere Arrera Neuron Network](https://raw.githubusercontent.com/Arrera-Software/ArreraNeuronNetwork/refs/heads/Version-3/asset/baniere.png)

Moteur logique, neuronal et vocal pour développer des assistants personnels intelligents en **Python 3.14 uniquement**.

Version 4.0 : **Architecture 100 % Headless**, entièrement découplée de toute interface graphique et pilotable en mode autonome (CLI / Serveur) ou connectable à n'importe quel frontend via le contrat `IGestGui`.

*Pour l'interface graphique officielle Tkinter / CustomTkinter, consultez le projet dédié :*  
👉 **[`ann-tkinter`](https://github.com/ANN-Framework/Arrera-Neuron-Network-Tkinter)**

[Readme in english](./readme_en.md) | [Guide d'Intégration](./markdown/INTEGRATION.md) | [Architecture](./markdown/ARCHITECTURE.md)

---

## 🚀 Deux Modes d'Exécution

1. **Mode Headless (Console / Serveur)** :
   Le moteur s'exécute sans aucune interface graphique (`HeadlessGuiManager`). Les requêtes (météo, actualités, tâches, agenda, etc.) sont traitées et restituées textuellement ou vocalement.
2. **Mode Graphique (Frontend externe)** :
   Un frontend (tel que [`ann-tkinter`](https://github.com/ANN-Framework/Arrera-Neuron-Network-Tkinter)) injecte son propre gestionnaire d'affichage via `gest.set_gui_manager(mon_gui)`. Le cerveau IA active automatiquement les outils visuels et délègue l'affichage des fenêtres spécialisées au frontend.

---

## 🧠 Fonctionnalités du Moteur Core

Arrera Neuron Network repose sur un moteur hybride combinant des neurones déterministes ultra-rapides (`core_neuron`) et un routeur IA local GGUF (`IARouter`) :

* **Intelligence Artificielle Locale (GGUF)** : Routage d'intentions (`IARouter`), pré-filtrage à 0 ms (`core_neuron`), chargement à la demande (*Lazy Loading*) et déchargement automatique de la RAM après inactivité avec libération mémoire native multi-OS.
* **Gestion des modèles IA** : Catalogue officiel (Gemma 4, Mistral, Qwen 2.5), recommandation automatique selon le matériel (RAM, GPU VRAM, CPU), téléchargement direct de modèles `.gguf` et support d'un dossier partagé sous Linux (`/arrera/ia_model`).
* **Mémoire & Session** : Mémorisation persistante des faits utilisateur avec dédoublonnage IA (`gestMemoire`) et suivi du contexte conversationnel (`gestSession`).
* **Synthèse et Reconnaissance Vocale** : Synthèse hors-ligne ultra-rapide (`piper-tts`) et reconnaissance vocale (`speechRecognition`), avec signaux sonores système synthétisés directement en mémoire (zéro asset disque requis).
* **Météo & Température** : Prévisions météorologiques et relevés de température en direct via `meteofrance-api`.
* **Résumé (Brief)** : Agrégation matinale, d'après-midi ou du soir combinant actualités, météo et tâches planifiées.
* **GPS & Itinéraires** : Coordonnées géographiques et génération d'itinéraires Google Maps.
* **Actualités & Flux RSS** : Collecte des flux d'actualités par thématique (généraliste, science, tech, etc.).
* **Traduction** : Moteur de traduction multi-langues.
* **Lancement d'Applications & Sites Web** : Gestionnaire universel d'ouverture de logiciels, applications système et URLs configurées.
* **Radio en Streaming** : Écoute et gestion de stations de radio (`pyradios` + `python-vlc`).
* **Outils Arrera** : Moteur de calcul complexe/Pythagore et téléchargement multimédia (`yt-dlp`).
* **Horloge, Chronomètre & Minuteur** : Gestion temporelle complète avec alarmes sonores autonomes.
* **Agenda & Tâches (To-Do)** : Planification d'événements, suivi des tâches du jour, globales et par projet.
* **Recherche Web** : Requêtes web simples ou approfondies (*big search*).
* **Emails Assistés par IA** : Rédaction, correction stylistique et génération de réponses assistées par le modèle local (`fncMail`).
* **Arrera Work (Projets, Bureautique & Agent de Code)** : Manipulation de documents Word (`.docx`, `.odt`), tableurs Excel (`.xlsx`) et mode **Agent IA** pour générer du code et des architectures de projet.
* **Outils de Développement & Git (`CodeHelp`)** : Consultation de documentation (Python, DevDocs, Microsoft, GitHub), organisateur de variables, sélecteur de couleurs et commandes Git natives.
* **Réseau & WebSocket** : Serveur et client WebSocket pour communiquer avec des services externes ou l'éditeur Arrera Markdown.

---

## 📦 Installation & Dépendances

`ann-core` requiert **Python 3.14 exclusivement**.

```bash
# Cloner le dépôt
git clone https://github.com/ANN-Framework/Arrera-Neuron-Network-Core.git
cd Arrera-Neuron-Network-Core

# Installer en mode éditable
pip install -e .
```

Pour les dépendances système (PortAudio, libsndfile, VLC, FFmpeg), consultez :  
👉 **[Dépendances Système du Projet](./markdown/dependency.md)**

---

## 🔌 Intégration dans Votre Application

Pour connecter `ann-core` à votre propre interface graphique ou service :  
👉 **[Guide d'Intégration Core (`markdown/INTEGRATION.md`)](./markdown/INTEGRATION.md)**

---

## 🏗️ Architecture

Pour le détail complet des dossiers et modules :  
👉 **[Architecture Détaillée du Projet](./markdown/ARCHITECTURE.md)**
