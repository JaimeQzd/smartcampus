#usamos una imagen ofical de Python
FROM python:3.12-slim


#definimos la carpeta de trabajo
WORKDIR /app


#evitamos que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


#copiamos primero requirements
COPY requirements.txt .


#instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt


#copiamos el resto de archivos
COPY . .


#indicamos que la aplicacion utiliza el puerto 8000
EXPOSE 8000


#ejecutamos FastAPI mediante Uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}"]