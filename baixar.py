import os
import urllib.request
import pandas as pd

# Função para carregar o dicionário
def carregar_dicionario(csv_path):
    return pd.read_csv(csv_path, delimiter=',')

# Função para baixar imagens com cabeçalhos HTTP
def baixar_imagens(dicionario, pasta_destino):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)  # Cria a pasta de destino se não existir

    for index, row in dicionario.iterrows():
        image_url = row['hand_image_link']
        if pd.notna(image_url):  # Verifica se o link da imagem existe
            nome_imagem = f"{row['word']}.jpg"  # Nome da imagem, baseado na palavra
            caminho_imagem = os.path.join(pasta_destino, nome_imagem)
            try:
                # Adicionando cabeçalhos para simular uma requisição de navegador
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                }
                req = urllib.request.Request(image_url, headers=headers)
                with urllib.request.urlopen(req) as response, open(caminho_imagem, 'wb') as out_file:
                    out_file.write(response.read())  # Baixa a imagem
                print(f"Imagem '{nome_imagem}' baixada com sucesso.")
            except Exception as e:
                print(image_url)
                print(f"Erro ao baixar imagem para '{row['word']}': {e}")

# Caminho para o CSV do dicionário
caminho_csv = "dicionario_libras.csv"  # Substitua com o caminho correto para o seu arquivo CSV
# Pasta de destino para armazenar as imagens
pasta_destino = "imagens_libras"

# Carregar dicionário e baixar as imagens
try:
    dicionario = carregar_dicionario(caminho_csv)
    baixar_imagens(dicionario, pasta_destino)
except Exception as e:
    print(f"Erro ao carregar o dicionário: {e}")
