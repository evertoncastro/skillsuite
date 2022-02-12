from os import getenv
from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path=".env")


DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
RESTPLUS_MASK_HEADER = False
SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
