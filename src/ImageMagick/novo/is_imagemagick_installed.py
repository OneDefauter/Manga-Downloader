import subprocess

def is_imagemagick_installed():
    try:
        subprocess.run(['magick', '--version'], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False