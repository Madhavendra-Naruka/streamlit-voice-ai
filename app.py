import streamlit as st
from streamlit_mic_recorder import mic_recorder
from backend import *

# Main Streamlit logic
audio = mic_recorder(start_prompt="🎤 Record", stop_prompt="⏹ Stop", just_once=True, format="webm")
if audio:
    audio_bytes = audio["bytes"]
    st.audio(audio_bytes)
    
    if len(audio_bytes) < 1000:  # adjust threshold if needed
        st.warning("Audio too short to process. Please try again.")
    else:
        try:
            # Speech-to-Text
            st.write("Transcribing...")  # Inform the user that transcription is in progress
            transcript = transcribe_audio(audio_bytes)  # Transcribe the audio
            st.info("You said: "+ transcript)  # Indicate successful transcription
            # st.warning(transcript)  # Display the transcribed text

            # Gemini Response
            st.write("Thinking with Gemini...")  # Inform the user that Gemini is processing
            reply = ask_gemini(transcript)  # Get the Gemini response based on the transcription
            st.success("Gemini says: "+ reply)  # Indicate Gemini's response
            # st.warning(reply)  # Display the Gemini response


        except Exception as e:
        st.error(f"Error: {e}")
