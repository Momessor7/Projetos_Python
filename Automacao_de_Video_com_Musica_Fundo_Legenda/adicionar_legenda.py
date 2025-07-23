#quarta coisa a fazer
import subprocess

def adicionar_legenda(video_entrada, legenda_srt, video_saida):
    cmd = [
        "ffmpeg",
        "-i", video_entrada,
        "-vf", f"subtitles={legenda_srt}",
        "-c:a", "copy",
        video_saida,
        "-y"
    ]
    subprocess.run(cmd, check=True)
