# Talking Rusty Game

## Features

- Speech recognition using the `speech_recognition` library.
- Text-to-speech using the `pyttsx3` library.
- Background music that changes based on the randomly selected background image.
- Animated robot that talks and waves.
- Integration with Google Gemini API for generating responses.

## Requirements

- Python 3.x
- Pygame
- Pyttsx3
- SpeechRecognition
- Pygame Mixer
- Google Generative AI

## Installation

1. Clone the repository or download the code.
2. Install the required Python libraries:

   ```

   pip install pygame pyttsx3 SpeechRecognition google-generativeai

   ```
3. Ensure you have the required folders and files in your project directory:

   - `TalkFile/` containing `Talk0.png` to `Talk8.png`.
   - `WaveFile/` containing `Wave1.png` to `Wave25.png`.
   - `backgrounds/` containing `1.png` to `26.png`.
   - `audio/` containing the `.wav` files (class.wav, city.wav, future.wav, etc.).

## Configuration

- You will need an API key for the Google Gemini API. Replace the placeholder API key in the `get_gemini_response` function with your own API key.

## Usage

Run the script:

```

python talking_rusty.py

```
#   t a l k i n g - r u s t y - a i  
 