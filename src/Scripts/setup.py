from src.Scripts.Normal.ImageDownloader import setup as ImageDownloader
from src.Scripts.Normal.Picviewer import setup as Picviewer
from src.Scripts.Normal.Teste import setup as Download

from src.Scripts.Cloudflare.ImageDownloader import setup as ImageDownloader_cloudflare
from src.Scripts.Cloudflare.Picviewer import setup as Picviewer_cloudflare
from src.Scripts.Cloudflare.Teste import setup as Download_cloudflare
from src.Scripts.Cloudflare.Cloudflare import setup as Cloudflare_cloudflare

async def setup(
    driver,
    e_01 = False,
    e_02 = False,
    e_03 = False,
    e_04 = False,
    cloudflare = False
):
    if cloudflare:
        if e_01:
            await ImageDownloader_cloudflare(driver)
        if e_02:
            await Picviewer_cloudflare(driver)
        if e_03:
            await Download_cloudflare(driver)
        if e_04:
            await Cloudflare_cloudflare(driver)
        
    else:
        if e_01:
            ImageDownloader(driver)
        if e_02:
            Picviewer(driver)
        if e_03:
            Download(driver)
            
def setup_not_cloudflare(driver):
    Picviewer(driver)