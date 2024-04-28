import re

def version_to_tuple(version_str):
    # Função para converter a versão em uma tupla de números inteiros
    return tuple(map(int, re.findall(r'\d+', version_str)))
