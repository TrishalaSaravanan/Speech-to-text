import streamlit as st
import speech_recognition as sr
import spacy

# Initialize the speech recognition recognizer
recognizer = sr.Recognizer()

# Function to convert speech to text
def speech_to_text(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Record the audio file
        try:
            text = recognizer.recognize_google(audio_data)  # Use Google Web Speech API for speech recognition
            return text
        except sr.UnknownValueError:
            return "Sorry, could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Function for basic NLP processing
def nlp_processing(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    # Example of NLP processing - extracting named entities
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    return named_entities

# Main function
def main():
    st.title("Speech to Text and NLP Processing")

    # Upload audio file
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav"])

    if uploaded_file is not None:
        audio_file = uploaded_file.name
        st.audio(uploaded_file, format='audio/wav')

        # Convert speech to text
        text = speech_to_text(uploaded_file)
        st.subheader("Transcribed Text:")
        st.write(text)

        # Perform NLP processing
        named_entities = nlp_processing(text)
        st.subheader("Named Entities:")
        for entity, label in named_entities:
            st.write(f"{entity}: {label}")

if __name__ == "__main__":
    main()
