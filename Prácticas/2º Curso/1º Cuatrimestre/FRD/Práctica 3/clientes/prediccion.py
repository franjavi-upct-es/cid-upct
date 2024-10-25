import requests

# Diccionario predefinido para mapear los nombres de las cuidades
city_codes = {
    "Cartagena": "30016",
    "Murcia": "30030",
}

def get_weather_data(city_code):
    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{city_code}"
    querystring = {
        "api_key": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmcmFuY2lzY29qYXZpZXIubWVyY2FkZXJAZWR1LnVwY3QuZXMiLCJqdGkiOiI3MWRmYTgwYy1iZjdhLTQwMmItOTQyZi0zOTI2ZDI0ZjY0ODEiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTcyNzg3ODA4OSwidXNlcklkIjoiNzFkZmE4MGMtYmY3YS00MDJiLTk0MmYtMzkyNmQyNGY2NDgxIiwicm9sZSI6IiJ9.Ikde8UbY3Z6bbohB8YXke6S-q0wzPcyGbp-MYK0ePBE"}
    headers = {"cache-control": "no-cache"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        datos = response.json()
        url_datos = datos['datos']
        response_datos = requests.request("GET", url_datos, headers=headers)
        if response_datos.status_code == 200:
            return response_datos.json()
    return None

def main():
    city_name = input("Introduce el nombre de la ciudad: ")
    city_code = city_codes.get(city_name)

    if not city_code:
        print("Ciudad no encontrada.")
        return

    weather_data = get_weather_data(city_code)
    if not weather_data:
        print("No se pudo obtener los datos del tiempo.")

    """
    Asumiendo que la estructura de los datos siempre está en formato JSON,
    se ajustan las claves según la esctructura que tenemos de momento.
    """
    current_weather = weather_data[0]['prediccion']['dia'][0]
    temperature = current_weather['temperatura']["dato"][1]["value"]
    thermal_sensation = current_weather['sensTermica']["dato"][1]["value"]
    humidity = current_weather["humedadRelativa"]["dato"][1]["value"]

    print(f"La temperatura actual es: {temperature} ºC")
    print(f"La sensación térmica es: {thermal_sensation} ºC")
    print(f"La humedad relativa es: {humidity} %")

if __name__ == '__main__':
    main()
