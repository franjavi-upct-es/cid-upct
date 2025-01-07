# Usa la imagen base de Oracle XE
FROM esanguin/oraclexe:latest

# Exponer los puertos necesarios
EXPOSE 1521 8080

# Comando para iniciar la base de datos al iniciar el contenedor
CMD ["/bin/bash", "-c", "/entrypoint.sh"]
