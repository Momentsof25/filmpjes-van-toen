import streamlit as st
from moviepy.editor import ImageSequenceClip, AudioFileClip
import os
import tempfile

st.title("🎞️ Filmpjes van Toen")
st.write("Upload foto's en een muziekbestand. Wij maken een herinneringsvideo.")

uploaded_images = st.file_uploader("Upload foto's", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
uploaded_audio = st.file_uploader("Upload muziek (MP3)", type=["mp3"])

if st.button("Maak video") and uploaded_images and uploaded_audio:
    with tempfile.TemporaryDirectory() as tmpdir:
        image_paths = []
        for img_file in uploaded_images:
            img_path = os.path.join(tmpdir, img_file.name)
            with open(img_path, "wb") as f:
                f.write(img_file.read())
            image_paths.append(img_path)

        audio_path = os.path.join(tmpdir, uploaded_audio.name)
        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.read())

        audio_clip = AudioFileClip(audio_path)
        clip = ImageSequenceClip(image_paths, durations=[1]*len(image_paths))
        clip = clip.set_audio(audio_clip.set_duration(clip.duration))

        video_path = os.path.join(tmpdir, "result.mp4")
        clip.write_videofile(video_path, fps=24)

        with open(video_path, "rb") as f:
            st.download_button("Download jouw video", f, file_name="herinnering.mp4", mime="video/mp4")
