FROM amd64/python:3.7-slim-buster

RUN mkdir /service
WORKDIR /service

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main.py /service/main.py
COPY dynamic-config/ /service/dynamic-config/
COPY lib/ /service/lib/

CMD ["python3", "-u", "./main.py" ]
