# 🧪 Protocole de Test - Assistant Arrera (Opale)

Ce document récapitule les commandes et phrases de test à envoyer à l'assistant pour valider l'ensemble des fonctionnalités du système (**`core_neuron`**, **`IARouter`**, **`HeadlessGuiManager`** et **`gestFNC`**).

---

## ⚡ 1. Intents Rapides (`core_neuron`)

| Test | Phrase à envoyer | Résultat attendu | Validé |
|---|---|---|:---:|
| **Heure** | `Quelle heure est-il ?` | L'assistant donne l'heure courante (format HH:MM) | [ ] |
| **Date** | `Quelle est la date du jour ?` | L'assistant donne la date complète | [ ] |
| **Météo actuelle** | `Quel temps fait-il ?` | Météo locale (description + température) | [ ] |
| **Température** | `Quelle est la température ?` | Température locale actuelle | [ ] |
| **Météo avec ville** | `Quel temps fait-il à Paris ?` | Météo de la ville demandée | [ ] |
| **Lancement Radio** | `Mets France Info` ou `Lance NRJ` | Lancement du flux audio de la radio | [ ] |
| **Arrêt Radio** | `Arrête la radio` | Arrêt de la lecture radio | [ ] |

---

## 🖥️ 2. Ouverture des Interfaces Graphiques (`HeadlessGuiManager`)

| Interface | Phrase à envoyer | Résultat attendu | Validé |
|---|---|---|:---:|
| **Calculatrice** | `Ouvre la calculatrice` | Fenêtre de la calculatrice s'ouvre | [ ] |
| **Agenda** | `Ouvre l'agenda` | Fenêtre de l'agenda s'ouvre | [ ] |
| **Tâches globales** | `Ouvre les tâches` | Fenêtre des tâches s'ouvre | [ ] |
| **Arrera Work** | `Ouvre Arrera Work` | Fenêtre d'accueil Work s'ouvre | [ ] |
| **Traducteur** | `Ouvre le traducteur` | Fenêtre du traducteur s'ouvre | [ ] |
| **Correcteur** | `Ouvre le correcteur d'orthographe` | Fenêtre du correcteur s'ouvre | [ ] |
| **Lecteur vocal** | `Ouvre l'interface de lecture` | Fenêtre de lecture vocale s'ouvre | [ ] |
| **Arrera Download** | `Ouvre Arrera Download` | Fenêtre du téléchargeur YouTube s'ouvre | [ ] |
| **Actus Tech** | `Ouvre les actualités tech` | Fenêtre des actualités tech s'ouvre | [ ] |
| **Actus Sport** | `Affiche les actualités sport` | Fenêtre des actualités sport s'ouvre | [ ] |
| **Actus Science** | `Montre les actualités scientifiques` | Fenêtre des actualités sciences s'ouvre | [ ] |

---

## 📁 3. Arrera Work (Projets, Tâches, Tableur & Word)

| Module | Test | Phrase à envoyer | Résultat attendu | Validé |
|---|---|---|---|:---:|
| **Projet** | Lister | `Liste mes projets` | Liste les projets existants | [ ] |
| **Projet** | Créer | `Crée le projet test_ia` | Création confirmée | [ ] |
| **Projet** | Ouvrir | `Ouvre le projet test_ia` | Projet ouvert | [ ] |
| **Tâches Projet** | Ouvrir GUI | `Ouvre les tâches du projet` | **Fenêtre des tâches du projet ouverte + confirmation vocale sans erreur** | [ ] |
| **Tâches Projet** | Ajouter | `Ajoute la tâche finir le rapport au projet` | Tâche ajoutée au projet | [ ] |
| **Tâches Projet** | Lister | `Liste les tâches du projet` | Liste les tâches du projet actif | [ ] |
| **Projet** | Fermer | `Ferme le projet` | Confirmation de fermeture | [ ] |
| **Tableur** | Ouvrir | `Ouvre le tableur` | Tableur initialisé / ouvert | [ ] |
| **Tableur** | Écrire | `Écris 42 dans la case A1` | Valeur ajoutée en A1 | [ ] |
| **Tableur** | Lire | `Lis le tableur` | Retourne le contenu des cellules | [ ] |
| **Tableur** | Fermer | `Ferme le tableur` | Confirmation de fermeture | [ ] |
| **Word** | Ouvrir | `Ouvre un document Word` | Document ouvert | [ ] |
| **Word** | Écrire | `Écris Bonjour tout le monde dans Word` | Texte écrit dans le document | [ ] |
| **Word** | Lire | `Lis le document Word` | Lit le texte contenu dans le document | [ ] |
| **Word** | Fermer | `Ferme le document Word` | Document fermé | [ ] |

