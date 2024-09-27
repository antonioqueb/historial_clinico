FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpython3-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5004

CMD ["python", "app.py"]
