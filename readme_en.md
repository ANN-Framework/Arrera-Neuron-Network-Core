# ℹ️ About Arrera Neuron Network

![Arrera Neuron Network Banner](https://raw.githubusercontent.com/Arrera-Software/ArreraNeuronNetwork/refs/heads/Version-3/asset/baniere.png)

This project aims to create a foundation for developing personal assistants using **Python 3.14 exclusively** (Modular Headless `ann-core` architecture decoupled from the GUI frontend).

## Features

The Arrera Neuron Network assistant (Version 4.0) is powered by a hybrid local GGUF AI engine (`core_neuron` + `IARouter`) to handle natural language requests:

*   **Local AI Engine (GGUF)**: Smart intent routing (`IARouter`), fast pre-filtering (`core_neuron`), on-demand *Lazy Loading*, and automatic RAM unloading when idle.
*   **AI Model Management**: Built-in catalog (Gemma 4, Mistral, Qwen 2.5), automatic hardware-based model recommendation (RAM, GPU VRAM, CPU), custom model downloading via direct `.gguf` links, and shared Linux OS model directory support (`/arrera/ia_model`).
*   **Memory & Session**: Persistent user memory (`gestMemoire`) and conversation context tracking (`gestSession`).
*   **Weather & Temperature**: Provides current weather, temperature, and forecasts (home, work, or current location).
*   **Brief**: Provides a summary of news, weather, and tasks (morning brief or on-demand summary).
*   **GPS**: Gives current geographical coordinates and can launch a Google Maps route (start and end points).
*   **News**: Delivers the latest news (general, tech, etc.).
*   **Translation**: Text translation and translation tool integration.
*   **Software & Website Opening**: Opens user-configured software, system applications, or saved websites (YouTube, YouTube Music, etc.).
*   **Radio**: Plays radio stations (Europe 1, France Info, NRJ, Skyrock, etc.) or stops the radio.
*   **Arrera Tools**: Opens internal tools like the video downloader (`Arrera Download`) or calculator modes (complex, Pythagoras).
*   **Time, Date & Time Tools**: Gives the current time/date and manages the stopwatch, clock, or timer.
*   **Agenda & Tasks**: Full calendar and to-do list management (add, remove, mark as done, check task count).
*   **Internet Search**: Performs standard or in-depth searches on the configured search engine.
*   **Calculations, Reading & Spelling**: Mathematical calculations, offline text-to-speech (`piper-tts`), and AI-assisted spelling correction.
*   **Emails**: AI-assisted email drafting, correction, and replies (`fncMail`).
*   **Arrera Work (Projects, Spreadsheet & Word Processing)**: Project creation and management, Word/Excel file editing (sum, average, min, max), and **AI Code Agent mode** for file generation.
*   **Development Tools & Git (`CodeHelp`)**: Documentation search (DevDocs, Microsoft, Python, GitHub), variable organizer, color selector, and Git integration (`status`, `commit`, `push`, `branch`, `log`).
*   **Display Modes & Network**: Activates display modes (mode 1 to 6) and integrates a WebSocket client/server to interact with external services and "Arrera Markdown".
*   **Shutdown**: Manages the shutdown of the assistant or modes.

# Architecture

[View project architecture](./markdown/ARCHITECTURE.md)

# Project Dependencies

[View project dependencies](./markdown/dependency.md)