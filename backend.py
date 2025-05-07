from google.cloud import speech_v1p1beta1 as speech
import google.generativeai as genai
import io
import os
import streamlit as st
import google.generativeai as genai


# ***********for local machine*************

# # Set your credentials path
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "audi-api-459011-25c023846c00.json"

# # Set up Gemini API key
# genai.configure(api_key=os.getenv("AIzaSyApF4U0FhxjwRi5ewDm5pvGcaA-SDC38oU"))
# # models = list(genai.list_models())  # Convert the generator to a list
# # print(models)



# **************for streamlit******************

# Load credentials from st.secrets
google_creds = st.secrets["google"]["credentials"]
gemini_key = st.secrets["gemini"]["api_key"]

# Set environment variable for Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/google_credentials.json"

# Write credentials to a temporary file (for Google SDK to read)
with open("/tmp/google_credentials.json", "w") as f:
    f.write(google_creds)

# Use the gemini_key wherever required
genai.configure(api_key=gemini_key)


# Function to transcribe with Google Cloud Speech-to-Text
def transcribe_audio(audio_bytes):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcript

# Function to ask Gemini
def ask_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text