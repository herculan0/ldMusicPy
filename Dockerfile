FROM python:3
LABEL Author="Herculano"
LABEL Email="lucasgherculano@gmail.com"
LABEL version="0.0.1a"

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV FLASK_APP "backend/app.py"
#ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

RUN mkdir /usr/src/app

WORKDIR /usr/src/app

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