---

## 📅 4. Tâches & Agenda Globaux (`IARouter`)

| Test | Phrase à envoyer | Résultat attendu | Validé |
|---|---|---|:---:|
| **Ajout Tâche** | `Ajoute la tâche Acheter du pain pour aujourd'hui` | Tâche enregistrée avec date du jour | [ ] |
| **Liste Tâches** | `Quelles sont mes tâches aujourd'hui ?` | Énumération des tâches du jour | [ ] |
| **Terminer Tâche** | `Termine la tâche Acheter du pain` | Tâche marquée comme terminée | [ ] |
| **Compter Tâches** | `Combien de tâches j'ai aujourd'hui ?` | Nombre exact de tâches retourné | [ ] |
| **Ajout Calendrier** | `Ajoute un événement Réunion demain à 14:00` | Événement enregistré dans l'agenda | [ ] |
| **Liste Calendrier** | `Quels sont mes événements aujourd'hui ?` | Liste des événements planifiés | [ ] |

---

## ⏱️ 5. Horloge, Minuteur & Chronomètre

| Test | Phrase à envoyer | Résultat attendu | Validé |
|---|---|---|:---:|
| **Minuteur vocal** | `Mets un minuteur de 60 secondes` | Décompte lancé pour 60s | [ ] |
| **Chronomètre** | `Démarre le chronomètre` | Chronomètre démarré | [ ] |
| **Temps Chrono** | `Quel est le temps du chronomètre ?` | Temps écoulé retourné | [ ] |
| **Arrêt Chrono** | `Arrête le chronomètre` | Chronomètre stoppé | [ ] |

---

## 🧭 6. GPS & Localisation

| Test | Phrase à envoyer | Résultat attendu | Validé |
|---|---|---|:---:|
| **Localisation** | `Où est-ce que je suis ?` | Ouvre ou donne la position GPS | [ ] |
| **Département** | `Quel est le département de Lyon ?` | Indique le numéro / nom de département | [ ] |
| **Itinéraire** | `Calcule un itinéraire de Paris à Marseille` | Ouvre l'itinéraire Google Maps | [ ] |

---

## 🧮 7. Calculs, Traduction & Outils

| Test | Phrase à envoyer | Résultat attendu | Validé |
|---|---|---|:---:|
| **Calcul simple** | `Calcule 154 multiplié par 3` | Résultat : `462` | [ ] |
| **Calcul complexe** | `Calcule racine de 144` | Résultat : `12` | [ ] |
| **Traduction** | `Traduis Bonjour en anglais` | Traduction : `Hello` | [ ] |
| **Lecture vocale** | `Lis le texte : Bienvenue dans le système Arrera` | Synthèse vocale prononce la phrase | [ ] |

---

## 🌐 8. Recherche Web & CodeHelp (Développeur)

| Test | Phrase à envoyer | Résultat attendu | Validé |
|---|---|---|:---:|
| **Recherche Web** | `Fais une recherche sur l'intelligence artificielle` | Ouvre la recherche par défaut | [ ] |
| **Moteur spécifique** | `Cherche python sur DuckDuckGo` | Lance la recherche sur DuckDuckGo | [ ] |
| **Doc Python** | `Cherche la doc de asyncio sur python` | Ouvre la documentation Python officielle | [ ] |
| **GitHub Search** | `Cherche sur github des projets machine learning` | Ouvre la recherche GitHub | [ ] |
| **Outil Couleurs** | `Ouvre le sélecteur de couleurs` | Ouvre l'outil sélecteur de couleurs | [ ] |
| **Doc Assistant** | `Ouvre la doc de l'assistant` | Ouvre la page de documentation de l'assistant | [ ] |

---

## 🛑 9. Arrêt du système

| Test | Phrase à envoyer | Résultat attendu | Validé |
|---|---|---|:---:|
| **Arrêt propre** | `Arrête-toi` ou `Au revoir` | Sauvegarde des logs + fermeture de l'application | [ ] |
