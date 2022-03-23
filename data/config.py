import os

from dotenv import load_dotenv

load_dotenv()
IP = os.getenv("IP")

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
USER = os.getenv('USER')
PHONE = os.getenv('PHONE')

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
PGDATABASE = str(os.getenv("PGDATABASE"))

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{IP}/{PGDATABASE}"

BUCKET = {'Name': str(os.getenv("BUCKET"))}
AWS_ACCESS_KEY = str(os.getenv("AWS_ACCESS_KEY"))
AWS_SECRET_KEY = str(os.getenv("AWS_SECRET_KEY"))
