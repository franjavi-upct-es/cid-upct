#!/bin/bash

# === CONFIGURACIÓN ===
KEY_NAME="Entregable-Prac4"
KEY_FILE="./${KEY_NAME}.pem"
STACK_NAME="stack-entregable-prac4"
REGION="us-east-1"
# =====================

# 1. Aseguramos permisos de clave
chmod 400 "$KEY_FILE"

echo ">>> [1/4] Recuperando configuración de la infraestructura..."
# Obtenemos las variables necesarias consultando al Stack ya creado
INSTANCE_IP=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=DockerInstance" "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].PublicIpAddress" --output text --region $REGION)
REPO_URI=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='RepositoryUri'].OutputValue" --output text --region $REGION)
CLUSTER_NAME=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='ClusterName'].OutputValue" --output text --region $REGION)
ALB_DNS=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='ALBDNS'].OutputValue" --output text --region $REGION)

echo "    Builder IP: $INSTANCE_IP"
echo "    Repo URI: $REPO_URI"
echo "    Cluster: $CLUSTER_NAME"

echo ">>> [2/4] Parcheando app.py y actualizando imagen..."
# Conectamos por SSH para sobrescribir app.py y reconstruir
ssh -o StrictHostKeyChecking=no -i "$KEY_FILE" ec2-user@$INSTANCE_IP <<EOF
  set -e
  cd /home/ec2-user/icap-practica4
  
  # --- CORRECCIÓN DEL CÓDIGO ---
  # Sobrescribimos app.py con una versión corregida.
  # El error probable era usar la variable 'z' en el try y 'az' en el except.
  cat <<PY > app.py
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
        z = ec2_metadata.availability_zone
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
                <span class="value">{z}</span>
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
PY

  echo ">> Reconstruyendo imagen (Docker Build)..."
  sudo docker build -t icap-practica4 .
  
  echo ">> Subiendo imagen corregida (Docker Push)..."
  aws ecr get-login-password --region $REGION | sudo docker login --username AWS --password-stdin $REPO_URI
  sudo docker push $REPO_URI:latest
EOF

echo ">>> [3/4] Forzando despliegue en ECS (Rolling Update)..."
# Este comando fuerza a ECS a bajar la nueva imagen y reemplazar los contenedores
aws ecs update-service \
    --cluster $CLUSTER_NAME \
    --service icap-service \
    --force-new-deployment \
    --region $REGION > /dev/null

echo "=========================================================="
echo ">>> [4/4] ¡ACTUALIZACIÓN LANZADA! <<<"
echo "ECS está reemplazando los contenedores ahora mismo."
echo "Espera unos 2-3 minutos y recarga esta URL:"
echo "http://$ALB_DNS"
echo "=========================================================="