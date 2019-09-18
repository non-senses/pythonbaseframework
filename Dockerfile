FROM python:3.7-stretch as base
ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt


CMD ["make","startdev"]
