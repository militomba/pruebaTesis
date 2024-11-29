FROM python:3.10

#Vamos a trabajar en esta carpeta con docker
WORKDIR /tesisEstacionamiento

# Instala dependencias de Python
COPY requirements.txt /tesisEstacionamiento/
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos de tu aplicación al workdir
COPY . /tesisEstacionamiento/

# Comando para ejecutar la aplicación
#CMD ["python3", "manage.py", "runserver_plus", "--cert-file", "cert.pem", "--key-file", "key.pem"]
