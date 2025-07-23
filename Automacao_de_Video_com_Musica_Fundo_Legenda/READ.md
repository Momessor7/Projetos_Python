# 🎶 Automatizador de Vídeos com Música, Fundo e Legendas 🎬

Este projeto é uma automação completa que:
1. Extrai o áudio de um vídeo musical.
2. Seleciona automaticamente um vídeo de fundo (loopado se necessário).
3. Transcreve a letra da música.
4. Gera legendas sincronizadas.
5. Renderiza um vídeo final com o áudio da música, vídeo de fundo e legendas.

## 📁 Estrutura de Pastas
Automatizar_musicas/
├── audios/
│ └── musica_extraida.mp3 ->Áudio extraído do vídeo original
├── videos_fundo/
│ └── fundo.mp4 ->Vídeo de fundo a ser usado
├── legendas/
│ └── legenda_ass.ass ->Legenda gerada automaticamente
├── saida/
│ └── video_final.mp4 ->Resultado final com tudo combinado
├── gerar_legenda.py ->Script que transcreve o áudio e gera legenda ASS
├── combinar_video_audio.py ->Script que junta vídeo de fundo + áudio + legenda
├── requirements.txt ->Dependências do projeto
└── README.md ->Documentação do projeto


## 🧠 Requisitos

- Python 3.10+
- FFmpeg instalado e disponível no PATH
- Virtualenv recomendado

## 📦 Instalação

git clone https://github.com/seu-usuario/Automatizar_musicas.git
cd Automatizar_musicas
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Como Usar
Coloque o vídeo de fundo em videos_fundo/fundo.mp4
Coloque o áudio extraído da música em audios/musica_extraida.mp3
Execute o script de geração de legendas: python gerar_legenda.py. Depois, combine tudo com: python combinar_video_audio.py. O resultado final estará em saida/video_final.mp4.

## ✅ Funcionalidades
🧠 Transcrição com Whisper (OpenAI)
📝 Geração de legendas no formato .ass
📽 Combinação de vídeo + áudio + legenda via FFmpeg
🔁 Loop automático do vídeo de fundo se for mais curto que a música
🗣 Legendas sincronizadas com a letra da música

OBS: Tentei utilizar o "moviepy", porém devido a uma série de erros em que eu quebrei a cabeça e tive dificuldades em continuar, acabei optando por escolher um caminho que exige mais da cpu, porém é muito seguro e tranquilo de se codar(ffmpeg diretamente via módulo ffmpeg-python para todas as estapas de combinação).

🧠 Desenvolvido por Gabriel Momesso com Python + Whisper + FFmpeg