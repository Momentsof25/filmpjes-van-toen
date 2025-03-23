from flask import Flask, render_template, request, send_file
from moviepy.editor import ImageSequenceClip, AudioFileClip
import os
import tempfile

app = Flask(__name__)
UPLOAD_FOLDER = tempfile.mkdtemp()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    images = request.files.getlist("images")
    audio = request.files.get("audio")

    if not images or not audio:
        return "Geen foto's of audio geüpload", 400

    # Opslaan van bestanden
    image_paths = []
    for image in images:
        img_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(img_path)
        image_paths.append(img_path)

    audio_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    audio.save(audio_path)

    # Maak video met MoviePy
    audio_clip = AudioFileClip(audio_path)
    clip = ImageSequenceClip(image_paths, durations=[1]*len(image_paths))  # 1 sec per foto
    clip = clip.set_audio(audio_clip.set_duration(clip.duration))

    video_path = os.path.join(UPLOAD_FOLDER, "result.mp4")
    clip.write_videofile(video_path, fps=24)

    return send_file(video_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
