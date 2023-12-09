import pytz
from datetime import datetime

def setup():
    tz = pytz.timezone('America/Sao_Paulo')
    hora = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
    
    return hora