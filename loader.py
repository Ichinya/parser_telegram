import boto3
from gino import Gino
from telethon.sync import TelegramClient
from botocore.client import Config

from data import config

client = TelegramClient(config.USER, config.API_ID, config.API_HASH)
client.start()

db = Gino()

timeweb_s3 = boto3.client(
    's3',
    endpoint_url='https://s3.timeweb.com',
    region_name='ru-1',
    aws_access_key_id=config.AWS_ACCESS_KEY,
    aws_secret_access_key=config.AWS_SECRET_KEY,
    config=Config(s3={'addressing_style': 'path'})
)

__all__ = ["client", "db", "timeweb_s3"]
