from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import os,time,glob
import pandas as pd
import json
import base64
import sys
from datetime import datetime,timedelta
def setup_driver_with_download_path(dev = False):
    download_path = os.path.join(os.getcwd(), "descargas_selenium")
    os.makedirs(download_path, exist_ok=True)

    chrome_options = Options()
    chrome_prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_settings.popups": 0,  # deshabilitar popups
        "download.allow_multiple_downloads": True      # permitir varias descargas
    }
    #params = {
    #"behavior": "allow",
    #"downloadPath": download_path
    #}
    if not dev: chrome_options.add_argument("--headless=new")  # usa la nueva versión de headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", chrome_prefs)
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver,timeout=100)
    #driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
    return (wait, driver, download_path)

def navegate_to(context,url):
    context[1].get(url)


def wait_for_download(download_path):
    csv_files = glob.glob(os.path.join(download_path, "*.xls"))
    if csv_files:
        latest_file = max(csv_files, key=os.path.getctime)
        return latest_file
    time.sleep(1)

def set_input_value(context,id,value):
    for _ in range(2):
        try:
            ajax_element = context[0].until(
                EC.element_to_be_clickable((By.ID, id))
                )
            ajax_element.click()
            break
        except StaleElementReferenceException:
            time.sleep(0.5)  # esperar y reintentar

    campo = context[0].until(
                EC.element_to_be_clickable((By.ID, id))
                )

    campo.clear()
    campo.send_keys(value)

def press_button(context,id,intents = 0,by=By.ID):
    for _ in range(intents):
        try:
            context[0].until(
                EC.element_to_be_clickable((by, id))
                )
            break
        except StaleElementReferenceException:
            time.sleep(0.5)


    button = context[0].until(
                EC.element_to_be_clickable((by, id))
            )
    button.click()


def press_button_script(context,id,intents = 2, by = By.ID):
    for _ in range(intents):
        try:
            context[0].until(
                EC.element_to_be_clickable((by, id))
                )
            break
        except StaleElementReferenceException:
            time.sleep(0.5)


    button = context[0].until(
                EC.element_to_be_clickable((by, id))
            )
    context[1].execute_script("arguments[0].click();", button)

def execute_script(context,script):
    context[1].execute_script(script)
    
def read_xlr_file(download_path,words = []):
    time.sleep(2)
    xls_file = wait_for_download(download_path)
    df = pd.read_excel(xls_file, engine="xlrd")  # Para .xls antiguos
    df = df.where(pd.notnull(df), None)
    df = df.fillna("")
    if len(words) > 0:
        df = df[df[df.columns[6]].astype(str).str.lower().apply(
            lambda valor: any(palabra.lower() in valor for palabra in words)
        )]

    # Calcular el timestamp de hace un mes (30 días)
    hace_un_mes = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)
    
    # Filtrar filas usando convert_to_time solo para comparar fechas
    # (mantener solo las fechas que son posteriores a hace_un_mes)
    df = df[df[df.columns[2]].apply(convert_to_time) >= hace_un_mes]

    df = df.drop(df.columns[[0,4,7,8,9]], axis=1)
    resultado = df.to_dict(orient="records")
    os.remove(xls_file)
    return resultado

def print_data(data):
    os.system("cls")
    json_str = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    base64_str = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    print(base64_str)

def read_args():
    result = {}
    if len(sys.argv) >= 2:
        for i in range(1,len(sys.argv)):
            item =sys.argv[i].split(":")
            result[item[0]] = str(item[1])
    return result

def set_ruc(context,ruc):    
    press_button(context,"tbBuscador:idFormBuscarProceso:ajax")
    time.sleep(0.5)
    set_input_value(context,"tbBuscador:idFormBuscarProceso:txtRucEntidad",ruc)
    press_button(context,"tbBuscador:idFormBuscarProceso:btnBuscarEntidad")
    press_button(context,"tbBuscador:idFormBuscarProceso:dataTable:0:ajax")

def set_keyword(context,keyword):
    set_input_value(context,"tbBuscador:idFormBuscarProceso:descripcionObjeto",keyword)


def press_seach(context):
    time.sleep(1.5)
    press_button(context,"tbBuscador:idFormBuscarProceso:btnBuscarSelToken")

def press_export(context):
    press_button(context,"tbBuscador:idFormBuscarProceso:btnExportar")
    time.sleep(2)

def set_description(context,description):
    set_input_value(context,"tbBuscador:idFormbuscarACF:descripcionObjeto",description)

def set_code(context,code):
    press_button(context,"//legend[normalize-space()='Búsqueda Avanzada']",by=By.XPATH)
    time.sleep(1.5)
    set_input_value(context,"tbBuscador:idFormBuscarProceso:siglasEntidad",code)

def find_by_params(wait,params):
    keys = params.keys()
    if "ruc" in keys and params["ruc"] != None:
        set_ruc(wait,params["ruc"])
    if "description" in keys and params["description"] != None:
        set_description(wait,params["description"])
    if "keyword" in keys and params["keyword"] != None:
        set_keyword(wait,params["keyword"])
    if "code" in keys and params["code"] != None:
        set_code(wait,params["code"])
    press_seach(wait)
def convert_to_time(date):
    try:
        return int(datetime.strptime(date, "%d/%m/%Y %H:%M").timestamp() * 1000)
    except ValueError:
        return int(datetime.strptime(date, "%d/%m/%Y").timestamp() * 1000)
    return date