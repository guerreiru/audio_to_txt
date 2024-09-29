import tkinter as tk
from tkinter import filedialog, messagebox
import os
import whisper
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from threading import Thread

def get_documents_dir():
    """Obtém o diretório 'Documentos' do usuário."""
    return os.path.join(os.path.expanduser("~"), "Documents")

def save_to_txt(text, archive):
    """Salva o texto transcrito em um arquivo .txt no diretório 'Documentos'."""
    documents_dir = get_documents_dir()
    base_name = os.path.splitext(os.path.basename(archive))[0]
    file_name = os.path.join(documents_dir, f"{base_name}.txt")
    
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(text)
        messagebox.showinfo("Sucesso", f"Texto transcrito salvo em {file_name}")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {str(e)}")

def select_audio_file():
    """Abre o dialog para selecionar um arquivo de áudio."""
    return filedialog.askopenfilename(
        title="Selecione um arquivo de áudio",
        filetypes=[("Arquivos de áudio", "*.mp3 *.wav *.m4a *.ogg")]
    )

def transcribe_audio():
    """Inicia a transcrição do áudio selecionado."""
    audio_file = select_audio_file()
    
    if not audio_file:
        return  # Se o usuário cancelar a seleção, sai da função
    
    progress_bar.pack(pady=10, fill='x', padx=20)
    progress_bar.start()
    
    # Usa threading para não travar a interface
    Thread(target=process_transcription, args=(audio_file,)).start()

def process_transcription(audio_file):
    """Processa a transcrição do áudio em segundo plano."""
    try:
        result_text.set("Transcrevendo o áudio, por favor aguarde...")
        
        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        
        save_to_txt(result['text'], audio_file)
        result_text.set('Transcrição concluída com sucesso!')
        
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao transcrever o áudio: {str(e)}")
        result_text.set("")
    finally:
        progress_bar.stop()

# Configurações da janela principal (UI)
window = ttk.Window(themename="darkly")  
window.title("Transcrição de Áudio para Texto")
window.geometry("600x400")

# Elementos da interface
label_instructions = ttk.Label(window, text="Selecione um arquivo de áudio para transcrição:", font=("Segoe UI", 14))
label_instructions.pack(pady=20)

btn_select = ttk.Button(window, text="Selecionar Áudio", bootstyle="primary", command=transcribe_audio)
btn_select.pack(pady=10)

progress_bar = ttk.Progressbar(window, bootstyle=INFO, mode='indeterminate')

result_text = tk.StringVar()
label_result = ttk.Label(window, textvariable=result_text, wraplength=500, font=("Segoe UI", 12), justify="left")
label_result.pack(pady=20)

window.mainloop()
