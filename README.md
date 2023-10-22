# Manga Downloader

Este código usa [selenium](https://www.selenium.dev/pt-br/documentation/) para conseguir as URL's das imagens dos capítulos e então baixa e coloca em sua receptiva pasta.

# Requisitos
● [**Python**](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)\n
● [**ImageMagick**](https://github.com/OneDefauter/Menu_/releases/download/Req/ImageMagick-7.1.1-21-Q16-HDRI-x64-dll.exe)

## Módulos necessários
● **requests**
● **pywin32**
● **selenium**
● **aiohttp**

***Nota: os módulos são instalados caso não tenha.***

## Instalação

Baixe o arquivo [**run.py**](https://github.com/OneDefauter/Manga-Downloader/releases/download/Main/run.py) e inicie e pronto.

## Argumentos

|                |Encurtado                          |Completo                         |
|----------------|-------------------------------|-----------------------------|
|**Executar o Selenium em modo não segundo plano**|**`-nh`**            |**`--no-headless`**            |
|**Número do agregador**         |**`-a`**            |**`--agregador`**            |
|**Nome da obra**          |**`-n`**|**`--nome`**|
|**Número do capítulo**          |**`-c`**|**`--capitulo`**|
|**Até qual capítulo baixar**          |**`-t`**|**`--ate`**|

**Exemplo de uso: run.py -a 1 -n "Is This Hero For Real?" -c 50**

**Com esse argumento vai baixar o capítulo 50 da obra 'Is This Hero For Real?' no agregador 1**

**Caso queira baixar vários capítulos use: run.py -a 1 -n "Is This Hero For Real?" -c 50 -t 80**

**Assim irá baixar do capítulo 50 ao 80.**
