# 🛠️ Guide Développeur — Intégrer `ann-core` dans un Projet Python

Ce guide s'adresse aux développeurs qui souhaitent intégrer le moteur d'assistant intelligent **Arrera Neuron Network (`ann-core`)** dans leur propre application Python (script CLI, API web FastAPI/Flask, bot Discord/Telegram, projet domotique/IoT, application de bureau, etc.).

---

## 📋 Table des Matières

1. [Prérequis & Installation](#1-prérequis--installation)
2. [Démarrage Rapide (Hello World en 10 lignes)](#2-démarrage-rapide-hello-world)
3. [Comprendre le Fonctionnement (`ABrain`)](#3-comprendre-le-fonctionnement-abrain)
4. [Cas d'Usage & Exemples Concrets](#4-cas-dusage--exemples-concrets)
   - [Cas A : Assistant Interactif en Console (CLI)](#cas-a--assistant-interactif-en-console-cli)
   - [Cas B : API Web (FastAPI / Microservice)](#cas-b--api-web-fastapi--microservice)
   - [Cas C : Bot Discord / Messagerie](#cas-c--bot-discord--messagerie)
5. [Accès Direct aux Fonctions Métier (Sans passer par l'IA)](#5-accès-direct-aux-fonctions-métier)
6. [Configuration Avancée (`confNeuron`)](#6-configuration-avancée-confneuron)
7. [Activer la Voix (TTS & STT hors-ligne)](#7-activer-la-voix-tts--stt-hors-ligne)
8. [Mémoire Utilisateur & Gestion de Session](#8-mémoire-utilisateur--gestion-de-session)
9. [Bonnes Pratiques & Cycle de Vie](#9-bonnes-pratiques--cycle-de-vie)

---

## 1. Prérequis & Installation

### Prérequis Système
* **Python 3.14** exclusivement.
* Bibliothèques système pour l'audio et les médias :
  * **Linux (Debian/Ubuntu)** : `sudo apt install python3.14-dev portaudio19-dev libsndfile1 vlc ffmpeg`
  * **macOS** : `brew install portaudio libsndfile vlc ffmpeg`
  * **Windows** : VLC 64-bit et FFmpeg ajoutés au `PATH`.

### Installation du Package
Ajoutez `ann-core` dans votre environnement virtuel :

```bash
# Installation depuis le dépôt Git
pip install git+https://github.com/ANN-Framework/Arrera-Neuron-Network-Core.git@version4.0

# Ou en local (mode éditable) si vous avez cloné le dépôt :
pip install -e /chemin/vers/ArreraNeuronNetwork
```

---

## 2. Démarrage Rapide (Hello World)

Voici l'exemple minimal pour poser une question en langage naturel à l'assistant et obtenir une réponse textuelle :

```python
from config.confNeuron import confNeuron
from brain.brain import ABrain

# 1. Configurer l'assistant
config = confNeuron(
    name="MonAssistant",
    active_ia=True,      # Active le LLM local (GGUF)
    active_voice=False   # Mode texte uniquement
)

# 2. Instancier et démarrer le moteur
assistant = ABrain(config=config)
assistant.start()

# 3. Poser une question
reponse = assistant.requet("Donne-moi l'heure et la météo du jour")
print(f"Assistant : {reponse}")

# 4. Fermer proprement l'assistant
assistant.destroy()
```

---

## 3. Comprendre le Fonctionnement (`ABrain`)

La classe `ABrain` (`brain.brain.ABrain`) est le **point d'entrée unique** de l'assistant :

* **`assistant.start()`** : Démarre les services d'arrière-plan (démons timers, serveurs WebSocket, chargement des mots-clés).
* **`assistant.requet(text: str) -> str`** : Envoie une requête utilisateur. Le moteur analyse la demande, choisit instantanément entre un neurone déterministe (0 ms) ou le modèle local LLM GGUF, exécute l'action appropriée (météo, calcul, actualités, agenda, etc.) et retourne la réponse rédigée.
* **`assistant.destroy()`** : Arrête les threads en arrière-plan, libère la mémoire vive et ferme les sockets.

---

## 4. Cas d'Usage & Exemples Concrets

### Cas A : Assistant Interactif en Console (CLI)

Un script complet de chat en boucle dans votre terminal :

```python
import sys
from config.confNeuron import confNeuron
from brain.brain import ABrain

def main():
    conf = confNeuron(name="Jarvis", active_ia=True, active_voice=False)
    assistant = ABrain(config=conf)
    assistant.start()

    print(f"--- Assistant {conf.name} prêt (tapez 'quitter' pour sortir) ---")
    try:
        while True:
            user_input = input("\nVous > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quitter", "exit", "quit"]:
                break

            response = assistant.requet(user_input)
            print(f"{conf.name} > {response}")
    finally:
        assistant.destroy()
        print("Assistant arrêté.")

if __name__ == "__main__":
    main()
```

---

### Cas B : API Web (FastAPI / Microservice)

Intégrez l'assistant dans une API REST pour alimenter une application web ou mobile :

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from config.confNeuron import confNeuron
from brain.brain import ABrain

assistant: ABrain = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global assistant
    # Démarrage au lancement du serveur
    config = confNeuron(name="ServeurBot", active_ia=True, active_voice=False)
    assistant = ABrain(config=config)
    assistant.start()
    yield
    # Nettoyage à l'arrêt du serveur
    assistant.destroy()

app = FastAPI(lifespan=lifespan)

class QueryRequest(BaseModel):
    message: str

class QueryResponse(BaseModel):
    reply: str

@app.post("/api/chat", response_model=QueryResponse)
def chat_endpoint(req: QueryRequest):
    if not assistant:
        raise HTTPException(status_code=500, detail="Moteur non initialisé")
    
    reply = assistant.requet(req.message)
    return QueryResponse(reply=reply)
```

---

### Cas C : Bot Discord / Messagerie

Exemple d'intégration asynchrone avec `discord.py` :

```python
import discord
from config.confNeuron import confNeuron
from brain.brain import ABrain

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Initialisation du moteur ANN
conf = confNeuron(name="BotDiscord", active_ia=True, active_voice=False)
assistant = ABrain(config=conf)
assistant.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Si le bot est mentionné ou préfixé par !ia
    if message.content.startswith("!ia "):
        prompt = message.content[4:]
        # Exécution de la requête dans un thread pour ne pas bloquer la boucle asyncio
        reponse = await client.loop.run_in_executor(None, assistant.requet, prompt)
        await message.channel.send(reponse)

@client.event
async def on_close():
    assistant.destroy()

client.run("VOTRE_TOKEN_DISCORD")
```

---

## 5. Accès Direct aux Fonctions Métier

Si vous n'avez pas besoin du routeur en langage naturel mais souhaitez utiliser directement les modules fonctionnels développés dans ANN :

```python
from config.confNeuron import confNeuron
from brain.brain import ABrain

assistant = ABrain(config=confNeuron(name="Dev"))
gest = assistant.getGestionnaire()
fnc = gest.getGestFNC()

# 1. Météo
meteo_data = fnc.getFNCMeteo().get_meteo_actuelle()
print("Météo :", meteo_data)

# 2. Actualités (RSS)
news = fnc.getFNCActu().get_actu_general()
print("Derniers titres :", [a['titre'] for a in news[:3]])

# 3. Tâches (To-Do List)
fnc.getFNCTache().add_task("Acheter du café")
taches = fnc.getFNCTache().get_all_task()
print("Tâches en cours :", taches)

# 4. Traduction
traduction = fnc.getFNCTraduction().translate(text="Bonjour le monde", dest="en")
print("Traduit :", traduction)
```

---

## 6. Configuration Avancée (`confNeuron`)

Vous pouvez personnaliser finement le comportement de l'assistant lors de l'instanciation de `confNeuron` :

```python
from config.confNeuron import confNeuron

config = confNeuron(
    name="Opale",                # Nom de l'assistant (utilisé dans les prompts)
    active_ia=True,              # Active le LLM local (llama-cpp)
    active_voice=False,          # Active la synthèse et la reconnaissance vocale
    ia_os_directory="/models"    # Dossier optionnel personnalisé pour les modèles GGUF
)
```

---

## 7. Activer la Voix (TTS & STT hors-ligne)

Pour concevoir un assistant vocal complet :

```python
from config.confNeuron import confNeuron
from brain.brain import ABrain

config = confNeuron(
    name="Opale",
    active_ia=True,
    active_voice=True  # Active piper-tts et speechRecognition
)

assistant = ABrain(config=config)
assistant.start()

# L'assistant répond vocalement et peut écouter via le microphone :
voice_engine = assistant.getGestionnaire().getVoiceEngine()
# Parler directement
voice_engine.say("Bonjour, comment puis-je vous aider aujourd'hui ?")
```

---

## 8. Mémoire Utilisateur & Gestion de Session

`ann-core` intègre une mémoire long-terme persistante et une mémoire de session court-terme :

```python
gest = assistant.getGestionnaire()

# Mémoire long-terme (persiste dans user.json)
memoire = gest.getGestMemoire()
memoire.memoriser("L'utilisateur s'appelle Alice et est développeuse Python.")

# Contexte de session court-terme
session = gest.getGestSession()
session.set_context("sujet_en_cours", "Déploiement Docker")
```

---

## 9. Bonnes Pratiques & Cycle de Vie

* **Ne créez pas plusieurs instances de `ABrain` simultanément** : Un seul cerveau doit tourner par processus pour éviter les conflits d'écoute audio ou de chargement du modèle GGUF.
* **Libération de la RAM automatique** : Le moteur LLM se charge à la demande (*Lazy Loading*) et se décharge tout seul de la RAM après quelques minutes sans requête.
* **Toujours invoquer `assistant.destroy()`** : Dans un bloc `try...finally` ou dans le gestionnaire d'arrêt de votre application, pour clore proprement les processus en arrière-plan.
