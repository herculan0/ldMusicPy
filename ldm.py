from app import create_app
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.envrc.prod')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


if __name__ == "__main__ ":
    app = create_app(os.getenv('APP_SETTINGS'))
    app.run()
