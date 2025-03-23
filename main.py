import os
from flask import Flask, render_template, request, send_file
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    audio = request.files.get('audio')
    images = request.files.getlist('images')

    if not audio or not images:
        return 'Audio en afbeeldingen zijn verplicht!', 400

    audio_path = os.path.join(UPLOAD_FOLDER, secure_filename(audio.filename))
    audio.save(audio_path)

    image_paths = []
    for image in images:
        image_path = os.path.join(UPLOAD_FOLDER, secure_filename(image.filename))
        image.save(image_path)
        image_paths.append(image_path)

    audio_clip = AudioFileClip(audio_path)
    duration_per_image = audio_clip.duration / len(image_paths)

    clips = []
    for path in image_paths:
        clip = ImageClip(path).set_duration(duration_per_image).fadein(0.5).fadeout(0.5).resize(height=720)
        clips.append(clip)

    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.set_audio(audio_clip)

    output_path = os.path.join(OUTPUT_FOLDER, 'herinnering.mp4')
    final_video.write_videofile(output_path, fps=24)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
