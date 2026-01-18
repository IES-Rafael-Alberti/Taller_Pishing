# Usamos una imagen ligera de Python
FROM python:3.9-slim

# Variables de entorno para que Python no buffee la salida
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero el archivo de requisitos
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de los archivos del proyecto
COPY . .

# Exponemos los puertos necesarios (5000 para Flask)
EXPOSE 5000

# Comando por defecto: ejecutar la aplicación Flask
CMD ["python", "app.py"]
