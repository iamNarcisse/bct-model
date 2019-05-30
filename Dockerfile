FROM python:3.6.8

COPY . /main

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["main.py"]