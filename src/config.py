from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


DEBUG = False
API_ROOT = getenv('API_ROOT', 'skillsuite')
API_VERSION = getenv('API_VERSION', '1.0')
SQLALCHEMY_TRACK_MODIFICATIONS = False
RESTPLUS_MASK_HEADER = False
SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
