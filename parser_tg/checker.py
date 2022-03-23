import os

from utils import upload_file
from utils.db_api.models import TgMedia


async def check_media():
    db_media = await TgMedia.query.where(TgMedia.storage is None).gino.all()

    for media in db_media:
        if media.storage:
            continue
        is_upload = upload_file(media.file, media.file.replace('\\', '/'))
        if is_upload:
            await media.update(storage=True).apply()
            os.remove(media.file)
