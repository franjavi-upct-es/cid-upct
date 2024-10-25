import requests
import matplotlib.pyplot as plt
import pandas as pd

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

    # Procesar los datos para la gráfica
    dates = []
    temperatures = []
    for forecast in weather_data['list']:
        dates.append(forecast['dt_txt'])
        temperatures.append(forecast['main']['temp'])

    # Imprime los datos en la consola
    print(f"Temperaturas para los próximos 5 días en {city_name}:")
    for date, temp in zip(dates, temperatures):
        print(f"{date}: {temp} ºC")

    # Convertir los datos en un DataFrame
    df = pd.DataFrame({'Fecha': pd.to_datetime(dates), 'Temperatura (ºC)': temperatures})

    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(df['Fecha'], df['Temperatura (ºC)'], marker='o', linestyle='-', color='b')

    # Etiquetas y título
    plt.title(f'Temperaturas para los próximos 5 días en {city_name}')
    plt.xlabel('Fecha')
    plt.ylabel('Temperatura (ºC)')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Mostrar la gráfica
    plt.tight_layout()
    plt.show()
if __name__ == '__main__':
    main()