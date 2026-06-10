# immagine base da cui partire 
FROM python:3.10-alpine

# cartella di lavoro dentro il container
WORKDIR /app

# copia il file dentro al container
COPY app.py .

# installa flask
RUN pip install flask 

CMD ["python3", "app.py"]