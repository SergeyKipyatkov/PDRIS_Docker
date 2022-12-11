FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install --upgrade python-dotenv Flask mysqlclient

EXPOSE 8000

ENTRYPOINT [ "python" ]

CMD ["app.py"]