from gestionnaire.gestion import gestionnaire
from config.confNeuron import confNeuron
import os

# Initialisation de la configuration et du gestionnaire
conf = confNeuron(
    name="Opale",
    lang="fr",
    icon="asset/icon.png",
    asset="asset/",
    bute="Tester Arrera Voice",
    createur="Pauchet Baptiste",
    listFonction=[],
    moteurderecherche="google",
    etatService=1,
    etatTime=1,
    etatOpen=1,
    etatSearch=1,
    etatChatbot=1,
    etatApi=1,
    etatCodehelp=1,
    etatWork=1,
    etatSocket=0,
    lienDoc="",
    fichierLangue="language/vouvoiment/",
    fichierKeyword="keyword/",
    voiceAssistant=True
)

gest = gestionnaire(conf)
arr_voice = gest.getArrVoice()
user_conf = gest.getUserConf()


def test_tts_current():
    print("\n--- Test TTS (Voix Actuelle) ---")
    current_voice = user_conf.get_voice_selected() or "google"
    print(f"Voix actuellement sélectionnée : {current_voice}")
    text = input("Texte à prononcer (Appuyez sur Entrée pour le texte par défaut) : ").strip()
    if not text:
        text = "Bonjour ! Je suis l'assistant vocal Arrera, test de la synthèse vocale."

    print(f"Synthèse vocale en cours avec '{current_voice}'...")
    success = arr_voice.say(text)
    if success:
        print("✅ Synthèse vocale réussie !")
    else:
        print("❌ Échec de la synthèse vocale.")


def test_all_voices():
    print("\n--- Test de toutes les voix disponibles ---")
    voices = arr_voice.get_list_voice_model()
    text = input("Texte à prononcer (Appuyez sur Entrée pour 'Ceci est un test de la voix') : ").strip()
    if not text:
        text = "Ceci est un test de la voix."

    for v in voices:
        print(f"\n-> Passage à la voix : {v}")
        user_conf.set_voice(v)
        arr_voice.loadConfig()
        print(f"Lecture en cours avec {v}...")
        success = arr_voice.say(f"{text} {v}")
        if success:
            print(f"✅ Voix '{v}' : Succès")
        else:
            print(f"❌ Voix '{v}' : Échec")


def change_voice():
    print("\n--- Changer la voix active ---")
    voices = arr_voice.get_list_voice_model()
    print("Modèles disponibles :")
    for i, v in enumerate(voices, 1):
        print(f"  {i}. {v}")

    choix = input("Choisissez le nom ou le numéro de la voix : ").strip()
    selected_voice = None
    if choix.isdigit() and 1 <= int(choix) <= len(voices):
        selected_voice = voices[int(choix) - 1]
    elif choix in voices:
        selected_voice = choix

    if selected_voice:
        if user_conf.set_voice(selected_voice):
            arr_voice.loadConfig()
            print(f"✅ Voix configurée sur : {selected_voice}")
            # Tester le chargement
            if arr_voice.load_voice_model():
                print("✅ Modèle chargé avec succès en mémoire.")
            else:
                print("⚠️ Impossible de charger le modèle en mémoire.")
        else:
            print("❌ Erreur lors de la sauvegarde de la voix.")
    else:
        print("❌ Choix invalide.")


def test_listen():
    print("\n--- Test Reconnaissance Vocale (Microphone) ---")
    print("Parlez dans votre microphone après le signal sonore...")
    res = arr_voice.listen()
    if res == 0:
        texte = arr_voice.getTextMicro()
        print(f"✅ Texte reconnu : \"{texte}\"")
    elif res == -1:
        print("⚠️ Aucun texte détecté ou non compris.")
    elif res == -2:
        print("❌ Erreur de requête (connexion Internet requise pour Google STT).")


