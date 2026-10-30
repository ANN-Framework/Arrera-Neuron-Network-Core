import sys
import os

# Permettre l'import depuis la racine du projet ArreraNeuronNetwork
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from librairy.audio_data import get_micro_sound_stream, get_bip_sound_stream
from config.confNeuron import confNeuron
from gestionnaire.gestion import gestionnaire
import soundfile as sf
import sounddevice as sd


def test_audio():
    print("=" * 60)
    print("  Arrera Neuron Network - Test Audio en Mémoire (audio_data)")
    print("=" * 60)

    # 1. Vérification du décodage des flux mémoire
    print("\n[1/3] Vérification des données audio en RAM...")
    try:
        data_micro, sr_micro = sf.read(get_micro_sound_stream(), dtype="int16")
        dur_micro = len(data_micro) / sr_micro
        print(f"  ✓ Son Micro : {sr_micro} Hz | Durée : {dur_micro:.2f}s | Échantillons : {len(data_micro)}")

        data_bip, sr_bip = sf.read(get_bip_sound_stream(), dtype="int16")
        dur_bip = len(data_bip) / sr_bip
        print(f"  ✓ Son Bip   : {sr_bip} Hz | Durée : {dur_bip:.2f}s | Échantillons : {len(data_bip)}")
    except Exception as e:
        print(f"  ✗ Erreur de décodage audio : {e}")
        return

    # 2. Test via CArreraVoice (playFile avec flux mémoire)
    print("\n[2/3] Initialisation de CArreraVoice...")
    conf = confNeuron(
        name="Opale",
        lang="fr",
        bute="Test Audio",
        createur="Arrera",
        voiceAssistant=True
    )
    gest = gestionnaire(conf)
    arr_voice = gest.getArrVoice()

    while True:
        print("\n" + "-" * 40)
        print("Menu de test audio :")
        print("  1. Jouer le son Micro (activation micro)")
        print("  2. Jouer le son Bip (alarme / horloge)")
        print("  3. Jouer les deux sons à la suite")
        print("  0. Quitter")
        print("-" * 40)

        choix = input("Votre choix (0-3) : ").strip()

        if choix == "1":
            print("🔊 Lecture du son Micro via CArreraVoice.playFile()...")
            arr_voice.playFile(get_micro_sound_stream())
            print("✓ Fin de lecture.")
        elif choix == "2":
            print("🔊 Lecture du son Bip via CArreraVoice.playFile()...")
            arr_voice.playFile(get_bip_sound_stream())
            print("✓ Fin de lecture.")
        elif choix == "3":
            print("🔊 Lecture du son Micro...")
            arr_voice.playFile(get_micro_sound_stream())
            print("🔊 Lecture du son Bip...")
            arr_voice.playFile(get_bip_sound_stream())
            print("✓ Fin de lecture.")
        elif choix in ("0", "q", "quit", "exit"):
            print("Fermeture du test.")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    test_audio()
