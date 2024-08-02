import yt_dlp
import subprocess
import os
import shutil


def download_audio_from_youtube(video_url, output_filename="audio"):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": output_filename,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


def remove_music(audio_filename="audio.mp3"):
    command = [
        "spleeter",
        "separate",
        "-p",
        "spleeter:2stems",
        "-o",
        ".",
        audio_filename,
    ]
    subprocess.run(command, check=True)
    if os.path.exists(audio_filename):
        os.remove(audio_filename)
    vocals_path = os.path.join("audio", "vocals.wav")
    if os.path.exists(vocals_path):
        subprocess.run(["ffmpeg", "-i", vocals_path, "audio.mp3"], check=True)
    if os.path.exists("audio"):
        shutil.rmtree("audio")


def get_vocals(video_url):
    if os.path.exists("audio.mp3"):
        os.remove("audio.mp3")
    download_audio_from_youtube(video_url)
    remove_music()
