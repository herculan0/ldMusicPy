FROM python:3.8-slim
LABEL Author="Herculano,Diovane,Marconi"
LABEL Email="lucasgherculano@gmail.com"
LABEL version="0.0.1a"

ENV FLASK_ENV prod
ENV FLASK_APP ldm.py

ENV DEBIAN_FRONTEND=noninteractive

RUN adduser -D ldmusic

WORKDIR /home/ldmusic

COPY requirements requirements
RUN python -m venv venv

COPY app app
COPY migrations migrations
COPY ldm.py config.py boot.sh ./

RUN echo "Installing Apt-get packages..." \
    && apt-get update \
    && apt-get install -y apt-utils 2> /dev/null \
    && apt-get install -y wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN venv/bin/pip install --no-cache-dir -r requirements/docker.txt

ENV DEBIAN_FRONTEND=teletype

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
