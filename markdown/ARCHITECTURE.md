# ArreraNeuronNetwork Project Architecture

This document describes the file and folder organization of the ArreraNeuronNetwork project.

## Directories

### asset/
Contains static resources (images, sounds).
- `calendar/`: Images for the calendar.
- `horloge/`: Images and sounds (bip.mp3) for the clock, stopwatch, and timer.
- `meteo/`: Icons for weather conditions.
- `tache/`: Icons for task management.
- `theme/`: Contains the Arrera Tk V2 theme file
- `work/`: Icons for the workspace (projects, spreadsheet, word processing).

### brain/
- `brain.py`: Likely contains the central logic or "brain" of the assistant.

### config/
Configuration files.
- `confNeuron.py`: Neuron configuration.
- `listFete.json`: Database of holidays/celebrations.
- `tiger_demon.py`: Module that manages whether the personal assistant needs an update (Only works for Arrera applications)

### fnc/ (Functions)
Modules implementing the various functionalities of the assistant.
- `fncBase.py`: Base class for functions.
- `fonctionActu.py`: News management.
- `fonctionArreraDownload.py`: Download management.
- `fonctionArreraWork.py`: Work-related functionalities (office tools).
- `fonctionBreef.py`: Summaries or briefs.
- `fonctionCalculatrice.py`: Calculator logic.
- `fonctionCalendar.py`: Calendar management.
- `fonctionCodeHelp.py`: Coding/development helper.
- `fonctionGPS.py`: Location and GPS.
- `fonctionHorloge.py`: Time management, alarms, timer.
- `fonctionLecture.py`: Text-to-speech or text reading.
- `fonctionMeteo.py`: Weather forecasts.
- `fonctionOPEN.py`: Opening files or programs.
- `fonctionOrthographe.py`: Spelling correction.
- `fonctionRadio.py`: Radio player.
- `fonctionRecherche.py`: Internet search.
- `fonctionTache.py`: Task manager (To-Do).
- `fonctionTraduction.py`: Text translation.

### gestionnaire/ (Managers)
Management modules and coordinators.
- `gestion.py`: Global manager.
- `gestFNC.py`: Function manager.
- `HeadlessGuiManager.py`: GUI manager.
- `gestHistorique.py`: Interaction history management.
- `gestIA.py`: Artificial Intelligence management.
- `gestKeyword.py`: Keyword management for recognition.
- `gestLangue.py`: Language management.
- `gestNeuron.py`: Neural network management.
- `gestSocket.py`: Network/socket connection management.
- `gestSTR.py`: String processing utilities.
- `gestUserSetting.py`: User settings management.

### gui/ (Graphical User Interface)
Code related to the user interface (windows, widgets).
- `guibase.py`: Base class for windows.
- `GUIAgenda.py`: Window interface for the agenda/calendar, showing events and dates.
- `GUIArreraDownload.py`: Window interface for the Arrera video/audio download tool (YouTube downloader).
- `GUIArreraWork.py`: Main window interface for the Arrera Work environment (project management, spreadsheet, word).
- `GUIBaseTache.py`: Base GUI components/templates for task management features.
- `GUICalculatrice.py`: Window interface for the calculator (standard, complex, and Pythagoras modes).
- `GUIHelp.py`: Window interface displaying help and documentation about the assistant.
- `GUIHorloge.py`: Window interface for the clock, stopwatch, and timer functionalities.
- `GUILecture.py`: Window interface for the text-to-speech reading feature.
- `GUIorthographe.py`: Window interface for the spelling correction tool.
- `GUITache.py`: Window interface for displaying and managing the main To-Do list.
- `GUITaskProject.py`: Window interface for managing tasks specific to an Arrera Work project.
- `GUITraducteur.py`: Window interface for the translation tool.
- `GUIView.py`: General purpose view window for displaying generic results or web searches.
- `GUIViewBreef.py`: Window interface for displaying the daily brief (news, weather, tasks).
- `GUIViewResumer.py`: Window interface for displaying concise summaries.
- `codehelp/CCHguiBase.py`: Base GUI class for CodeHelp module windows.
- `codehelp/CCHcolorSelector.py`: Window interface for the developer color selector tool.
- `codehelp/CHGithub.py`: Window interface for the GitHub project management tool.
- `codehelp/CHLibrairy.py`: Window interface for the project library browser.
- `codehelp/CHOrgraVarriable.py`: Window interface for the variable organizer tool.

### instruction_ia/
Contains AI prompts and instructions files.
- `help_agenda_taches.txt`: Instructions for managing agenda and tasks.
- `help_arrera_work.txt`: Instructions regarding the usage of Arrera Work.
- `help_dev_recherche.txt`: Instructions detailing development and internet search features.
- `help_gps.txt`: Instructions concerning GPS functionalities and directions.
- `help_infos_meteo.txt`: Instructions for fetching and interpreting weather information.
- `help_medias_apps.txt`: Instructions for media control and opening applications.
- `prompt_main.txt`: The primary or base prompt initializing the assistant's AI personality and behavior.
- `prompt_orthographe.txt`: Instructions specifically dedicated to the spelling correction functionality.

### keyword/
JSON files defining trigger keywords.
- `api.json`, `codehelp.json`, `interface.json`, `open.json`, `search.json`, `service.json`, `time.json`, `utils.json`, `work.json`.

### language/
Linguistic configuration files (responses, standard phrases).
Divided into two modes:
- `tutoiment/`: Configuration for informal address ("tu").
- `vouvoiment/`: Configuration for formal address ("vous").
Each folder contains JSON files like `chatbot.json`, `formule.json`, `interface.json`, `markdown.json`, etc.

### librairy/
Utility libraries and support modules.
- `ArreraIALoad.py`: AI model loading.
- `arrera_date.py`: Date utilities.
- `arrera_tk.py`: Extensions or utilities for Tkinter.
- `arrera_voice.py`: Voice management (TTS/STT).
- `dectectionOS.py`: Host OS detection.
- `model_downloader.py`: External model downloader.
- `network.py`: Network utilities.
- `openSoftware.py`: Launching external software.
- `parreraclient.py`: Client for Arrera services (including WebSocket client).
- `PArreraServer.py`: WebSocket server for Arrera network communication.
- `resource_lib.py`: Resources location manager (especially for macOS).
- `travailJSON.py`: JSON read/write utilities.

### neuron/
"Neural" logic for request processing.
- `CNeuronBase.py`: Base class.
- `API.py`, `chatBots.py`, `codehelp.py`, `interface.py`, `markdown.py`, `open.py`, `search.py`, `service.py`, `time.py`, `work.py`: Domain-specific processing modules. (Note: `markdown.py` added to manage markdown processing and Arrera Markdown).

### objet/
Business objects and class definitions.
- `CArreraDownload.py`: Download object.
- `CHsearchDoc.py`: Documentation search.
- `arreradocument.py`: Document management.
- `arreratableur.py`: Spreadsheet management.