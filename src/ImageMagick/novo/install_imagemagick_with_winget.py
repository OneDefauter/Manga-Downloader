import subprocess

def install_imagemagick_with_winget():
    try:
        subprocess.run(['winget', 'install', 'ImageMagick.ImageMagick' '-h', '--accept-package-agreements', '--accept-source-agreements'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False