#!/bin/bash

# === CONFIGURACIÓN ===
KEY_NAME="Entregable-Prac4"
KEY_FILE="./${KEY_NAME}.pem"
STACK_NAME="stack-entregable-prac4"
REGION="us-east-1"
# =====================

# 1. Asegurar permisos del .pem
if [ -f "$KEY_FILE" ]; then
    echo ">>> Ajustando permisos de la clave privada a 400..."
    chmod 400 "$KEY_FILE"
else
    echo "ERROR: No encuentro el archivo $KEY_FILE"
    exit 1
fi

echo ">>> [1/7] Lanzando Infraestructura (VPC, ALB, Cluster EC2, ECR)..."
# Intentamos crear el stack. Si ya existe, avisamos pero no paramos si es un re-run manual controlado,
# aunque lo ideal es borrar antes si se quiere limpieza total.
aws cloudformation create-stack \
  --stack-name $STACK_NAME \
  --template-body file://plantilla-infraestructura.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=$KEY_NAME \
  --capabilities CAPABILITY_IAM \
  --region $REGION

# Si falla porque ya existe, lo ignoramos para permitir re-ejecución del script en las fases siguientes
if [ $? -ne 0 ]; then
  echo "AVISO: El stack ya existe o hubo un error. Intentando continuar..."
else
  echo ">>> Esperando creación de stack (esto tarda unos 4-5 mins)..."
  aws cloudformation wait stack-create-complete --stack-name $STACK_NAME --region $REGION
fi

# Obtener Outputs
echo ">>> [2/7] Obteniendo datos de la infraestructura..."
TG_ARN=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='TargetGroupArn'].OutputValue" --output text --region $REGION)
REPO_URI=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='RepositoryUri'].OutputValue" --output text --region $REGION)
CLUSTER_NAME=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='ClusterName'].OutputValue" --output text --region $REGION)
ALB_DNS=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='ALBDNS'].OutputValue" --output text --region $REGION)

# Instancia y Cuenta
INSTANCE_IP=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=DockerInstance" "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].PublicIpAddress" --output text --region $REGION)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "    ALB DNS: $ALB_DNS"
echo "    Repo URI: $REPO_URI"
echo "    Builder IP: $INSTANCE_IP"

echo ">>> [3/7] Pausa técnica (10s)..."
sleep 10

echo ">>> [4/7] Construyendo y Subiendo Docker (vía SSH)..."
ssh -o StrictHostKeyChecking=no -i "$KEY_FILE" ec2-user@$INSTANCE_IP <<EOF
  set -e
  # Verificamos si el directorio existe
  if [ ! -d "/home/ec2-user/icap-practica4" ]; then
     echo "Directorio no encontrado. Creándolo..."
     mkdir -p /home/ec2-user/icap-practica4
     cd /home/ec2-user/icap-practica4
     # Descarga de emergencia
     wget https://raw.githubusercontent.com/franjavi-upct-es/cid-upct/refs/heads/main/Pr%C3%A1cticas/3%C2%BA%20Curso/1%C2%BA%20Cuatrimestre/ICAP/Practica_4/app.py -O app.py
     wget https://raw.githubusercontent.com/franjavi-upct-es/cid-upct/refs/heads/main/Pr%C3%A1cticas/3%C2%BA%20Curso/1%C2%BA%20Cuatrimestre/ICAP/Practica_4/Dockerfile -O Dockerfile
     wget https://raw.githubusercontent.com/franjavi-upct-es/cid-upct/refs/heads/main/Pr%C3%A1cticas/3%C2%BA%20Curso/1%C2%BA%20Cuatrimestre/ICAP/Practica_4/requirements.txt -O requirements.txt
  else
     cd /home/ec2-user/icap-practica4
  fi
  
  echo ">> Construyendo imagen..."
  sudo docker build -t icap-practica4 .
  
  echo ">> Login ECR..."
  aws ecr get-login-password --region $REGION | sudo docker login --username AWS --password-stdin $REPO_URI
  
  echo ">> Tagging y Push..."
  sudo docker tag icap-practica4:latest $REPO_URI:latest
  sudo docker push $REPO_URI:latest
EOF

echo ">>> [5/7] Registrando Definición de Tarea (Task Definition)..."
TASK_DEF_JSON=$(
  cat <<EOF
{
  "family": "icap-task",
  "networkMode": "bridge",
  "containerDefinitions": [
    {
      "name": "icap-container",
      "image": "$REPO_URI:latest",
      "cpu": 256,
      "memory": 256,
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000,
          "protocol": "tcp"
        }
      ],
      "essential": true
    }
  ],
  "requiresCompatibilities": ["EC2"],
  "cpu": "256",
  "memory": "256",
  "executionRoleArn": "arn:aws:iam::$ACCOUNT_ID:role/LabRole"
}
EOF
)

# Registramos la tarea
aws ecs register-task-definition \
  --cli-input-json "$TASK_DEF_JSON" \
  --region $REGION >/dev/null

echo ">>> [6/7] Creando Servicio ECS..."
aws ecs create-service \
  --cluster $CLUSTER_NAME \
  --service-name icap-service \
  --task-definition icap-task \
  --desired-count 4 \
  --launch-type EC2 \
  --load-balancers "targetGroupArn=$TG_ARN,containerName=icap-container,containerPort=5000" \
  --region $REGION >/dev/null

echo "=========================================================="
echo ">>> [7/7] ¡DESPLIEGUE COMPLETADO! <<<"
echo "La aplicación estará disponible en unos minutos en:"
echo "http://$ALB_DNS"
echo "=========================================================="
