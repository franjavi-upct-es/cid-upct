#!/bin/bash

# === CONFIGURACIÓN ===
STACK_NAME="stack-entregable-prac4"
REGION="us-east-1"
# =====================

echo ">>> [1/3] Recuperando configuración..."
CLUSTER_NAME=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='ClusterName'].OutputValue" --output text --region $REGION)
TG_ARN=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='TargetGroupArn'].OutputValue" --output text --region $REGION)
REPO_URI=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='RepositoryUri'].OutputValue" --output text --region $REGION)
ALB_DNS=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='ALBDNS'].OutputValue" --output text --region $REGION)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "    Cluster: $CLUSTER_NAME"

echo ">>> [2/3] Registrando Nueva Tarea con 'networkMode: host'..."
# La clave aquí es "networkMode": "host".
# Esto elimina el aislamiento de red que bloquea los metadatos.
TASK_DEF_JSON=$(
  cat <<EOF
{
  "family": "icap-task",
  "networkMode": "host",
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

aws ecs register-task-definition \
  --cli-input-json "$TASK_DEF_JSON" \
  --region $REGION > /dev/null

echo ">>> [3/3] Actualizando Servicio..."
# Forzamos a ECS a usar la nueva configuración
aws ecs update-service \
  --cluster $CLUSTER_NAME \
  --service icap-service \
  --task-definition icap-task \
  --force-new-deployment \
  --region $REGION > /dev/null

echo "=========================================================="
echo ">>> ¡CAMBIO DE RED APLICADO! <<<"
echo "ECS está reiniciando los contenedores en modo 'Host'."
echo "Espera 2-3 minutos y recarga:"
echo "http://$ALB_DNS"
echo "=========================================================="