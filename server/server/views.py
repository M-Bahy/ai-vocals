from django.http import HttpResponse, HttpResponseBadRequest, FileResponse
import re
import os
from . import vocals


def is_valid_url(url):

    youtube_regex = re.compile(
        r"^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$"
    )
    return re.match(youtube_regex, url) is not None


def convert(request):
    url = request.GET.get("url")

    if not url:
        return HttpResponseBadRequest("URL parameter is missing")

    if is_valid_url(url):
        vocals.get_vocals(url)

        files = os.listdir(".")
        mp3_files = [file for file in files if file.endswith(".mp3")]
        if mp3_files:
            audio_file_path = mp3_files[0]
            if os.path.exists(audio_file_path):
                return FileResponse(
                    open(audio_file_path, "rb"),
                    as_attachment=True,
                    filename=audio_file_path,
                )
            else:
                return HttpResponseBadRequest("Audio file not found")
        else:
            return HttpResponseBadRequest("No .mp3 files found in the directory")
    else:
        return HttpResponseBadRequest("Invalid YouTube URL")
