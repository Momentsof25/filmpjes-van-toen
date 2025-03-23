import streamlit as st
from moviepy.editor import ImageSequenceClip, AudioFileClip
import os
import tempfile

st.title("Filmpjes van Toen 🎬")

uploaded_images = st.file_uploader("Upload foto's", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
uploaded_audio = st.file_uploader("Upload muziek (MP3)", type=["mp3"])

if st.button("Maak video") and uploaded_images and uploaded_audio:
    with tempfile.TemporaryDirectory() as tmpdir:
        image_paths = []
        for image in uploaded_images:
            path = os.path.join(tmpdir, image.name)
            with open(path, "wb") as f:
                f.write(image.read())
            image_paths.append(path)

        audio_path = os.path.join(tmpdir, uploaded_audio.name)
        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.read())

        audio_clip = AudioFileClip(audio_path)
        clip = ImageSequenceClip(image_paths, durations=[1]*len(image_paths))
        clip = clip.set_audio(audio_clip.set_duration(clip.duration))

        video_path = os.path.join(tmpdir, "video.mp4")
        clip.write_videofile(video_path, fps=24)

        with open(video_path, "rb") as f:
            st.download_button("Download video", f, file_name="filmpje.mp4")