def test_trigger_word():
    print("\n--- Test Mot Déclencheur (Trigger Word) ---")
    mots = user_conf.getListWord()
    print(f"Mots configurés : {mots}")
    if not mots:
        print("⚠️ Aucun mot déclencheur dans la configuration.")
        add = input("Voulez-vous ajouter un mot clé (ex: 'bonjour', 'opale') ? (o/n) : ").strip().lower()
        if add == 'o':
            mot = input("Mot à ajouter : ").strip().lower()
            if mot:
                user_conf.addWord(mot)
                arr_voice.loadConfig()
                mots = user_conf.getListWord()
                print(f"Mots actifs : {mots}")
            else:
                return
        else:
            return

    print("Dites une phrase contenant un des mots clés...")
    res = arr_voice.trigerWord()
    status = arr_voice.get_trigger_status()
    print(f"Statut déclencheur : {status}")
    if res == 1:
        print("✅ Mot déclencheur DÉTECTÉ !")
    elif res == 0:
        print("ℹ️ Phrase comprise mais AUCUN mot déclencheur trouvé.")
    elif res == -1:
        print("⚠️ Parole non comprise.")
    elif res == -2:
        print("❌ Erreur de service Google STT.")
    elif res == -3:
        print("❌ Aucun mot configuré.")


def test_play_file():
    print("\n--- Test Lecture de fichier audio (sounddevice / soundfile) ---")
    sound_path = "../asset/sound/micro.mp3"
    custom_path = input(f"Chemin du fichier (Appuyez sur Entrée pour '{sound_path}') : ").strip()
    if custom_path:
        sound_path = custom_path

    if os.path.exists(sound_path):
        print(f"Lecture du fichier '{sound_path}'...")
        arr_voice.playFile(sound_path)
        print("✅ Fin de la lecture.")
    else:
        print(f"❌ Le fichier '{sound_path}' n'existe pas.")


def view_diagnostics():
    print("\n================ DIAGNOSTIC DU SYSTÈME VOCAL ================")
    print(f"Voix sélectionnée (User Config) : {user_conf.get_voice_selected()}")
    print(f"Voix disponibles               : {arr_voice.get_list_voice_model()}")
    print(f"Son du micro activé            : {user_conf.getSoundMicro()}")
    print(f"Mots déclencheurs              : {user_conf.getListWord()}")
    print(f"Connexion Internet             : {'Oui' if gest.getNetworkObjet().getEtatInternet() else 'Non'}")
    
    # Vérification des dossiers de modèles
    home = os.path.expanduser("~")
    dectos = gest.getOSObjet()
    if dectos.osLinux() or dectos.osMac():
        model_dir = os.path.join(home, ".config", "arrera-assistant", "voice_model")
    else:
        model_dir = os.path.join(home, "AppData", "Roaming", "arrera-assistant", "voice_model")
    
    print(f"Dossier des modèles Piper      : {model_dir}")
    if os.path.exists(model_dir):
        files = os.listdir(model_dir)
        print(f"Fichiers dans le dossier       : {files if files else 'Dossier vide'}")
    else:
        print("Dossier des modèles non existant sur le disque.")
    print("=============================================================")


def main():
    while True:
        print("\n" + "=" * 55)
        print("         MENU DE TEST ARRERA VOICE")
        print("=" * 55)
        print("1. [TTS] Dire un texte avec la voix active")
        print("2. [TTS] Tester toutes les voix à la suite (Google, Tom, Siwis)")
        print("3. [TTS] Changer la voix active")
        print("4. [STT] Tester l'écoute microphone (listen)")
        print("5. [STT] Tester la détection de mot clé (trigerWord)")
        print("6. [Audio] Tester la lecture d'un fichier audio (playFile)")
        print("7. [Infos] Afficher le diagnostic vocal")
        print("0. Quitter")
        print("=" * 55)

        choix = input("Votre choix : ").strip()

        match choix:
            case "1":
                test_tts_current()
            case "2":
                test_all_voices()
            case "3":
                change_voice()
            case "4":
                test_listen()
            case "5":
                test_trigger_word()
            case "6":
                test_play_file()
            case "7":
                view_diagnostics()
            case "0":
                print("Fin des tests. Au revoir !")
                break
            case _:
                print("Option invalide, veuillez réessayer.")


if __name__ == "__main__":
    main()
