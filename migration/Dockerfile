FROM python:latest

COPY . /app

WORKDIR /app

RUN pip install python-dotenv mysqlclient

ENTRYPOINT [ "python" ]

CMD ["migrate.py"]