# ArreraNeuronNetwork (`ann-core` v4.0) Project Architecture

This document describes the file and folder organization of the **ArreraNeuronNetwork (`ann-core`)** project in Version 4.0 (100% Headless core engine, decoupled from GUI frontends via `IGestGui`).

## Directories

### `brain/`
- `brain.py`: Central controller (`ABrain`) orchestrating boot, shutdown, background notifications, socket messages, and request routing between `core_neuron` and `IARouter`.

### `config/`
Configuration and update modules:
- `confNeuron.py`: Assistant configuration dataclass (`confNeuron`), including feature flags and `ia_os_directory` (`/arrera/ia_model` shared Linux mode).
- `listFete.json`: Database of holidays and name days.
- `tiger_demon.py`: Update checker module for Arrera applications and assistants.

### `fnc/` (Functions)
Business logic modules implementing the assistant's capabilities (zero GUI dependencies):
- `fncBase.py`: Base class for all function modules.
- `fncMail.py`: Email reading, AI-assisted drafting, correction, and reply logic.
- `fonctionActu.py`: RSS/news feed fetching and summaries.
- `fonctionArreraDownload.py`: Video/audio download logic (`yt-dlp`).
- `fonctionArreraWork.py`: Project management, Word/Excel manipulation, and AI Code Agent file generation.
- `fonctionBrief.py`: Morning/daily brief aggregation (weather, news, tasks).
- `fonctionCalculatrice.py`: Mathematical calculation engine.
- `fonctionCalendar.py`: Agenda and calendar event management.
- `fonctionCodeHelp.py`: Developer tools and Git operations (`status`, `commit`, `push`, `branch`, `log`).
- `fonctionGPS.py`: Geolocation and Google Maps route generation.
- `fonctionHorloge.py`: Timer, stopwatch, and alarm management.
- `fonctionLecture.py`: Text reading preparation.
- `fonctionMeteo.py`: Weather and temperature forecasts (`meteofrance-api`).
- `fonctionOPEN.py`: Launching user software, system apps, and websites.
- `fonctionOrthographe.py`: AI-assisted spelling correction.
- `fonctionRadio.py`: Internet radio streaming (`pyradios` + `python-vlc`).
- `fonctionRecherche.py`: Web search engine queries.
- `fonctionTache.py`: Global and project To-Do task management.
- `fonctionTraduction.py`: Text translation.

### `gestionnaire/` (Managers)
Coordinators and state managers:
- `gestion.py`: Central service locator (`gestionnaire`) instantiating all managers.
- `IGestGui.py`: Abstract interface (`IGestGui`) defining the contract between `ann-core` and external GUI frontends (such as `ann-tkinter`).
- `HeadlessGuiManager.py`: Default no-op/CLI implementation of `IGestGui` for headless execution.
- `gestFNC.py`: Function registry and dispatcher.
- `gestHistorique.py`: Interaction history manager.
- `gestIA.py`: Local GGUF AI manager (worker thread, lazy loading, auto-unload RAM after idle, 0ms Python pre-classifier, Passe 0 / Passe 1 / Passe 2 orchestration, and model catalog/hardware recommendation delegation).
- `gestKeyword.py`: Keyword loader for socket/interface commands.
- `gestLangue.py`: Language and personality phrase manager.
- `gestMemoire.py`: Long-term user memory manager (with AI deduplication).
- `gestNeuron.py`: Instantiates `core_neuron`, `IARouter`, `interface`, and `neuroneMarkdown`.
- `gestSession.py`: Short-term conversation context manager.
- `gestSocket.py`: WebSocket client/server manager.
- `gestSTR.py`: String cleaning and normalization utilities.
- `gestUserSetting.py`: User configuration manager (`user.json`, software/site lists, AI model selection, hardware recommendation, and custom GGUF download).

### `instruction_ia/`
System prompts used by specialized AI tasks in `gestIA.py`:
- `prompt_dedoublonnage.txt`: Deduplication prompt for long-term user memory.
- `prompt_mail_correction.txt`: Prompt for correcting email drafts.
- `prompt_mail_creation.txt`: Prompt for writing new emails.
- `prompt_mail_reponse.txt`: Prompt for generating email replies.
- `prompt_orthographe.txt`: Prompt for spelling and grammar correction.

### `keyword/`
- `interface.json`: Trigger keywords for external Arrera socket/interface commands.

### `language/`
Linguistic configuration files divided into two address modes:
- `tutoiment/`: Informal French ("tu") — `formule.json`, `personnalite.json`.
- `vouvoiment/`: Formal French ("vous") — `formule.json`, `personnalite.json`.

### `librairy/`
Low-level libraries and OS utilities:
- `ArreraIALoad.py`: `llama-cpp-python` wrapper with GGUF loading, lazy state tracking, and multi-OS native RAM reclamation (`malloc_trim`, `SetProcessWorkingSetSize`, `libSystem.dylib`).
- `audio_data.py`: In-memory system sound generation (base64 audio streams for microphone and timer bip cues, eliminating static audio file dependencies).
- `arrera_date.py`: Date and time helper utilities.
- `arrera_voice.py`: Offline TTS (`piper-tts`) and STT (`speechRecognition` + `sounddevice`) engine.
- `dectectionOS.py`: Multi-OS detection (Linux, Windows, macOS).
- `model_downloader.py`: Official 9-model GGUF catalog (Gemma 4, Mistral, Qwen 2.5), multi-OS hardware detection & model recommendation, custom direct-link `.gguf` downloader (with Magic Bytes & disk space validation), and `/arrera/ia_model` shared Linux directory support.
- `network.py`: Internet connectivity checker.
- `openSoftware.py`: Cross-platform application launcher.
- `parreraclient.py` & `PArreraServer.py`: WebSocket client and server for Arrera inter-process communication.
- `resource_lib.py`: Resource path resolver.
- `travailJSON.py`: JSON file wrapper.

### `neuron/`
Request routing and processing layer:
- `CNeuronBase.py`: Base class for neurons.
- `core_neuron.py`: Fast-track deterministic execution for immediate commands (time, weather, temperature, news, radio, timer, GUI triggers).
- `IARouter.py`: Tool-calling JSON router mapping natural language requests to the 21 assistant tool categories (`action_type` / `parameters`).
- `interface.py`: Socket command handler for Arrera interface modes.
- `markdown.py`: Socket handler for the external Arrera Markdown editor.

### `objet/`
Domain objects manipulated by `fnc/` modules:
- `arreradocument.py`: Word/ODT document wrapper.
- `arreratableur.py`: Excel spreadsheet wrapper.
- `CArreraDownload.py`: Media downloader object (`yt-dlp`).
- `CHGit.py`: Git repository wrapper (`GitPython` / CLI).
- `CHsearchDoc.py`: Developer documentation search helper.

### `src/` & `test_file/`
- `src/opale.py`: CLI entry point for the Opale assistant.
- `test_file/`: Interactive and automated test suites (`test-hallucination.py`, `test-user-setting.py`, `test-fnc.py`, `test-voice.py`, `test_connection_server.py`, `test_tiger_demon.py`).