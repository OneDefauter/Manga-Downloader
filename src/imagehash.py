import os
import re
import imagehash
from PIL import Image

HASHS = [
    'df8fbfdf00843d2d',
    '003c7efefe7e7c00',
    '00383c3c743c3c00',
    '7f7f7f0303010103',
    '98f8dcd979fd8d0e'
]

def only_f_and_7(s):
    return re.fullmatch(r'[f7]*', s) is not None

def setup(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff')):
            file_path = os.path.join(folder_path, filename)
            # Carrega a imagem
            try:
                img = Image.open(file_path)
                img.verify()  # Verifica se a imagem é válida
                img = Image.open(file_path)  # Reabre a imagem para uso
            except:
                os.remove(file_path)
                continue
            
            # Calcula o hash da imagem
            img_hash = str(imagehash.average_hash(img))
            
            # Verifica o tamanho da imagem
            if img.width < 300 or img.height < 300:
                if not only_f_and_7(img_hash):
                    img.close()  # Garante que a imagem esteja fechada
                    os.remove(file_path)
                    continue
            
            if img_hash in HASHS:
                os.remove(file_path)
    
    imagens_hash = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff')):
            file_path = os.path.join(folder_path, filename)
            # Carrega a imagem
            try:
                img = Image.open(file_path)
                img.verify()  # Verifica se a imagem é válida
                img = Image.open(file_path)  # Reabre a imagem para uso
            except:
                os.remove(file_path)
                continue
            
            img_hash = str(imagehash.average_hash(img))
            img.close()  # Garante que a imagem esteja fechada
            
            if img_hash not in imagens_hash:
                imagens_hash.append(img_hash)
            else:
                os.remove(file_path)
