import requests

# Define the correct base URL (note port 5000 instead of 500)
url = "http://localhost:5000"

# Define the endpoints for IP and MD5 services
ip_service = "/ip"
md5_service = "/md5/"

# Define headers
headers = {'cache-control': "no-cache"}

# Make a request to the IP service
ip_response = requests.get(url + ip_service, headers=headers)

# Check if the response from the IP service is successful
if ip_response.status_code == 200:
    datos = ip_response.json()  # Parse the JSON response
    print(f"Mi dirección IP es: {datos['ip']}")
else:
    print(f"Error al obtener la IP: {ip_response.status_code}")

text_to_hash = input("Introduce un texto para el hash MD5: ")

md5_response = requests.get(url + md5_service + text_to_hash, headers=headers)

if md5_response.status_code == 200:
    hash_data = md5_response.json()
    print(f"El hash MD5 de '{text_to_hash}' es: {hash_data['md5']}")
else:
    print(f"Error al obtener el hash MD5: {md5_response.status_code}")
