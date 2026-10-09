# ArreraNeuronNetwork Integration Guide

This document explains how to integrate and use the ArreraNeuronNetwork in a Python project, based on the implementation found in `../src/opale.py`.

## Overview

The integration revolves around the `ABrain` class (from `brain.brain`), which acts as the central controller for the assistant. The process involves configuring the neuron, initializing the brain, and then interacting with it via text inputs.

## Step-by-Step Integration

### 1. Configuration (`confNeuron`)

Before initializing the brain, you must create a configuration object using `confNeuron` (from `config.confNeuron`). This object defines the assistant's behavior, identity, and enabled capabilities.

```python
from config.confNeuron import confNeuron

# Example configuration
configuration = confNeuron(
    name="Opale",
    lang="fr",
    asset="asset/",
    icon="asset/icon.png",
    assistant_color="white",
    assistant_texte_color="black",
    bute="develop a ChatBot algo...",
    createur="Your Name",
    listFonction=["open app", "search internet", "weather", "news"],
    moteurderecherche="google",
    # Enable/Disable specific neurons (1 = On, 0 = Off)
    etatService=1,
    etatTime=1,
    etatOpen=1,
    etatSearch=1,
    etatChatbot=1,
    etatApi=1,
    etatCodehelp=1,
    etatWork=1,
    etatSocket=0,
    lienDoc="www.google.com",
    fichierLangue="language/vouvoiment/", # Path to language files
    fichierKeyword="keyword/",            # Path to keyword files
    voiceAssistant=True
)
```

### 2. Initialization (`ABrain`)

Once configured, instantiate the `ABrain` class.

```python
from brain.brain import ABrain

try:
    assistant_brain = ABrain(config=configuration)
    print("Brain initialized successfully.")
except Exception as e:
    print(f"Error initializing brain: {e}")
```

### 3. Booting the Assistant

Call the `boot()` method to start the assistant. This usually returns a welcome message.

```python
welcome_message = assistant_brain.boot()
print(f"Assistant says: {welcome_message}")
```

### 4. Interaction (The "Neuron" Loop)

To process user input, use the `neuron()` method. This is typically done in a separate thread to avoid freezing the UI during processing.

```python
import threading

def process_message(message):
    # This runs the logic to determine the response
    assistant_brain.neuron(message)

# Example usage
user_input = "What time is it?"
thread = threading.Thread(target=process_message, args=(user_input,))
thread.start()
```

### 5. Retrieving Results

After the `neuron()` method finishes processing, you can retrieve the results using:
*   `getValeurSortie()`: Returns an integer code representing the type of action performed (e.g., 15 for exit).
*   `getListSortie()`: Returns a list where the first element is usually the text response.

```python
# Wait for the thread to finish or check periodically
thread.join() 

response_code = assistant_brain.getValeurSortie()
response_text = assistant_brain.getListSortie()[0]

print(f"Code: {response_code}")
print(f"Response: {response_text}")
```

### 6. Background Updates

The assistant may need to perform background tasks (like checking alarms or timers). The `updateAssistant()` method should be called periodically.

```python
if assistant_brain.updateAssistant():
    # If true, a background event triggered a response
    new_code = assistant_brain.getValeurSortie()
    new_text = assistant_brain.getListSortie()[0]
    print(f"Update: {new_text}")
```

### 7. Shutdown

Properly close the assistant resources using `shutdown()`.

```python
assistant_brain.shutdown()
```

## Key Components Summary

*   **`config.confNeuron`**: Configuration data structure.
*   **`brain.brain.ABrain`**: Main controller class.
*   **`neuron(message)`**: Core method to process user text.
*   **`getValeurSortie()` / `getListSortie()`**: Methods to get the assistant's output.
*   **`updateAssistant()`**: Method for background event handling.
