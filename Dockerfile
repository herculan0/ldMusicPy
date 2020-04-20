FROM python:3.7-alpine
LABEL Author="Herculano"
LABEL Email="lucasgherculano@gmail.com"
LABEL version="0.0.1a"

ENV FLASK_DEBUG=True
ENV FLASK_ENV=development
ENV FLASK_APP=ldm.py

RUN mkdir /usr/src/app

WORKDIR /usr/src/app

COPY . ./

RUN apk update \ 
    apk upgrade \ 
    apk add py-setuptools \
    apk add py-pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "ldm.py"]
