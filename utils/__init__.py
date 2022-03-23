import os

from data.config import BUCKET
from loader import timeweb_s3


def basename(pathfile):
    pathname, extension = os.path.splitext(pathfile)
    filename = pathname.split('\\')
    return filename[-1]


def upload_file(file: str, key: str) -> bool:
    try:
        timeweb_s3.upload_file(Filename=file, Bucket=BUCKET['Name'], Key=key)
        return True
    except Exception as ex:
        print(ex)
        print('Не удалось загрузить файл в S3')
        return False
