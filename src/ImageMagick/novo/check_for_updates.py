import subprocess

def check_for_updates():
    try:
        subprocess.run(['winget', 'upgrade', 'ImageMagick.ImageMagick'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False