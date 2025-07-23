#segunda coisa a fazer
from faster_whisper import WhisperModel

def formatar_tempo(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = segundos % 60
    return f"{horas:02}:{minutos:02}:{segundos:06.3f}".replace(".", ",")

def gerar_legenda(audio_path, legenda_path):
    model = WhisperModel("medium", compute_type="int8")
    segments, _ = model.transcribe(audio_path)

    with open(legenda_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments):
            f.write(f"{i + 1}\n")
            f.write(f"{formatar_tempo(segment.start)} --> {formatar_tempo(segment.end)}\n")
            f.write(f"{segment.text.strip()}\n\n")
