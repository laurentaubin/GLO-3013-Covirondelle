FROM jjanzic/docker-python3-opencv

RUN apt-get update -y
RUN apt-get -y install tesseract-ocr

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ src

EXPOSE 5555

CMD ["python", "-u", "src/__main__.py", "--local"]