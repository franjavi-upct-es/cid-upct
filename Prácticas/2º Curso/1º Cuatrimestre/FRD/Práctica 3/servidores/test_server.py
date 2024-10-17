import requests

url = "http://localhost:500"

ip_service = "/ip"
md5_service = "md5/"

headers = {'cache-control': "no-cache"}

ip_response = requests.request("GET", url+ip_service, headers=headers)

if ip_response.status_code == 200:
    datos = ip_response.json()
    print(f"Mi dirección IP es: " + datos)
