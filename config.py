import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
password = os.getenv("PASSWORD")
session_name = os.getenv("SESSION_NAME")

# Logging configuration
LOGGING_LEVEL = 'INFO'
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
