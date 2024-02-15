import os
import re
import shutil
import imageio
import zipfile
import win32api
import win32con
from PIL import Image
from wand.image import Image as MagickImage

tamanho_máximo = 10000
número_de_partes = 5

def cortar_imagem(image, output_folder, folder_path, allow_ext = ['.png', '.jpg', '.jpeg', '.webp']):
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the image
    image_size = Image.open(image)
    
    # Get the dimensions of the image
    width, height = image_size.size
    
    # Height of each part
    height_part = height // número_de_partes
    
    # Loop to crop the image into parts
    for i in range(número_de_partes):
        # Set the cropping coordinates for the current part
        left = 0
        top = i * height_part
        right = width
        bottom = (i + 1) * height_part

        # Crop the current part
        current_part = image_size.crop((left, top, right, bottom))

        # Save the current part with the desired name
        filename = os.path.basename(image)
        name, extension = os.path.splitext(filename)
        part_path = os.path.join(output_folder, f"{name}-{i}.jpg")
        current_part.save(part_path)

        # Close the image of the current part
        current_part.close()
    
    os.remove(image)
    
    output_files = [f for f in os.listdir(output_folder) if f.lower().endswith(tuple(allow_ext))]
    for image in output_files:
        output_pathfile = os.path.join(output_folder, image)
        shutil.move(output_pathfile, folder_path)

def verificar_imagem(folder_path, allow_ext = ['.png', '.jpg', '.jpeg', '.webp']):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(tuple(allow_ext))]
    input_images = [os.path.join(folder_path, image) for image in image_files]
    output_folder = os.path.join(folder_path, "temp")
    
    images_over_limit = []
    try:
        for image in input_images:
            try:
                image_size = Image.open(image)
            except:
                try:
                    imagem = imageio.imread(image)
                    imageio.imwrite(image, imagem)
                    image_size = Image.open(image)
                except:
                    try:
                        with MagickImage(filename=image) as img:
                            img.save(filename=image)
                        image_size = Image.open(image)
                    except:
                        continue
            tamanho = image_size.height
            image_size.close()
            if tamanho > tamanho_máximo:
                images_over_limit.append(image)
    except:
        pass

    if images_over_limit:
        for image in images_over_limit:
            cortar_imagem(image, output_folder, folder_path)
        
    if os.path.exists(output_folder):
        os.rmdir(output_folder)

def converter_imagem(folder_path, extension, allow_ext = ['.png', '.jpg', '.jpeg', '.webp']):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(tuple(allow_ext))]
    input_images = [os.path.join(folder_path, image) for image in image_files]
    
    for image in input_images:
        base, ext = os.path.splitext(image)
        if ext.lower() != extension.lower():
            try:
                imagem = imageio.imread(image)
                novo_caminho = base + extension.lower()
                imageio.imwrite(novo_caminho, imagem)
                os.remove(image)
            except:
                try:
                    with MagickImage(filename=image) as img:
                        novo_caminho = base + extension.lower()
                        img.save(filename=novo_caminho)
                    os.remove(image)
                except Exception as e:
                    print(f"Erro ao converter {image}: {e}")


def organizar(folder_path, compactar, compact_extension, extension, extensoes_permitidas = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff']):
    # Verifique se há arquivos de imagem na pasta
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(tuple(extensoes_permitidas))]

    if not image_files:
        print("Capítulo sem imagem ou não carregaram.")
        # Excluir pasta se estiver vazia
        shutil.rmtree(folder_path)
        return
        
    file_list = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(tuple(extensoes_permitidas))], key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

    count = 1

    for filename in file_list:
        base, ext = os.path.splitext(filename)
        new_filename = f"{base}__{ext}"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))

    file_list = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(tuple(extensoes_permitidas))], key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

    for filename in file_list:
        base, ext = os.path.splitext(filename)
        new_filename = f"{count:02d}{ext}"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
        count += 1



    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(tuple(extensoes_permitidas))]

    input_images = [os.path.join(folder_path, image) for image in image_files]
    output_folder = os.path.join(folder_path, "temp")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    atributos_atuais = win32api.GetFileAttributes(output_folder)
    win32api.SetFileAttributes(output_folder, atributos_atuais | win32con.FILE_ATTRIBUTE_HIDDEN)


    verificar_imagem(folder_path)
    converter_imagem(folder_path, extension)


    if compactar:
        if compact_extension == ".cbz":
            if os.path.exists(f'{folder_path}.cbz'):
                os.remove(f'{folder_path}.cbz')
            with zipfile.ZipFile(f'{folder_path}.cbz', 'w') as zipf:
                for file_name in os.listdir(folder_path):
                    if file_name.endswith(extension):
                        zipf.write(os.path.join(folder_path, file_name), file_name)
            shutil.rmtree(folder_path)
        elif compact_extension == ".zip":
            if os.path.exists(f'{folder_path}.zip'):
                os.remove(f'{folder_path}.zip')
            with zipfile.ZipFile(f'{folder_path}.zip', 'w') as zipf:
                for file_name in os.listdir(folder_path):
                    if file_name.endswith(extension):
                        zipf.write(os.path.join(folder_path, file_name), file_name)
            shutil.rmtree(folder_path)
