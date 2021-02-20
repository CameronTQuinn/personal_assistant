# Ye old import statements
import os
from os.path import join, dirname
from dotenv import load_dotenv
import wolframalpha
import wikipedia
import pyttsx3
import PySimpleGUI as sg
import speech_recognition as sr

# Initialize engine for speech recognition.
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Initialize engine for speech-to-text.
engine = pyttsx3.init()

# Get API key for Wolframalpha from .env file and set up client.
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
API_KEY = os.getenv("TOKEN")
client = wolframalpha.Client(API_KEY)

# Create window:
sg.theme('DarkBlue')   # Add a touch of color.
# All the stuff inside the window.
layout = [[sg.Text('Enter your query'), sg.InputText()], [sg.Button('Ok'), sg.Button("Speak"), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('JARVIS', layout)


# Function for processing input
def process_input(input):
    try:  # Try to get wolfram and wikipedia results.
        wolfram_res = next(client.query(input).results).text
        wiki_res = wikipedia.summary(input, sentences=2)
        engine.say("Wolframalpha results: " + wolfram_res)
        engine.say("Wikipedia results: " + wiki_res)
        sg.PopupNonBlocking("Wolframalpha results: " + wolfram_res, "Wikipedia results: " + wiki_res)

    except (wikipedia.exceptions.DisambiguationError,
            wikipedia.exceptions.PageError):  # Wikipedia results must be giving an error, simply display wolfram results.
        wolfram_res = next(client.query(input).results).text
        engine.say("Wolframalpha results: " + wolfram_res)
        sg.PopupNonBlocking("Wolframalpha results: " + wolfram_res)

    except:  # Neither wolfram or wikipedia has results.
        errorMsg = "Hmmmmm, your query has no results."
        engine.say(errorMsg)
        sg.PopupNonBlocking(errorMsg)

    engine.runAndWait()


# Event Loop to process "events" and get the "values" of the inputs.
while True:
    event, values = window.read()

    if event in (None, 'Cancel'):  # If user closes window or clicks cancel.
        break

    elif event in 'Speak':
        with mic as source:
            audio = recognizer.listen(source)

        output = recognizer.recognize_google(audio)

        process_input(output)

    else:
        process_input(values[0])

window.close()
