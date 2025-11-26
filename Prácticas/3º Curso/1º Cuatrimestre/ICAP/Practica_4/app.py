from flask import Flask
from ec2_metadata import ec2_metadata

app = Flask(__name__)


@app.route("/")
def home():
    # Inicializamos variables por defecto para evitar errores de "variable no definida"
    iid = "No disponible (Error/Local)"
    az = "No disponible"
    ipv4 = "No disponible"
    subnet = "No disponible"

    try:
        iid = ec2_metadata.instance_id
        az = ec2_metadata.availability_zone
        ipv4 = ec2_metadata.private_ipv4
        mac = ec2_metadata.mac
        subnet = ec2_metadata.network_interfaces[mac].subnet_id
    except Exception as e:
            # Si falla algo, mantenemos los valores por defecto y mostramos error en consola
            print(f"Error obteniendo metadatos: {e}")
            iid = "Error Metadatos"
            
    # HTML con el formato solicitado
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>ICAP: Instancia contenedor de Práctica 4</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }}
        .highlight {{
            color: red;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h2>ICAP: Instancia contenedor de Práctica 4</h2>
    <p><span class="highlight">Francisco Javier Mercader Martínez</span></p>

    <h3>Id de instancia:</h3>
    <p><span class="highlight">{iid}</span></p>

    <h3>Zona de disponibilidad:</h3>
    <p><span class="highlight">{az}</span></p>

    <h3>Dirección IPv4 privada:</h3>
    <p><span class="highlight">{ipv4}</span></p>

    <h3>Id de subred:</h3>
    <p><span class="highlight">{subnet}</span></p>
</body>
</html>
    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
