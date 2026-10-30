# ℹ️ About Arrera Neuron Network (`ann-core`)

![Arrera Neuron Network Banner](https://raw.githubusercontent.com/Arrera-Software/ArreraNeuronNetwork/refs/heads/Version-3/asset/baniere.png)

Logic, neural routing, and voice engine for developing intelligent personal assistants using **Python 3.14 exclusively**.

Version 4.0: **100% Headless Architecture**, fully decoupled from any GUI framework and operable in standalone mode (CLI / Server) or connectable to any frontend through the `IGestGui` interface contract.

*For the official Tkinter / CustomTkinter graphical frontend, see the dedicated repository:*  
👉 **[`ann-tkinter`](https://github.com/ANN-Framework/Arrera-Neuron-Network-Tkinter)**

[Version française](./readme.md) | [Integration Guide](./markdown/INTEGRATION.md) | [Architecture](./markdown/ARCHITECTURE.md)

---

## 🚀 Two Execution Modes

1. **Headless Mode (Console / Server)**:
   The engine runs without any graphical interface (`HeadlessGuiManager`). Requests (weather, news, tasks, calendar, etc.) are processed and returned as text or speech output.
2. **Graphical Mode (External Frontend)**:
   A frontend (such as [`ann-tkinter`](https://github.com/ANN-Framework/Arrera-Neuron-Network-Tkinter)) injects its own display manager via `gest.set_gui_manager(my_gui)`. The AI brain dynamically activates visual tools and delegates specialized window rendering to the frontend.

---

## 🧠 Core Features

Arrera Neuron Network is driven by a hybrid engine combining deterministic 0ms neurons (`core_neuron`) and a local GGUF AI router (`IARouter`):

* **Local AI Engine (GGUF)**: Intent routing (`IARouter`), 0ms pre-filtering (`core_neuron`), on-demand *Lazy Loading*, and automatic RAM unloading after idle with multi-OS native memory reclamation.
* **AI Model Management**: Official catalog (Gemma 4, Mistral, Qwen 2.5), automatic hardware-based recommendation (RAM, GPU VRAM, CPU), direct `.gguf` downloads, and shared Linux directory support (`/arrera/ia_model`).
* **Memory & Session**: Persistent user memory with AI deduplication (`gestMemoire`) and conversational context tracking (`gestSession`).
* **Offline Voice Engine**: Ultra-fast offline text-to-speech (`piper-tts`) and speech recognition (`speechRecognition`), with in-memory synthesized audio signals (zero static audio files needed on disk).
* **Weather & Forecasts**: Real-time weather and temperature forecasts via `meteofrance-api`.
* **Daily Brief**: Morning, afternoon, and evening briefs aggregating news, weather, and scheduled tasks.
* **GPS & Routes**: Geolocation coordinates and Google Maps route generation.
* **News & RSS Feeds**: News aggregation across multiple categories (General, Science, Tech, etc.).
* **Translation**: Multi-language text translation engine.
* **App & Website Launcher**: Cross-platform launcher for system apps, custom software, and saved websites.
* **Internet Radio**: Live radio streaming (`pyradios` + `python-vlc`).
* **Arrera Tools**: Complex math / Pythagoras calculation and media downloading (`yt-dlp`).
* **Time Tools**: World clock, stopwatch, and timer with autonomous alerts.
* **Agenda & To-Do List**: Calendar event scheduling, daily tasks, global tasks, and project-specific tasks.
* **Web Search**: Standard or in-depth search engine queries.
* **AI-Assisted Emails**: Email reading, drafting, stylistic correction, and automated reply generation (`fncMail`).
* **Arrera Work (Projects, Office & AI Code Agent)**: Word documents (`.docx`, `.odt`), Excel spreadsheets (`.xlsx`), and **AI Code Agent** for code and project file generation.
* **Developer Tools & Git (`CodeHelp`)**: Developer documentation lookup (Python, DevDocs, Microsoft, GitHub), variable organizer, color selector, and native Git commands.
* **WebSocket Network**: Integrated WebSocket client and server for communicating with external services or Arrera Markdown.

---

## 📦 Installation & Dependencies

`ann-core` requires **Python 3.14 exclusively**.

```bash
# Clone repository
git clone https://github.com/ANN-Framework/Arrera-Neuron-Network-Core.git
cd Arrera-Neuron-Network-Core

# Install in editable mode
pip install -e .
```

For system audio/video dependencies (PortAudio, libsndfile, VLC, FFmpeg), please see:  
👉 **[System Dependencies](./markdown/dependency.md)**

---

## 🔌 Integration Guide

To connect `ann-core` to your own graphical interface or service:  
👉 **[Core Integration Guide (`markdown/INTEGRATION.md`)](./markdown/INTEGRATION.md)**

---

## 🏗️ Architecture

For complete directory and module breakdown:  
👉 **[Project Architecture](./markdown/ARCHITECTURE.md)**
