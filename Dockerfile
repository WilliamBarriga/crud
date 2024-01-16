FROM python:3.11

RUN apt update && apt install -y gettext

WORKDIR /app

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8001
CMD gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001 --max-requests 100 --access-logfile - --error-logfile - --log-level info