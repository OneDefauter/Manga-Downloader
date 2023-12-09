import os
import asyncio
from colorama import Fore, Style

async def download(link, folder_path, session, counter, max_attempts=10, sleep_time=5, extensoes_permitidas2 = ['png', 'jpg', 'jpeg', 'webp', 'gif', 'apng', 'avif', 'bmp', 'tiff']):
    attempts = 0
    while attempts < max_attempts:
        try:
            for x in extensoes_permitidas2:
                if x in link.lower():
                    if not f".{x}" in link.lower():
                        link2 = link.lower().replace(f"{x}", f".{x}")
                        image_extension = link2.split(".")[-1]
                    else:
                        image_extension = link.split(".")[-1]
                    
            image_name = f"{counter:02d}.{image_extension}"
            image_path = os.path.join(folder_path, image_name)

            # Aguardar um tempo antes de fazer o download
            await asyncio.sleep(2)

            async with session.get(link, ssl=False) as response:
                # Verificar se a resposta tem status 200 (OK)
                if response.status == 200:
                    print(f"{Fore.GREEN}Baixando {link} como {image_name}...{Style.RESET_ALL}")
                    
                    # Salvar a imagem no disco
                    with open(image_path, "wb") as f:
                        f.write(await response.read())

                    # Se chegou até aqui, o download foi bem-sucedido, então saia do loop
                    break
                else:
                    print(f"{Fore.RED}Tentativa {attempts + 1} - Erro ao baixar {link}. Status code: {response.status}{Style.RESET_ALL}")
                    # Aguardar um tempo antes de tentar novamente
                    await asyncio.sleep(sleep_time)

        except Exception as e:
            print(f"Tentativa {attempts + 1} - Erro ao baixar {link}: {e}")

        # Incrementar o número de tentativas
        attempts += 1

    # Se chegou aqui, significa que atingiu o número máximo de tentativas sem sucesso
    if attempts == max_attempts:
        print(f"Atenção: Não foi possível baixar {link} após {max_attempts} tentativas.")

