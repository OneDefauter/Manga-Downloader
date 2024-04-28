from src.ImageMagick.antigo.version_to_tuple import version_to_tuple

def compare_versions(installed_version, required_version):
    # Converter as versões para tuplas de números inteiros
    installed_version_tuple = version_to_tuple(installed_version)
    required_version_tuple = version_to_tuple(required_version)

    # Comparar as versões
    return installed_version_tuple >= required_version_tuple

