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

        info_dict = ydl.extract_info(video_url, download=False)
        video_title = info_dict.get("title", None)
        ydl.download([video_url])

    return video_title


def remove_music(video_title, audio_filename="audio.mp3"):
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
        subprocess.run(["ffmpeg", "-i", vocals_path, video_title + ".mp3"], check=True)
    if os.path.exists("audio"):
        shutil.rmtree("audio")


def get_vocals(video_url):

    files = os.listdir('.')
    mp3_files = [file for file in files if file.endswith('.mp3')]
    for mp3_file in mp3_files:
        if os.path.exists(mp3_file):
            os.remove(mp3_file)

    video_title = download_audio_from_youtube(video_url)
    remove_music(video_title)
