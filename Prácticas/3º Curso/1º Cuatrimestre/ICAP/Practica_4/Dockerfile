# Usamos una imagen base ligera de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos de requisitos y la aplicación
COPY requirements.txt .
COPY app.py .

# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto 5000 (puerto de Flask)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]