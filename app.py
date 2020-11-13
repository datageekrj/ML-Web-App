import speech_recognition as sr 
import moviepy.editor as mp
from flask import Flask, request, render_template
def extract_text(video_path, audio_path, duration = 20):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    recognizer = sr.Recognizer()
    audio = sr.AudioFile("audio.wav")
    with audio as source:
        audio_file = recognizer.record(source, duration=duration)

    result = recognizer.recognize_google(audio_file)
    return result

app = Flask(__name__)

import os 
folder_to_save = os.path.join(app.instance_path, "uploads")
os.makedirs(folder_to_save, exist_ok=True)


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["img"]
        file.save(os.path.join(folder_to_save, file.filename))
        # We define two paths
        audio_path = os.path.join(folder_to_save, "toBeCovt.wav")
        video_path = os.path.join(folder_to_save, file.filename)

        # Get the number of seconds
        def_value = 20
        number = request.form.get("seconds", def_value)
        number = int(number)

        # Use the path with extract_text function
        result = extract_text(video_path, audio_path, duration=number)
        return render_template("index.html", result = result)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
