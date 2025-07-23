#primeira coisa a fazer
import yt_dlp
import sys
import os

def baixar_audio(link, saida='musica_extraida.mp3'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': saida,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python baixar_audio.py <URL_DO_VIDEO>")
    else:
        link = sys.argv[1]
        baixar_audio(link)
