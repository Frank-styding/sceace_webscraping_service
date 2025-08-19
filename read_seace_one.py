from methods import *
from bs4 import BeautifulSoup
from datetime import datetime
import io
import zipfile

def press_first_button(context):
    execute_script(context,'Array.from(document.querySelectorAll(".ui-widget-content.ui-datatable-even   .ui-commandlink.ui-widget")).pop()?.click()')



        
def get_table_data(context):
    html = context[1].find_element(By.ID,"tbFicha:dtCronograma_data").get_attribute("innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    data = []
    for tr in soup.find_all("tr"):
        celds = tr.find_all("td")
        row = []
        for td in celds:
            text = td.get_text(separator=" ", strip=True)
            row.append(text)
        data.append(row)

    return (convert_to_time(data[1][1]), convert_to_time(data[1][2]))
        
def download_files(context):
    context[1].execute_script('Array.from(document.querySelectorAll(".ui-datatable-data.ui-widget-content .ui-commandlink.ui-widget > span")).forEach((item,i)=>setTimeout(()=>item.parentElement.click(), i*5000));')



def convert_to_zip():
    folder = "descargas_selenium"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zipf:
        for filename in os.listdir(folder):
            ruta = os.path.join(folder, filename)
            if os.path.isfile(ruta):
                zipf.write(ruta, arcname=filename)  # arcname = nombre dentro del ZIP
    buf.seek(0)

    # Borrar archivos originales después de comprimir
    for filename in os.listdir(folder):
        ruta = os.path.join(folder, filename)
        if os.path.isfile(ruta):
            os.remove(ruta)
    return buf




def get_url_for_items(data:list[dict],dev=True):
    url = "https://prod2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml"
    context = setup_driver_with_download_path(dev)
    navegate_to(context,url)
    press_button(context, "Buscador de Procedimientos de Selección",by =By.LINK_TEXT)
    time.sleep(1)

    ndata = []

    for item in data:
        if not "Nomenclatura" in item.keys():continue
        try:
            print(item["Nomenclatura"])
            find_by_params(context,{"code":item["Nomenclatura"]})
            time.sleep(3);
            press_first_button(context)
            time.sleep(3)
            time_intervar = get_table_data(context)
            now = int(datetime.now().timestamp()* 1000)
            if  now <= time_intervar[1]:
                item["url"] = context[1].current_url
                ndata.append(item)
            time.sleep(1)
            navegate_to(context,url)
            time.sleep(3)
            press_button(context,"tbBuscador:idFormBuscarProceso:btnLimpiarSel")
            time.sleep(3)
        except:
            continue

    context[1].close()

    return ndata        


#    press_button(context, "Buscador de Procedimientos de Selección",by =By.LINK_TEXT)
#    time.sleep(0.5)
#    find_by_params(context,{"code":code})
#    time.sleep(2);
#    press_first_button(context)
#    time.sleep(2)
#    time_intervar = get_table_data(context)
#    now = int(datetime.now().timestamp()* 1000)
#    if  now <= time_intervar[1]:
#        return context[1].current_url
#    return None
    

