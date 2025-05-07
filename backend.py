from google.cloud import speech_v1p1beta1 as speech
import google.generativeai as genai
import io
import os
import streamlit as st
import json
import tempfile
# ***********for local machine*************



# Set up Gemini API key
# genai.configure(api_key=os.getenv("AIzaSyApF4U0FhxjwRi5ewDm5pvGcaA-SDC38oU"))
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "audi-api-459011-afed87082894.json"




# # **************for streamlit******************

# Step 1: Fetch the credentials from Streamlit's secrets
gcp_credentials = st.secrets["GOOGLE_APPLICATION_CREDENTIALS_JSON"]

# Step 2: Parse the credentials JSON into a Python dictionary
credentials_dict = json.loads(gcp_credentials)

# Step 3: Create a temporary file to store the JSON content
with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".json") as temp_file:
    # Step 4: Write the credentials JSON data into the temporary file
    json.dump(credentials_dict, temp_file)
    temp_file_path = temp_file.name  # Store the path of the temporary file

# Step 5: Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of the temporary file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path

# Your code can now use the Google Cloud SDK, and it will authenticate using the temporary credentials file

print(f"Temporary credentials file created at: {temp_file_path}")









# Set up Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


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
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    response = model.generate_content(prompt)
    return response.text