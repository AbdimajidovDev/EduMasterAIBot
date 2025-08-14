import os

from dotenv import load_dotenv

load_dotenv()


ADMIN_ID = os.getenv('ADMIN_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
BASE_URL = os.getenv('BASE_URL')


