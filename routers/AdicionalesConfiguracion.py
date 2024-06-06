from fastapi import APIRouter, HTTPException
import requests
import os
from return_codes import *
import re

AdicionalesConfiguracion_router = APIRouter()

URL = "https://www.zonapagos.com/Apis_CicloPago/api/InicioPago"
#TOKEN = os.getenv("TOKEN")

@AdicionalesConfiguracion_router.post("/AdicionalesConfiguracion/", tags=['Zonapagos'])
def AdicionalesConfiguracion(int_codigo: int, str_valor: str):
    """
    ## **Descripción:**
    
    ## **Parámetros obligatorios:**
        - int_codigo -> Define la configuración adicional que puede tener el comercio.
        - str_valor -> Configuración adicional enviada por el comercio.

    """
    url = URL
    
    AdicionalesConfiguracion = {
        "int_codigo": int_codigo,
        "str_valor": str_valor,

    }

    response = requests.post(url, data=AdicionalesConfiguracion)
    return {"output": response.json()}  
   