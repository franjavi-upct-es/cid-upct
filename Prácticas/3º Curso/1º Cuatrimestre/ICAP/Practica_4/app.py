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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ICAP - Práctica 4</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                max-width: 800px;
                margin: 0 auto;
            }}
            h1 {{
                color: #333;
                border-bottom: 2px solid #0066cc;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #666;
                font-size: 18px;
                margin-top: 20px;
            }}
            .info-item {{
                margin: 15px 0;
                padding: 10px;
                background-color: #f9f9f9;
                border-left: 4px solid #0066cc;
            }}
            .label {{
                font-weight: bold;
                color: #333;
            }}
            .value {{
                color: #0066cc;
                font-family: monospace;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ICAP: Instancia contenedor de Práctica 4</h1>
            <h2>Francisco Javier Mercader Martínez</h2>
            
            <div class="info-item">
                <span class="label">Id de instancia:</span><br>
                <span class="value">{iid}</span>
            </div>
            
            <div class="info-item">
                <span class="label">Zona de disponibilidad:</span><br>
                <span class="value">{az}</span>
            </div>
            
            <div class="info-item">
                <span class="label">Dirección IPv4 privada:</span><br>
                <span class="value">{ipv4}</span>
            </div>
            
            <div class="info-item">
                <span class="label">Id de subred:</span><br>
                <span class="value">{subnet}</span>
            </div>
        </div>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
