import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/ciudad")
def get_weather():
    # Obtener el parámetro de la ciudad
    ciudad = request.args.get("q")

    # Asegurarse de que el parámetro de ciudad esté presente
    if not ciudad:
        return "Error: La ciudad no ha sido proporcionada.", 400

    # Clave API de OpenWeather
    api_key = '83de65eb45b2381624501b8d4a320409'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric"

    # Hacer solicitud a la API de OpenWeather
    response = requests.get(url)

    # Verificar si la respuesta fue exitosa
    if response.status_code != 200:
        return f"Error: No se pudo obtener el clima para {ciudad}", response.status_code

    # Convertir la respuesta en JSON
    data = response.json()

    # Verificar si la respuesta contiene la información de temperatura
    if 'main' in data and 'temp' in data['main']:
        temperatura = data["main"]["temp"]
    else:
        return "Error: No se han encontrado datos de temperatura.", 500

    # Formatear la ciudad para que la primera letra sea mayúscula
    ciudad_formato = ciudad.split(',')[0].capitalize()

    # Construir el mensaje con el formato solicitado
    return f"La temperatura actual de {ciudad_formato} es {temperatura} ºC"

if __name__ == '__main__':
    app.run(debug=True)