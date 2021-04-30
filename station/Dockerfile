FROM jjanzic/docker-python3-opencv

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ src
COPY resources/ ressources

EXPOSE 5555

CMD ["python", "-u", "src/__main__.py", "--local"]
