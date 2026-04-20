FROM python:3.9

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todo el proyecto al contenedor
COPY . /app

# Exponer puerto del servidor
EXPOSE 8080

# Lanzar el servidor web
CMD ["python3", "/app/webRD_python.py", "-ip", "0.0.0.0", "-p", "8080", "-f", "/app/files"]