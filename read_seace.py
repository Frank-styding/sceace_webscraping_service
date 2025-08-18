from methods import *
def read_seace(config,words):
    url = "https://prod2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml"
    context = setup_driver_with_download_path()
    navegate_to(context,url)
    time.sleep(2)
    press_button(context, "Buscador de Procedimientos de Selección",by=By.LINK_TEXT)
    time.sleep(2)
    find_by_params(context,config)
    time.sleep(2)
    press_export(context)
    context[1].quit()
    result = read_xlr_file(context[2],words)
    return result
