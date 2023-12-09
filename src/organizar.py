import os
import re
import shutil
import win32api
import win32con
import subprocess
import zipfile


def organizar(folder_path, compactar, compact_extension, extension, extensoes_permitidas = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff']):
    # Verifique se há arquivos de imagem na pasta
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(tuple(extensoes_permitidas))]

    if not image_files:
        print("Capítulo sem imagem.")
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



    output_filename = os.path.join(output_folder, f"0.jpg")
    command = ["magick", "convert", "-quality", "100", "-crop", f"32000x5000"]

    command += input_images + [output_filename]

    subprocess.run(command, check=True)

    for image_file in input_images:
        os.remove(image_file)

    # Contador para numerar os arquivos
    count = 1

    output_files = sorted([f for f in os.listdir(output_folder) if f.lower().endswith(tuple(extensoes_permitidas))], key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

    for filename in output_files:
        base, ext = os.path.splitext(filename)
        new_filename = f"{count:02d}{ext}"
        os.rename(os.path.join(output_folder, filename), os.path.join(output_folder, new_filename))
        count += 1

    output_files = [f for f in os.listdir(output_folder) if f.lower().endswith(tuple(extensoes_permitidas))]
    for image in output_files:
        output_pathfile = os.path.join(output_folder, image)
        shutil.move(output_pathfile, folder_path)

    # shutil.move(output_filename, folder_path)
    output_folder2 = os.path.join(folder_path, "temp")
    os.removedirs(output_folder2)
    
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
