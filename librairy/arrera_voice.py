import io
import soundfile as sf
import sounddevice as sd
import numpy as np
from gtts import gTTS
import os
import glob
import json
import requests
import speech_recognition as sr
from gestionnaire.gestion import gestionnaire, jsonWork
from librairy.resource_lib import resource_lib
from piper.voice import PiperVoice
from librairy.audio_data import get_micro_sound_stream


class CArreraVoice:
    def __init__(self, gestionnaire: gestionnaire):
        self.__gestionnaire = gestionnaire
        self.__emplacementSoundMicro = ""
        self.__soundMicro = True
        self.__listWord = []
        self.__nbWord = 0
        self.__outPutText = ""
        self.__resource_lib = resource_lib()
        self.__stop_flag = False
        self.__voice_model_download = True
        self.__trigger_status = 0
        self.__voice_name = "google"
        self.__tts = None
        self.__loaded_voice_name = None

        dectos = self.__gestionnaire.getOSObjet()

        if dectos.osLinux() or dectos.osMac():
            home = os.path.expanduser("~")
            self.__model_dir = os.path.join(home, ".config", "arrera-assistant", "voice_model")
        elif dectos.osWindows():
            home = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
            self.__model_dir = os.path.join(home, "arrera-assistant", "voice_model")
        else:
            self.__model_dir = os.path.join(os.path.expanduser("~"), ".arrera-assistant", "voice_model")

        os.makedirs(self.__model_dir, exist_ok=True)
        if not os.path.exists(self.__resource_lib.tmp_directory()):
            os.makedirs(self.__resource_lib.tmp_directory(), exist_ok=True)

        self.__json_conf = jsonWork(self.__gestionnaire.getUserConf().getVoicePath())

        tom_onnx = os.path.join(self.__model_dir, "fr_FR-tom-medium.onnx")
        tom_json = tom_onnx + ".json"
        siwis_onnx = os.path.join(self.__model_dir, "fr_FR-siwis-medium.onnx")
        siwis_json = siwis_onnx + ".json"

        if self.__gestionnaire.getNetworkObjet().getEtatInternet():
            if not os.path.exists(tom_onnx) or not self.__is_valid_json_file(tom_json):
                if not self.__download_model(
                        "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx?download=true",
                        "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx.json?download=true",
                        "tom"):  # Tom
                    self.__voice_model_download = False

            if not os.path.exists(siwis_onnx) or not self.__is_valid_json_file(siwis_json):
                if not self.__download_model(
                        "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx?download=true",
                        "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json?download=true",
                        "siwis"):  # Siwis
                    self.__voice_model_download = False

        if os.path.exists(tom_onnx) and self.__is_valid_json_file(tom_json):
            self.__json_conf.setValeurJson("tom_onnx", tom_onnx)
            self.__json_conf.setValeurJson("tom_json", tom_json)

        if os.path.exists(siwis_onnx) and self.__is_valid_json_file(siwis_json):
            self.__json_conf.setValeurJson("siwis_onnx", siwis_onnx)
            self.__json_conf.setValeurJson("siwis_json", siwis_json)

        self.__list_model = glob.glob(os.path.join(self.__model_dir, "*.onnx"))

        self.loadConfig()
        self.load_voice_model()

    def __is_valid_json_file(self, filepath):
        if not os.path.exists(filepath):
            return False
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except Exception:
            return False

    def __download_model(self, link_onnx: str, link_json: str, voice_model: str):
        if not link_onnx and not link_json:
            return False

        if voice_model != "tom" and voice_model != "siwis":
            return False

        json_file = link_json.split('/')[-1].replace('?download=true', '')
        onnx_path = link_onnx.split('/')[-1].replace('?download=true', '')

        try:
            response = requests.get(link_onnx, stream=True, timeout=30)

            if response.status_code != 200:
                return False

            full_path = os.path.join(self.__model_dir, onnx_path)
            with open(full_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            self.__json_conf.setValeurJson(voice_model + "_onnx", full_path)

            response = requests.get(link_json, stream=True, timeout=30)

            if response.status_code != 200:
                return False

            full_path = os.path.join(self.__model_dir, json_file)
            with open(full_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            self.__json_conf.setValeurJson(voice_model + "_json", full_path)

            return True

        except Exception as e:
            print(e)
            return False

    def get_list_voice_model(self):
        return ["tom", "siwis", "google"]

    def loadConfig(self):
        sound_val = self.__gestionnaire.getUserConf().getSoundMicro()
        self.__soundMicro = (sound_val in ("1", 1, True))
        self.__listWord = self.__gestionnaire.getUserConf().getListWord()
        self.__nbWord = len(self.__listWord)
        self.__voice_name = self.__gestionnaire.getUserConf().get_voice_selected() or "google"

    def load_voice_model(self):
        if self.__voice_name == "google":
            self.__tts = None
            self.__loaded_voice_name = "google"
            return True
        else:
            if self.__tts is not None and self.__loaded_voice_name == self.__voice_name:
                return True
            try:
                if self.__voice_name == "tom":
                    onnx_path = self.__json_conf.getContentJsonFlag("tom_onnx") or os.path.join(self.__model_dir, "fr_FR-tom-medium.onnx")
                elif self.__voice_name == "siwis":
                    onnx_path = self.__json_conf.getContentJsonFlag("siwis_onnx") or os.path.join(self.__model_dir, "fr_FR-siwis-medium.onnx")
                else:
                    return False

                if not onnx_path or not os.path.exists(onnx_path):
                    return False

                self.__tts = PiperVoice.load(onnx_path)
                self.__loaded_voice_name = self.__voice_name
                return True
            except Exception as e:
                print(e)
                self.__tts = None
                return False

    def say(self, text: str):
        if text != "":
            self.loadConfig()
            if self.__voice_name == "google":
                if self.__gestionnaire.getNetworkObjet().getEtatInternet():
                    try:
                        tts = gTTS(text=text, lang='fr', slow=False)
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)

                        data, samplerate = sf.read(fp, dtype='int16')
                        sd.play(data, samplerate=samplerate)
                        sd.wait()
                        return True
                    except Exception as e:
                        print(e)
                        return False
                else:
                    return False
            elif self.__voice_name == "tom" or self.__voice_name == "siwis":
                if self.__tts is None or self.__loaded_voice_name != self.__voice_name:
                    if not self.load_voice_model():
                        return False
                try:
                    audio_bytes = b"".join(
                        chunk.audio_int16_bytes for chunk in self.__tts.synthesize(text))
                    if len(audio_bytes) == 0:
                        return False
                    audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
                    frequence = self.__tts.config.sample_rate
                    sd.play(audio_data, samplerate=frequence)
                    sd.wait()
                    return True
                except Exception as e:
                    print(e)
                    return False
        else:
            return False

    def playFile(self, file_or_stream):
        """
        Lit un fichier audio depuis un chemin disque (str) ou un flux mémoire (io.BytesIO).
        """
        try:
            # Si c'est un chemin de fichier qui n'existe pas, on abandonne
            if isinstance(file_or_stream, str) and not os.path.exists(file_or_stream):
                print(f"Fichier introuvable : {file_or_stream}")
                return

            data, samplerate = sf.read(file_or_stream, dtype='int16')
            sd.play(data, samplerate=samplerate)
            sd.wait()
        except Exception as e:
            print(f"Erreur lecture audio : {e}")

    def stop_listen(self):
        self.__stop_flag = True

    def listen(self):
        self.loadConfig()
        if self.__soundMicro:
            self.playFile(get_micro_sound_stream())

        r = sr.Recognizer()
        self.__stop_flag = False
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = None
            while not self.__stop_flag:
                try:
                    audio = r.listen(source, timeout=0.5)
                    break
                except sr.WaitTimeoutError:
                    continue

        if self.__stop_flag or audio is None:
            self.__outPutText = ""
            return -1

        try:
            text = r.recognize_google(audio, language='fr-FR')
            self.__outPutText = text
            return 0
        except sr.UnknownValueError:
            return -1
        except sr.RequestError as e:
            return -2

    def getTextMicro(self):
        return self.__outPutText

    def getNbWord(self):
        return self.__nbWord

    def get_trigger_status(self):
        return self.__trigger_status

    def trigerWord(self):
        self.loadConfig()
        self.__trigger_status = 0
        if self.__nbWord == 0:
            self.__trigger_status = -3
            return -3

        r = sr.Recognizer()
        self.__stop_flag = False
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = None
            while not self.__stop_flag:
                try:
                    audio = r.listen(source, timeout=0.5)
                    break
                except sr.WaitTimeoutError:
                    continue

        if self.__stop_flag or audio is None:
            self.__trigger_status = -4  # Code pour dire qu'on a arrêté manuellement
            return -4

        try:
            text = r.recognize_google(audio, language='fr-FR')
            for word in self.__listWord:
                if word in text:
                    self.__trigger_status = 1
                    return 1
            self.__trigger_status = 0
            return 0
        except sr.UnknownValueError:
            self.__trigger_status = -1
            return -1
        except sr.RequestError as e:
            self.__trigger_status = -2
            return -2