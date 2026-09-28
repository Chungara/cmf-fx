
## Documentacion y terminos de uso API CMF - https://api.cmfchile.cl/terminos-de-uso.html


import requests
import csv
import os
from datetime import datetime
from dotenv import load_dotenv


url = "https://api.cmfchile.cl/api-sbifv3/recursos_api/dolar"
load_dotenv()
apikey=os.getenv("CMF_API_KEY")

## 

parametros = {
    "apikey": apikey,
    "formato": "json"
}



## Formato response, tal como la entrega la CMF
respuesta = requests.get(url, params=parametros, timeout=10)

## Por si la respuesta no es 200, lanzar un error
respuesta.raise_for_status()

## Convertir la respuesta JSON a estructuras de Python
datos = respuesta.json() 



registro = datos["Dolares"][0]

## Extraer valores de la respuesta de la API
valor = registro["Valor"]
valor_num = float(valor.replace(",", "."))

fecha = registro["Fecha"]



timestamp_consulta = datetime.now().isoformat(timespec="seconds")

if not os.path.exists("data/dolar.csv"):
    with open("data/dolar.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["fecha", "valor", "timestamp_consulta"])
        escritor.writerow([fecha, valor_num, timestamp_consulta])

else:
    with open("data/dolar.csv", "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        fechas_existentes = [fila["fecha"] for fila in lector]

    if fecha not in fechas_existentes:
        with open("data/dolar.csv", "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([fecha, valor_num, timestamp_consulta])

        print("Dato agregado")

    else:
        print("La fecha ya existe")



print(fecha, valor)