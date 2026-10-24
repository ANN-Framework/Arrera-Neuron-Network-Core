import gc
import os
from llama_cpp import Llama

class ArreraIALoad:
    def __init__(self):
        self.__model_type = None
        self.__model = None
        self.__tokeniser = None
        self.__classes = None
        self.__is_loaded = False
        self.__system_context_is_loaded = False
        self.__system_instructions = []

    # Methode private
    # Methode private
    def __predict_gguf_model(self, prompt, max_tokens=512, enable_consigne_langue: bool = True, as_json: bool = True):
        if enable_consigne_langue:
            consigne_langue = "\n\n(Réponds impérativement en français, même si je parle anglais ou technique)."
        else:
            consigne_langue = ""

        user_content = prompt + consigne_langue
        messages = []
        fallback_messages = []

        if self.__system_context_is_loaded and len(self.__system_instructions) > 0:
            combined_system_prompt = "Utilise les informations suivantes pour aider l'utilisateur :\n\n"
            combined_system_prompt += "\n\n---\n\n".join(self.__system_instructions)

            messages.append({"role": "system", "content": combined_system_prompt})
            messages.append({"role": "user", "content": user_content})

            final_prompt = combined_system_prompt + "\n\n---\n\nRequête utilisateur : " + user_content
            fallback_messages.append({"role": "user", "content": final_prompt})
        else:
            messages.append({"role": "user", "content": user_content})
            fallback_messages = messages

        kwargs = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.1,
            "top_p": 0.9,
            "repeat_penalty": 1.15,
        }
        if as_json:
            kwargs["response_format"] = {"type": "json_object"}
        else:
            kwargs["stop"] = [
                "\nUtilisateur :",
                "\nUtilisateur:",
                "\nUser :",
                "\nUser:",
                "\nDemande actuelle de l'utilisateur :",
                "=== L'UTILISATEUR ===",
                "=== TA PERSONNALITÉ ===",
            ]

        try:
            output = self.__model.create_chat_completion(**kwargs)
        except Exception:
            kwargs["messages"] = fallback_messages
            output = self.__model.create_chat_completion(**kwargs)

        return output['choices'][0]['message']['content']

    # Methode public

    def add_system_instruction(self, instruction:str):
        if instruction.strip():
            self.__system_instructions.append(instruction)
            self.__system_context_is_loaded = True
            return True
        return False


    def load_help_file(self, file_path: str):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.add_system_instruction(content)
                return True
            except Exception as e:
                print(f"Erreur de lecture : {e}")
                return False
        else:
            return False

    def unload_help(self):
        self.__system_context_is_loaded = False
        self.__system_instructions = []

    def unload_model(self):
        """Désinstancie proprement le modèle Llama chargé en mémoire."""
        if self.__model is not None:
            try:
                if hasattr(self.__model, 'close'):
                    self.__model.close()
            except Exception:
                pass
            del self.__model
            self.__model = None
            gc.collect()
        self.__is_loaded = False
        self.__system_context_is_loaded = False
        self.__system_instructions = []

    def load_model_gguf(self, model_path:str, n_ctx:int=2048):
        if not os.path.exists(model_path):
            raise ValueError(f"Le fichier modèle n'existe pas : {model_path}")

        # Si un modèle est déjà chargé, le désinstancier d'abord
        if self.__is_loaded or self.__model is not None:
            self.unload_model()

        try:
            self.__model = Llama(
                model_path=model_path,
                n_ctx=n_ctx,
                n_gpu_layers=0,
                verbose=False
            )

            self.__is_loaded = True
            return True
        except Exception as e:
            self.__is_loaded = False
            raise ValueError(f"Erreur lors du chargement : {e}")

    def send_request(self, sentence: str, consigne_langue: bool = True, as_json: bool = True):
        return self.__predict_gguf_model(sentence, 512, consigne_langue, as_json)
