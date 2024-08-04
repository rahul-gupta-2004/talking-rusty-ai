import pygame
import random
from pygame import mixer
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

# Initialize Pygame and Mixer
pygame.init()
mixer.init()

# Setup screen dimensions and display
screen_width, screen_height = 500, 750
screen = pygame.display.set_mode((screen_width, screen_height))

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Load and cache robot animations
talk_images = [pygame.image.load(f"TalkFile/Talk{i}.png").convert_alpha() for i in range(9)]
wave_images = [pygame.image.load(f"WaveFile/Wave{i}.png").convert_alpha() for i in range(1, 26)]
normal_image = pygame.image.load("TalkFile/Talk0.png").convert_alpha()

# Center position for the robot
robot_center = (screen_width // 2, screen_height // 2)

# Load a random background image
def load_background():
    random_bg = random.randint(1, 26)
    bg_url = f"backgrounds/{random_bg}.png"
    img = pygame.image.load(bg_url).convert()
    return img

# Load and play background music based on the selected background image
def play_background_music(random_bg):
    audio = ["audio/class.wav", "audio/city.wav", "audio/future.wav", "audio/forest.wav", "audio/desert.wav",
             "audio/cave.wav", "audio/jail.wav", "audio/snow.wav", "audio/ocean.wav", "audio/gen.wav"]

    if random_bg in [1, 2]:
        mixer.music.load(audio[0])
    elif random_bg in [3, 4]:
        mixer.music.load(audio[1])
    elif random_bg in [5, 6]:
        mixer.music.load(audio[2])
    elif random_bg in range(7, 10):
        mixer.music.load(audio[3])
    elif random_bg in [10, 11]:
        mixer.music.load(audio[4])
    elif random_bg in [12, 13]:
        mixer.music.load(audio[5])
    elif random_bg in range(14, 17):
        mixer.music.load(audio[6])
    elif random_bg in [17, 18]:
        mixer.music.load(audio[7])
    elif random_bg in range(19, 23):
        mixer.music.load(audio[8])
    elif random_bg in range(23, 27):
        mixer.music.load(audio[9])

    mixer.music.set_volume(0.025)
    mixer.music.play(-1)

# Recognize speech using the microphone
def recognize_speech():
    with sr.Microphone() as source:
        print("Speak something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"User said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, the service is down.")
            return None

# Respond with speech and synchronize animation
def respond_with_speech(response_text):
    print(f"Speaking: {response_text}")

    tts_engine.say(response_text)
    tts_engine.runAndWait()

# Callback functions for TTS events
def on_start(name):
    print(f'Starting {name}')

def on_word(name, location, length):
    animate_talk()

def on_end(name, completed):
    print(f'Finished {name}')
    reset_robot()  # Reset to normal state after speaking

# Connect TTS events to callback functions
tts_engine.connect('started-utterance', on_start)
tts_engine.connect('started-word', on_word)
tts_engine.connect('finished-utterance', on_end)

# Placeholder for Gemini API call
def get_gemini_response(input_text):
    genai.configure(api_key="YOUR_GEMINI_API_KEY")
    generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
    model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)
    response = model.generate_content([input_text + " Give answer in plain text without any bold or text styling effect."])

    response_text = ""
    for chunk in response:
        response_text += chunk.text
        
    print(response_text)

    return response_text

# Function to animate robot talking
def animate_talk():
    clock = pygame.time.Clock()
    for img in talk_images:
        screen.blit(background_image, (0, 0))  # Reload background to keep original
        img_rect = img.get_rect(center=robot_center)
        screen.blit(img, img_rect.topleft)
        pygame.display.update()
        clock.tick(10)  # Set to 10 frames per second
    
    reset_robot()

# Function to animate robot waving
def animate_wave():
    clock = pygame.time.Clock()
    for img in wave_images:
        screen.blit(background_image, (0, 0))  # Reload background to keep original
        img_rect = img.get_rect(center=robot_center)
        screen.blit(img, img_rect.topleft)
        pygame.display.update()
        clock.tick(10)  # Set to 10 frames per second

    reset_robot()

# Function to reset robot to its normal state
def reset_robot():
    screen.blit(background_image, (0, 0))  # Keep original background
    screen.blit(normal_image, normal_image.get_rect(center=robot_center).topleft)
    pygame.display.update()

# Main loop
background_image = load_background()
play_background_music(random.randint(1, 26))
reset_robot()  # Show robot in its normal state at the start
running = True

# Common greetings to trigger waving animation
greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get user speech and respond
    user_input = recognize_speech()
    if user_input:
        if any(greeting in user_input.lower() for greeting in greetings):
            response_text = "Hello! How can I assist you today?"
            respond_with_speech(response_text)
            animate_wave()
        else:
            if "your name" in user_input.lower() or "who are you" in user_input.lower():
                response_text = "My name is Rusty, and I'm here to assist you with whatever you need."
            else:
                response_text = get_gemini_response(user_input)

            respond_with_speech(response_text)
            animate_talk()

# Quit Pygame
pygame.quit()
