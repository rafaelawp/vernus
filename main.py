import tkinter as tk
from tkinter import scrolledtext, messagebox
import pandas as pd
import time
import PIL.Image, PIL.ImageTk
import os
import re
import spacy

# Carrega o modelo de português do spaCy
nlp = spacy.load("pt_core_news_sm")

# Lematiza uma palavra (traz para o infinitivo se for verbo)
def lematizar(palavra):
    doc = nlp(palavra)
    for token in doc:
        return token.lemma_

# Carrega o dicionário CSV
def carregar_dicionario(csv_path):
    return pd.read_csv(csv_path, delimiter=',')

# Busca uma palavra exata ou variantes, com lematização para verbos conjugados
def buscar_palavra(palavra, dicionario):
    # Busca direta
    resultado = dicionario[dicionario['word'].str.lower() == palavra.lower()]
    if not resultado.empty:
        return resultado.iloc[0]
    
    # Busca pela lematização
    # if resultado.iloc[0] = False: ou if resultado.empty:
    palavra_lematizada = lematizar(palavra)
    print(f"Palavra original: {palavra}, Lematizada: {palavra_lematizada}")
    resultado_lematizado = dicionario[dicionario['word'].str.lower() == palavra_lematizada.lower()]
    if not resultado_lematizado.empty:
        return resultado_lematizado.iloc[0]

    # Busca variantes (ex: palavra1, palavra2)
    regex = re.compile(f"^{palavra}\\d+$", re.IGNORECASE)
    variantes = dicionario[dicionario['word'].str.match(regex, na=False)]
    if not variantes.empty:
        return variantes.iloc[0]

    return None

# Ação do botão "Buscar" (não está sendo usado na GUI atual)
def acao_buscar():
    palavra = text_frame.get()
    resultado = buscar_palavra(palavra, dicionario)
    if resultado is not None:
        translation_label.config(text=f"{resultado['interpretation']}")
        image_path = os.path.join("imagens_libras", f"{resultado['word']}.jpg")
        if os.path.exists(image_path):
            carregar_imagem(image_path)
    else:
        translation_label.config(text="Palavra não encontrada.")

# Ação do botão "Interpretar"

# !!!!! soletrar está sendo pulado
def exibir_interpretacao():
    texto = entrada_texto.get("1.0", tk.END).strip()
    palavras = texto.split()
    
    for palavra in palavras:
        resultado = buscar_palavra(palavra, dicionario)
        
        if resultado is not None:
            translation_label.config(text=f"{resultado['interpretation']}")
            image_path = os.path.join("imagens_libras", f"{resultado['word']}.jpg")
            if os.path.exists(image_path):
                carregar_imagem(image_path)
        elif resultado is None:
            # Aqui você deve buscar a palavra lematizada
            palavra_lematizada = lematizar(palavra)
            resultado_lematizado = buscar_palavra(palavra_lematizada, dicionario)
            
            if resultado_lematizado is not None:
                translation_label.config(text=f"{resultado_lematizado['interpretation']}")
                image_path = os.path.join("imagens_libras", f"{resultado_lematizado['word']}.jpg")
                if os.path.exists(image_path):
                    carregar_imagem(image_path)
                
            root.update()
            time.sleep(2)
        else:
            translation_label.config(text=f"Palavra '{palavra}' não encontrada. Exibindo letra por letra.")
            root.update()
            time.sleep(2)
            for letra in palavra:
                resultado_letra = buscar_palavra(letra, dicionario)
                if resultado_letra is not None:
                    translation_label.config(text=f"Letra: {letra}")
                    image_path = os.path.join("imagens_libras", f"{resultado_letra['word']}.jpg")
                    
                    if os.path.exists(image_path):
                        carregar_imagem(image_path)
                    
                    root.update()
                    time.sleep(1)
                else:
                    translation_label.config(text=f"Letra '{letra}' não encontrada.")
                    root.update()
                    time.sleep(1)

# Exibe imagem no label
def carregar_imagem(image_path):
    img = PIL.Image.open(image_path)
    img = img.resize((300, 300), PIL.Image.LANCZOS)
    imgtk = PIL.ImageTk.PhotoImage(image=img)
    imagem_label.config(image=imgtk)
    imagem_label.image = imgtk

# ------------------- GUI -------------------

root = tk.Tk()
root.title("Tradutor e Visualizador de Libras")
root.geometry("1100x820")
root.resizable(width=False, height=False)

# Cabeçalho
header_frame = tk.Frame(root, bg= "#a82428")
header_frame.pack(fill=tk.X)

title_label = tk.Label(header_frame, text="Tradutor e Visualizador de Libras", bg="#a82428", fg="white", font=("Arial", 20))
title_label.pack(side=tk.LEFT, padx=10)

# Menu
menu_frame = tk.Frame(root, bg="#359830")
menu_frame.pack(fill=tk.X)

menu_items = ["Guias de Mobilidade", "Ajuda"]
for item in menu_items:
    btn = tk.Button(menu_frame, text=item, font=("Arial", 12), bg="#ffffff",
                    command=lambda text=item: messagebox.showinfo("Info", f"Você clicou em {text}"))
    btn.pack(side=tk.LEFT, padx=5)

# Tela principal
main_frame = tk.Frame(root, bg="#943199")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Entrada de texto
text_frame = tk.Frame(main_frame, bg="#F3F9D2")
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

text_label = tk.Label(text_frame, text="Insira texto:", bg="#F3F9D2", font=("Arial", 12))
text_label.pack()

entrada_texto = scrolledtext.ScrolledText(text_frame, height=6, font=("Arial", 12))
entrada_texto.pack(fill=tk.BOTH, expand=True)

# Botão interpretar
botao_interpretar = tk.Button(main_frame, text="Interpretar", command=exibir_interpretacao, font=("Arial", 12))
botao_interpretar.pack(pady=5)

# Tradução e Imagem lado a lado
resultado_frame = tk.Frame(main_frame, bg="#F3F9D2")
resultado_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Label de tradução (à esquerda)
translation_label = tk.Label(resultado_frame, text="tradução aparecerá aqui", bg="#F3F9D2", font=("Arial", 12), justify="left", wraplength=300)
translation_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

# Label de imagem (à direita)
imagem_label = tk.Label(resultado_frame, bg="#F3F9D2")
imagem_label.pack(side=tk.LEFT, padx=10)

# Carrega dicionário
caminho_csv = "dicionario_libras.csv"
try:
    dicionario = carregar_dicionario(caminho_csv)
except Exception as e:
    translation_label.config(text=f"Erro ao carregar dicionário: {e}")

root.mainloop()
