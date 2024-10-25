import requests

url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/30016"

querystring  = {"api_key": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmcmFuY2lzY29qYXZpZXIubWVyY2FkZXJAZWR1LnVwY3QuZXMiLCJqdGkiOiI3MWRmYTgwYy1iZjdhLTQwMmItOTQyZi0zOTI2ZDI0ZjY0ODEiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTcyNzg3ODA4OSwidXNlcklkIjoiNzFkZmE4MGMtYmY3YS00MDJiLTk0MmYtMzkyNmQyNGY2NDgxIiwicm9sZSI6IiJ9.Ikde8UbY3Z6bbohB8YXke6S-q0wzPcyGbp-MYK0ePBE"}

headers = {
        "cache-control": "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

if response.status_code == 200:
	datos = response.json()
	url_datos = datos["datos"]
	response_datos = requests.request("GET", url_datos, headers=headers)
	print(response_datos.text)

else:
	print("Respuesta sin éxito")