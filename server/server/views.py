from django.http import HttpResponse, HttpResponseBadRequest, FileResponse
import re
import os
from . import vocals


def is_valid_url(url):
    # Regular expression to check if the URL is a valid YouTube URL
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

        # Path to the audio file
        audio_file_path = "audio.mp3"

        # Check if the file exists
        if os.path.exists(audio_file_path):
            return FileResponse(
                open(audio_file_path, "rb"), as_attachment=True, filename="audio.mp3"
            )
        else:
            return HttpResponseBadRequest("Audio file not found")
    else:
        return HttpResponseBadRequest("Invalid YouTube URL")
