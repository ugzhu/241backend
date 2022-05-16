FROM python:3.9-slim
WORKDIR ~/app
COPY __init__.py .
COPY app.py .
COPY mysql_connector.py .
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY gunicorn_starter.sh .
ENTRYPOINT ["./gunicorn_starter.sh"]