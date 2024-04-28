from src.ImageMagick.antigo.setup import setup as antigo
from src.ImageMagick.novo.setup import setup as novo

def setup():
    nv_ = novo()
    
    if not nv_:
        antigo()
