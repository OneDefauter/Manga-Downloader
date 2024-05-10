import asyncio

# Image Downloader
async def setup(driver):
    url_extension = 'https://update.greasyfork.org/scripts/24204/Picviewer%20CE%2B.user.js'
    pagina = await driver.get(url_extension, new_tab=True)

    await asyncio.sleep(2)
    
    await pagina
    
    btn = await pagina.find('confirm')
    await btn.click()
    
    await pagina.close()
