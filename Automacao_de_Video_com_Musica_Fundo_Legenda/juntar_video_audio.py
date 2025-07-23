import whisper
import subprocess

def transcrever_audio(caminho_audio):
    model = whisper.load_model("small")
    resultado = model.transcribe(caminho_audio)
    print("Transcrição:")
    print(resultado["text"])
    return resultado["text"]

def juntar_audio_video(video_path, audio_path, output_path):
    cmd = [
    'ffmpeg',
    '-stream_loop', '-1',
    '-i', caminho_video,
    '-i', caminho_audio,
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-strict', 'experimental',
    '-shortest',
    caminho_saida
    ]
    subprocess.run(cmd, check=True)
    print(f"Vídeo final salvo em: {output_path}")

if __name__ == "__main__":
    caminho_audio = "musica_extraida.mp3"
    caminho_video = "video_de_fundo.mp4"
    caminho_saida = "video_com_audio.mp4"

    legenda = transcrever_audio(caminho_audio)

    juntar_audio_video(caminho_video, caminho_audio, caminho_saida)
