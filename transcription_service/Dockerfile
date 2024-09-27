# Usa la imagen base de Python 3.9 slim
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias de sistema, incluyendo ffmpeg y librerías necesarias
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 git && rm -rf /var/lib/apt/lists/*

# Instala Whisper directamente desde el repositorio de GitHub
RUN pip install git+https://github.com/openai/whisper.git

# Copia el archivo de requisitos y las dependencias de Python (si tienes más)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto que va a utilizar la aplicación Flask
EXPOSE 5001

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
