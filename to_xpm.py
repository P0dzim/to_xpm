# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    to_xpm.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: vitosant <vitosant@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/28 12:29:55 by vitosant          #+#    #+#              #
#    Updated: 2026/02/28 12:30:00 by vitosant         ###    ########.fr       #
#                                                                              #
# **************************************************************************** #

import os
import sys
import subprocess
import shutil

def obter_comando_imagemagick():
    """Descobre qual comando do ImageMagick está instalado no sistema."""
    # Tenta encontrar 'magick' (padrão nas versões mais recentes e no Windows)
    if shutil.which("magick"):
        return ["magick"]
    # Fallback para 'convert' (padrão em versões mais antigas do ImageMagick/Linux)
    elif shutil.which("convert"):
        return ["convert"]
    else:
        return None

def converter_para_xpm(diretorio):
    # Verifica se o diretório existe
    if not os.path.exists(diretorio):
        print(f"Erro: O diretório '{diretorio}' não foi encontrado.")
        return

    # Descobre qual comando usar antes de começar o loop
    comando_base = obter_comando_imagemagick()
    
    if not comando_base:
        print("⚠️ ERRO CRÍTICO: O ImageMagick não foi encontrado no sistema!")
        print("Nem o comando 'magick' nem o 'convert' estão disponíveis.")
        print("Instale o ImageMagick e garanta que ele está no PATH (variáveis de ambiente).")
        sys.exit(1)

    extensoes_validas = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
    
    print(f"Analisando a pasta: {diretorio}")
    print(f"Usando o comando: '{comando_base[0]}'\n" + "-"*30)

    encontrou_imagem = False

    for arquivo in os.listdir(diretorio):
        if arquivo.lower().endswith(extensoes_validas):
            encontrou_imagem = True
            caminho_completo = os.path.join(diretorio, arquivo)
            nome_sem_ext = os.path.splitext(arquivo)[0]
            caminho_saida = os.path.join(diretorio, f"{nome_sem_ext}.xpm")
            
            if os.path.exists(caminho_saida):
                print(f"⏭️  Pulando '{arquivo}' (O arquivo XPM já existe)")
                continue
                
            print(f"🔄 Convertendo '{arquivo}'...")
            
            # Junta o comando base ('magick' ou 'convert') com os arquivos de entrada e saída
            comando = comando_base + [caminho_completo, caminho_saida]
            
            try:
                subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  ✓ Salvo: {nome_sem_ext}.xpm")
            except subprocess.CalledProcessError:
                print(f"  ✗ Erro ao converter {arquivo}.")

    if not encontrou_imagem:
        print("Nenhuma imagem suportada foi encontrada neste diretório.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso incorreto!")
        print("Como usar: python3 to_xpm.py <caminho_da_pasta>")
        sys.exit(1)
    
    pasta_alvo = sys.argv[1] 
    
    converter_para_xpm(pasta_alvo)
    print("\nProcesso finalizado!")