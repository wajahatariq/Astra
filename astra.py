import streamlit as st
import speech_recognition as sr
import webbrowser
import random
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO

# Configure Gemini API
genai.configure(api_key="AIzaSyBviI-5MF2edr6H8KLQ8mO6sPLy-DjTS64")
model = genai.GenerativeModel('gemini-1.5-flash')

Astra_active_speak = ["Astra is on your service", "Yeahh!", "Yes Sir", "I'm active", "Hello"]

# Speak using gTTS
def speak(text):
    tts = gTTS(text)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    st.audio(mp3_fp.getvalue(), format="audio/mp3")

# Command processor
def process_command(User_command):
    command = User_command.lower()
    if "open google" in command:
        webbrowser.open("https://www.google.com/")
        return "Opening Google..."
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com/")
        return "Opening YouTube..."
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com/")
        return "Opening Instagram..."
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com/")
        return "Opening Facebook..."
    elif "open free pic" in command:
        webbrowser.open("https://www.freepik.com/")
        return "Opening Freepik..."
    else:
        response = model.generate_content(User_command)
        return response.text

# Streamlit UI
st.set_page_config(page_title="Astra - Voice AI Assistant")
st.title("🤖 Astra - Your AI Voice Assistant")
st.write("Click below to speak your command:")

if st.button("🎙️ Start Listening"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now")
        try:
            audio = r.listen(source, timeout=5)
            User_command = r.recognize_google(audio)
            st.success(f"Recognized: {User_command}")

            response_text = process_command(User_command)
            st.write(f"🧠 Astra: {response_text}")
            speak(response_text)

        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand your voice.")
        except sr.WaitTimeoutError:
            st.error("Listening timed out.")
        except Exception as e:
            st.error(f"Error: {e}")
