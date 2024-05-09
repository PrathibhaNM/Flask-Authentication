from os import environ
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = environ.get('SECRET_KEY')
MONGODB_URL = environ.get('MONGODB_URL')
JWT_SECRET_KEY=environ.get('JWT_SECRET_KEY')
