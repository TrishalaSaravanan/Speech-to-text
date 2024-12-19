from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
import spacy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Initialize the speech recognition recognizer
recognizer = sr.Recognizer()

# Folder to save uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Function to convert speech to text
def speech_to_text(audio_file_path):
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)  # Record the audio file
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

# Route to upload and process the audio file
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if file is in the request
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Convert speech to text
            transcription = speech_to_text(filepath)

            # Perform NLP processing if transcription is successful
            if transcription and transcription != "Sorry, could not understand the audio.":
                named_entities = nlp_processing(transcription)
                return jsonify({
                    "transcription": transcription,
                    "named_entities": named_entities
                })

            return jsonify({
                "transcription": transcription,
                "named_entities": []
            })

    return render_template("index.html")

# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True)
