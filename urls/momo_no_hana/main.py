import urls.momo_no_hana.Cloudflare.main as main_cloudflare
import urls.momo_no_hana.Normal.main as main

async def setup(
    driver,
    url,
    capítulo,
    ate,
    debug_var,
    baixando_label,
    folder_selected,
    nome_foler,
    nome,
    compactar,
    compact_extension,
    extension,
    download_folder,
    app_instance,
    max_attent,
    max_verify,
    username,
    password,
    cloudflare
):
    
    if cloudflare:
        result = await main_cloudflare.setup(
            driver,
            url,
            capítulo,
            ate,
            debug_var,
            baixando_label,
            folder_selected,
            nome_foler,
            nome,
            compactar,
            compact_extension,
            extension,
            download_folder,
            app_instance,
            max_attent,
            max_verify
        )
    
    else:
        result = await main.setup(
            driver,
            url,
            capítulo,
            ate,
            debug_var,
            baixando_label,
            folder_selected,
            nome_foler,
            nome,
            compactar,
            compact_extension,
            extension,
            download_folder,
            app_instance,
            max_attent,
            max_verify
        )
        
    return result