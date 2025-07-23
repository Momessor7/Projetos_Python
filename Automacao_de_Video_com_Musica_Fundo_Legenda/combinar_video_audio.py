#terceira coisa a fazer
import whisper
import subprocess
import os
import ffmpeg

AUDIO_PATH = "audios/musica_extraida.mp3"          #verificar nome e pasta corretos
VIDEO_FUNDO = "videos/fundo.mp4"
SRT_FILE = "saida/legenda.srt"
VIDEO_EXPANDIDO = "saida/video_com_audio.mp4"       #video com áudio embutido, mas ainda sem legenda
VIDEO_CORTADO = "saida/video_cortado.mp4"           #video cortado na duração da msc
SAIDA_FINAL = "saida/video_legendado.mp4"

os.makedirs("saida", exist_ok=True)

def format_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

print("🔍 Transcrevendo áudio com Whisper...")
model = whisper.load_model("base")
result = model.transcribe(AUDIO_PATH)

print("📝 Gerando arquivo de legenda...")
with open(SRT_FILE, "w", encoding="utf-8") as f:
    for i, seg in enumerate(result["segments"]):
        f.write(f"{i+1}\n")
        f.write(f"{format_srt_time(seg['start'])} --> {format_srt_time(seg['end'])}\n")
        f.write(seg["text"].strip() + "\n\n")

print("🔁 Repetindo vídeo para combinar com áudio...")
probe = ffmpeg.probe(AUDIO_PATH)
audio_duration = float(probe['format']['duration'])

probe_video = ffmpeg.probe(VIDEO_FUNDO)
video_duration = float(probe_video['format']['duration'])

repeticoes = int(audio_duration // video_duration) + 1

with open("saida/lista.txt", "w") as f:
    for _ in range(repeticoes):
        f.write(f"file '../{VIDEO_FUNDO}'\n")   #aqui o '../' é relativo ao arq lista.txt, que está na pasta "saida"

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", "saida/lista.txt",
    "-c", "copy", VIDEO_EXPANDIDO
], check=True)

#cortar p/ duração exata
subprocess.run([
    "ffmpeg", "-y", "-i", VIDEO_EXPANDIDO,
    "-ss", "0",
    "-t", str(audio_duration),
    "-c", "copy",
    VIDEO_CORTADO
], check=True)

print("🎬 Juntando vídeo cortado e áudio...")

subprocess.run([
    "ffmpeg", "-y",
    "-i", VIDEO_CORTADO,
    "-i", AUDIO_PATH,
    "-c:v", "copy",
    "-c:a", "aac",
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-shortest",
    VIDEO_EXPANDIDO    #sobrescreve o video_com_audio.mp4 com áudio embutido
], check=True)
