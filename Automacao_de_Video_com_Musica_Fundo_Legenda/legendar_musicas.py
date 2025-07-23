#quinta coisa a fzr
from gerar_legenda import gerar_legenda
from adicionar_legenda import adicionar_legenda

#caminhos -- ajustar conforme estrutura
audio_path = "audios/musica_extraida.mp3"
video_fundo = "videos/fundo.mp4"
legenda_path = "saida/legenda.srt"
video_com_audio_path = "saida/video_com_audio.mp4"
video_final_path = "saida/video_legendado.mp4"

#gerar legenda
gerar_legenda(audio_path, legenda_path)

#gerar vídeo com áudio e duração igual da música (executar script combinar_video_audio.py separadamente, ou copiar função aqui)
#OBS: Para evitar duplicação, o ideal é importar a função ou chamar o script.
#aqui só para dar ex, pode chamar via subprocess:
import subprocess
subprocess.run(["python", "combinar_video_audio.py"])

#add legenda embutida no vídeo final
adicionar_legenda(video_com_audio_path, legenda_path, video_final_path)

print("✅ Tudo pronto! Vídeo final com legenda está em:", video_final_path)
