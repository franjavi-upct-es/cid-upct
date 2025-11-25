from flask import Flask
from ec2_metadata import ec2_metadata

app = Flask(__name__)


@app.route("/")
def home():
    # Obtener metadatos de la instancia EC2
    instance_id = ec2_metadata.instance_id
    availability_zone = ec2_metadata.availability_zone
    private_ipv4 = ec2_metadata.private_ipv4
    subnet_id = ec2_metadata.subnet_id

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
                <span class="value">{instance_id}</span>
            </div>
            
            <div class="info-item">
                <span class="label">Zona de disponibilidad:</span><br>
                <span class="value">{availability_zone}</span>
            </div>
            
            <div class="info-item">
                <span class="label">Dirección IPv4 privada:</span><br>
                <span class="value">{private_ipv4}</span>
            </div>
            
            <div class="info-item">
                <span class="label">Id de subred:</span><br>
                <span class="value">{subnet_id}</span>
            </div>
        </div>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
