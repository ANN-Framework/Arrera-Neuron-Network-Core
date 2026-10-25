# System & Python Dependencies (`ann-core` v4.0)

`ArreraNeuronNetwork` (`ann-core`) requires **Python 3.14 exclusively** and is 100% Headless (zero GUI dependencies such as Tkinter or GTK).

Depending on your operating system, install the following system-level dependencies for audio (`sounddevice` / `piper-tts`), media playback (`python-vlc` / `yt-dlp`), clipboard (`pyperclip`), and OS notifications/services.

## Linux

### Debian / Ubuntu / Mint
```bash
sudo apt-get update
sudo apt-get install python3.14 python3.14-dev xclip xsel vlc libportaudio2 portaudio19-dev libsndfile1 ffmpeg git
```

### Fedora
```bash
sudo dnf install python3.14 python3.14-devel xclip xsel vlc portaudio portaudio-devel libsndfile ffmpeg git
```

### Arch Linux
```bash
sudo pacman -S python xclip xsel vlc portaudio libsndfile ffmpeg git
```

## macOS

Using [Homebrew](https://brew.sh/):

1. **Python 3.14**:
   ```bash
   brew install python@3.14
   ```
2. **VLC Media Player** (required for `python-vlc` radio/audio playback):
   ```bash
   brew install --cask vlc
   ```
3. **PortAudio & libsndfile** (required for `sounddevice` / `soundfile` / `piper-tts`):
   ```bash
   brew install portaudio libsndfile
   ```
4. **FFmpeg** (required for media and `yt-dlp` processing):
   ```bash
   brew install ffmpeg
   ```

## Windows

1. **Python 3.14 (64-bit)**: Install from [python.org](https://www.python.org/downloads/).
2. **VLC Media Player (64-bit)**: Download and install from [videolan.org](https://www.videolan.org/vlc/download-windows.html).
3. **FFmpeg**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your System `PATH`.
4. **C++ Build Tools**: Visual Studio Build Tools ("Desktop development with C++") may be required if prebuilt wheels for `llama-cpp-python` are not available for your architecture.

## Python Dependencies

Install `ann-core` in editable mode (or via `requirements.txt`):

```bash
pip install -e .
# or
pip install -r requirements.txt
```
