from flask import Flask, render_template,request
import os
import speech_recognition as sr 
import moviepy.editor as mp

app = Flask(__name__)
folder_to_save = os.path.join(app.instance_path, "uploads")
os.makedirs(folder_to_save, exist_ok=True)

@app.route('/', methods = ["GET", "POST"])
def hello_world():
    if request.method == "POST":
        file = request.files["img"]
        file.save(os.path.join(folder_to_save, file.filename))
        def_value = 10
        number = request.form.get("seconds", def_value)
        clip = mp.VideoFileClip(os.path.join(folder_to_save, file.filename)) 
        clip.audio.write_audiofile(os.path.join(folder_to_save, "toBeConvt.wav"))
        clip.close()
        r = sr.Recognizer()
        audio = sr.AudioFile(os.path.join(folder_to_save, "toBeConvt.wav"))
        with audio as source:
            audio_file = r.record(source, duration = int(number))
        result = r.recognize_google(audio_file)
        os.remove(os.path.join(folder_to_save, "toBeConvt.wav"))
        os.remove(os.path.join(folder_to_save, file.filename))
        return render_template("index.html", result = result)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run()