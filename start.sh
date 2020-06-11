sudo systemctl start docker && sudo docker-compose up -d &&
source ./.envrc && source ./venv/bin/activate
flask run
