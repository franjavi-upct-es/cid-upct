import requests

# Diccionario predefinido para mapear los nombres de las ciudades
city_codes = {
    "Cartagena" : "Cartagena,es",
    "Murcia": "Murcia, es"
}

def get_weather(city_name):
    api_key = '83de65eb45b2381624501b8d4a320409'
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric"
    headers = {"cache-control": "no-cache"}

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def main():
    city_name = input("Ingrese la ciudad que desea buscar: ")
    city_code = city_codes.get(city_name)

    if not city_code:
        print("Ciudad no encontrada")
        return

    weather_data = get_weather(city_code)
    if not weather_data:
        print("No se pudieron obtener los datos del tiempo.")
        return

    print(f"Temperaturas para los próximos 5 días en {city_name}:")
    for forecast in weather_data['list']:
        date = forecast['dt_txt']
        temp = forecast['main']['temp']
        print(f"{date}: {temp} ºC")

if __name__ == '__main__':
    main()