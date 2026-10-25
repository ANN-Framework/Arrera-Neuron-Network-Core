# ℹ️ À propos du projet Arrera Neuron Network

![Baniere Arrera Neuron Network](https://raw.githubusercontent.com/Arrera-Software/ArreraNeuronNetwork/refs/heads/Version-3/asset/baniere.png)

Projet qui a pour but de créer la base permettant de développer des assistants personnels en **Python 3.14 uniquement** (Architecture modulaire Headless `ann-core` découplée de l'interface graphique).

[Readme in english](./readme_en.md) 

## Fonctionnalités

L'assistant Arrera Neuron Network (Version 4.0) repose sur une architecture hybride pilotée par un moteur IA local GGUF (`core_neuron` + `IARouter`) pour répondre en langage naturel à diverses requêtes :
*   **Intelligence Artificielle Locale (GGUF)** : Routage intelligent (`IARouter`), pré-filtrage rapide (`core_neuron`), chargement à la demande (*Lazy Loading*) et libération automatique de la RAM après inactivité.
*   **Gestion des modèles IA** : Catalogue intégré (Gemma 4, Mistral, Qwen 2.5), recommandation automatique selon le matériel (RAM, VRAM GPU, CPU), téléchargement de modèles personnalisés par lien direct `.gguf` et support d'un dossier partagé OS sous Linux (`/arrera/ia_model`).
*   **Mémoire & Session** : Mémorisation persistante des informations utilisateur (`gestMemoire`) et suivi du contexte de conversation (`gestSession`).
*   **Météo & Température** : Donne la météo et la température actuelles ou les prévisions (domicile, travail ou localisation actuelle).
*   **Résumé (Brief)** : Fournit un résumé des actualités, de la météo et des tâches (brief du matin ou résumé à la demande).
*   **GPS** : Donne les coordonnées géographiques actuelles et permet de lancer un itinéraire Google Maps (point de départ et d'arrivée).
*   **Actualités** : Donne les dernières actualités (générales, tech, etc.).
*   **Traduction** : Traduction de texte et ouverture de l'outil de traduction.
*   **Ouverture de logiciels & sites web** : Ouvre des logiciels configurés par l'utilisateur, des applications système ou des sites web enregistrés (YouTube, YouTube Music, etc.).
*   **Radio** : Lance des stations de radio (Europe 1, France Info, NRJ, Skyrock, etc.) ou arrête la radio.
*   **Outils Arrera** : Ouvre des outils internes comme le téléchargeur vidéo (`Arrera Download`) ou les modes de calculatrice (complexe, Pythagore).
*   **Heure, Date & Outils de temps** : Donne l'heure/la date actuelle et gère le chronomètre, l'horloge ou le minuteur.
*   **Agenda & Tâches** : Gestion complète du calendrier et de la liste des tâches (ajout, suppression, marquage comme terminé, consultation).
*   **Recherche Internet** : Effectue des recherches simples ou approfondies sur le moteur de recherche configuré.
*   **Calculs, Lecture & Orthographe** : Calculs mathématiques, synthèse vocale hors-ligne (`piper-tts`) et correction orthographique assistée par IA.
*   **Emails** : Rédaction, correction et réponse aux e-mails assistées par l'IA (`fncMail`).
*   **Arrera Work (Projets, Tableur & Traitement de texte)** : Création et gestion de projets, édition de fichiers Word/Excel (somme, moyenne, min, max) et **mode Agent de code** avec génération de fichiers par IA.
*   **Outils de développement & Git (`CodeHelp`)** : Recherche de documentation (DevDocs, Microsoft, Python, GitHub), organisateur de variables, sélecteur de couleurs et intégration des commandes Git (`status`, `commit`, `push`, `branch`, `log`).
*   **Modes d'affichage & Réseau** : Activation des modes d'interface (mode 1 à 6) et serveur/client WebSocket pour interagir avec des services externes et "Arrera Markdown".
*   **Fermeture** : Gère la fermeture de l'assistant ou des modes.

# Architecture 

[Voir l'architecture du projet](./markdown/ARCHITECTURE.md)

[Voir l'architecture modulaire Headless (v4.0)](./markdown/ARCHITECTURE_MODULAIRE_ANN.md)

# Dépendance du projet 

[Voir les dépendances du projet](./markdown/dependency.md)