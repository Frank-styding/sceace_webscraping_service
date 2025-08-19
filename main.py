from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from read_seace import *
from read_seace_one import get_url_for_items
#   from test_data import data

app = FastAPI()


class FindBody(BaseModel):
    ruc: str|None = None
    keyword: str|None = None
    words: list[str]|None = None

@app.post("/find")
async def find_data(body:FindBody):
    config = {}
    words = []
    if body.ruc != None:
        config["ruc"] = body.ruc
    if body.keyword != None:
        config["keyword"] = body.keyword
    if body.words != None:
        words = body.words
    return read_seace(config,words,dev=False)


class FindOneBody(BaseModel):
    data:list[dict]


@app.post("/findOne")
async def find_data(body: FindOneBody):
    return get_url_for_items(body.data,dev=False)
    ##url = read_one(body.code)
    ##if url is None:
    ##    return {"error": True}
    ##body.data["url"] = url
    ##return body.data
    


#print(get_url_for_items(data[0]["data"]))
#data = [
#{
#"Nombre o Sigla de la Entidad": 
#"AUTORIDAD NACIONAL DE INFRAESTRUCTURA",
#"Fecha y Hora de Publicacion": 
#"15/08/2025 16:42",
#"Nomenclatura": 
#"PEC-PROC-5-2025-ANIN/DAI-1",
#"Objeto de Contratación": 
#"Servicio",
#"Descripción de Objeto": 
#"SERVICIO DE ALQUILER DE TRES CAMIONETAS PARA GESTIÓN DEL OBJETIVO 5 ¿PLAN DE TRABAJO ESPECÍFICO PARA LA FORMULACIÓN DEL ESTUDIO DE PRE INVERSIÓN A NIVEL DE PERFIL¿, DEL PROYECTO DE ¿MEJORAMIENTO Y AMPLIACIÓN DEL SERVICIO DE DRENAJE PLUVIAL EN LOS DISTRITOS DE PIURA, CASTILLA, CATACAOS Y DISTRITO DE"
#},
#{
#"Nombre o Sigla de la Entidad": 
#"UNIVERSIDAD NACIONAL INTERCULTURAL DE LA SELVA CENTRAL JUAN SANTOS ATAHUALPA",
#"Fecha y Hora de Publicacion": 
#"12/08/2025 19:42",
#"Nomenclatura": 
#"CONV-PROC-4-2025-DEC/UNISCJSA-1",
#"Objeto de Contratación": 
#"Servicio",
#"Descripción de Objeto": 
#"SERVICIO DE ALQUILER DE CAMIONETA"
#},
#{
#"Nombre o Sigla de la Entidad": 
#"UNIDAD DE GESTIÓN DE APOYO AL DESARROLLO SOSTENIBLE DEL VRAEM",
#"Fecha y Hora de Publicacion": 
#"11/08/2025 21:10",
#"Nomenclatura": 
#"CP-ABR-2-2025-DEVIDA-UE006/OC-1",
#"Objeto de Contratación": 
#"Servicio",
#"Descripción de Objeto": 
#"CONTRATACION DE SERVICIO DE ALQUILER DE VEHICULOS (CAMIONETAS) EN LA ZONA CENTRO- SUR Y NORTE PARA LAS DISTINTAS ACTIVIDADES DE LA UE006-DEVIDA-VRAEM."
#}
#]
##read_seace({"keyword":"alquiler"},["caminoneta"])
#print(get_url_for_items(data) )

