from python:3.8-slim


env PYTHONDONTWRITEBYTECODE 1
env PYTHONUNBUFFERED 1

run mkdir /usr/src/app
workdir /usr/src/app
copy . ./

run apt-get update && apt-get upgrade -y
run apt-get install python-psycopg2 apt-utils libpq-dev python3-dev -y
run rm -rf /var/lib/apt/lists/*
run pip install --upgrade pip

run pip install --no-cache-dir -r requirements.txt

expose 5000
