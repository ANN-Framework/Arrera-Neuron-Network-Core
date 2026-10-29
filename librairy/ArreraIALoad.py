import ctypes
import gc
import os
from llama_cpp import Llama
from librairy.dectectionOS import OS


class ArreraIALoad:
    DEFAULT_CTX = 3072
    LARGE_CTX = 8192

    def __init__(self):
        self.__model_type = None
        self.__model = None
        self.__tokeniser = None
        self.__classes = None
        self.__is_loaded = False
        self.__system_context_is_loaded = False
        self.__system_instructions = []
        self.__os = OS()
        self.__model_path = None
        self.__current_n_ctx = self.DEFAULT_CTX

    # Methode private
    def __release_os_memory(self):
        """Force l'OS (Linux, Windows, macOS) à récupérer immédiatement la RAM libérée par C++/GGUF."""
        try:
            if self.__os.osLinux():
                ctypes.CDLL("libc.so.6").malloc_trim(0)
            elif self.__os.osWindows():
                ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
            elif self.__os.osMac():
                ctypes.CDLL("libSystem.B.dylib").malloc_zone_pressure_relief(None, 0)
        except Exception:
            pass

    def ensure_ctx(self, target_ctx: int = DEFAULT_CTX) -> bool:
        """
        Vérifie si le modèle est chargé avec la taille de contexte demandée.
        Si ce n'est pas le cas, recharge le modèle avec target_ctx en conservant les instructions système.
        """
        if self.__model is not None and self.__current_n_ctx == target_ctx:
            return True

        if self.__model_path and os.path.exists(self.__model_path):
            return self.load_model_gguf(self.__model_path, n_ctx=target_ctx)
        return False

    def get_current_ctx(self) -> int:
        return self.__current_n_ctx

    def __predict_gguf_model(
        self,
        prompt: str,
        max_tokens: int = 512,
        enable_consigne_langue: bool = True,
        as_json: bool = True,
        use_system_context: bool = True,
        min_ctx: int = DEFAULT_CTX,
    ):
        # 1. Vérifie ou bascule sur le contexte minimal demandé
        if self.__current_n_ctx < min_ctx:
            self.ensure_ctx(min_ctx)

        if enable_consigne_langue:
            consigne_langue = "\n\n(Réponds impérativement en français, même si je parle anglais ou technique)."
        else:
            consigne_langue = ""

        user_content = prompt + consigne_langue
        messages = []
        fallback_messages = []

        if use_system_context and self.__system_context_is_loaded and len(self.__system_instructions) > 0:
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
        except ValueError as e:
            # Sécurité automatique : Dépassement de contexte détecté -> bascule dynamique vers LARGE_CTX
            err_msg = str(e).lower()
            if "exceed context window" in err_msg and self.__current_n_ctx < self.LARGE_CTX:
                print(f"[ArreraIALoad] Contexte dépassé ({self.__current_n_ctx}). Bascule automatique vers {self.LARGE_CTX} tokens...")
                self.ensure_ctx(self.LARGE_CTX)
                output = self.__model.create_chat_completion(**kwargs)
            else:
                # Tentative avec fallback_messages
                try:
                    kwargs["messages"] = fallback_messages
                    output = self.__model.create_chat_completion(**kwargs)
                except ValueError as e_fallback:
                    if "exceed context window" in str(e_fallback).lower() and self.__current_n_ctx < self.LARGE_CTX:
                        print(f"[ArreraIALoad] Contexte dépassé sur fallback. Bascule automatique vers {self.LARGE_CTX} tokens...")
                        self.ensure_ctx(self.LARGE_CTX)
                        output = self.__model.create_chat_completion(**kwargs)
                    else:
                        raise e_fallback
        except Exception:
            kwargs["messages"] = fallback_messages
            output = self.__model.create_chat_completion(**kwargs)

        return output['choices'][0]['message']['content']

    # Methode public
    def is_model_loaded(self) -> bool:
        return self.__is_loaded and self.__model is not None

    def add_system_instruction(self, instruction: str):
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

    def unload_model(self, keep_instructions: bool = False):
        """Désinstancie proprement le modèle Llama chargé en mémoire et rend la RAM à l'OS."""
        if self.__model is not None:
            try:
                if hasattr(self.__model, 'close'):
                    self.__model.close()
            except Exception:
                pass
            del self.__model
            self.__model = None
            gc.collect()
            self.__release_os_memory()
        self.__is_loaded = False
        if not keep_instructions:
            self.__system_context_is_loaded = False
            self.__system_instructions = []
            self.__model_path = None
            self.__current_n_ctx = self.DEFAULT_CTX

    def load_model_gguf(self, model_path: str, n_ctx: int = DEFAULT_CTX):
        if not os.path.exists(model_path):
            raise ValueError(f"Le fichier modèle n'existe pas : {model_path}")

        # Conserve le chemin du modèle actif
        self.__model_path = model_path
        self.__current_n_ctx = n_ctx

        # Si un modèle est déjà chargé, le désinstancier d'abord en conservant les instructions
        if self.__is_loaded or self.__model is not None:
            self.unload_model(keep_instructions=True)

        cpu_count = os.cpu_count() or 4
        # Garde 1 à 2 threads libres pour ne pas bloquer l'interface ou l'OS sur les petits PC
        n_threads = max(1, cpu_count - 2) if cpu_count > 2 else max(1, cpu_count)

        try:
            self.__model = Llama(
                model_path=model_path,
                n_ctx=n_ctx,
                n_threads=n_threads,
                n_threads_batch=n_threads,
                n_batch=256,
                n_gpu_layers=0,
                use_mmap=True,
                use_mlock=False,
                verbose=False
            )

            self.__is_loaded = True
            return True
        except Exception as e:
            self.__is_loaded = False
            raise ValueError(f"Erreur lors du chargement : {e}")

    def send_request(
        self,
        sentence: str,
        consigne_langue: bool = True,
        as_json: bool = True,
        max_tokens: int = 512,
        use_system_context: bool = True,
        min_ctx: int = DEFAULT_CTX,
    ):
        return self.__predict_gguf_model(
            sentence, max_tokens, consigne_langue, as_json, use_system_context, min_ctx
        )