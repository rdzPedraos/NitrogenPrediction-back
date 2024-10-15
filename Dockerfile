# Usa la imagen base oficial de Python
FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos (si existen)
COPY requirements .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements

# Copia tu código Flask al contenedor
COPY . .

# Expone el puerto 5000
EXPOSE 5000

CMD ["python", "src/main.py"]
