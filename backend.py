import streamlit as st
import os
import genai
from google.cloud import speech

# Load credentials from st.secrets
google_creds = st.secrets["gcp_creds"]  # Google Cloud credentials
gemini_key = st.secrets["gemini_api_key"]  # Gemini API key

# Display the loaded Gemini API key for confirmation
st.write("Google Credentials Loaded")
st.warning(gemini_key)

# Set the environment variable for Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/google_credentials.json"

# Write Google credentials to a temporary file for the Google SDK to read
with open("/tmp/google_credentials.json", "w") as f:
    f.write(google_creds)

# Initialize Gemini API with the api_key
genai.configure(api_key=gemini_key)

# Function to transcribe audio with Google Cloud Speech-to-Text
def transcribe_audio(audio_bytes):
    # Initialize the Google Cloud Speech client
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    # Extract the transcription text
    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcript

# Function to ask Gemini (ensure you have a model ready)
def ask_gemini(prompt):
    # Initialize the Gemini model and generate a response
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text
