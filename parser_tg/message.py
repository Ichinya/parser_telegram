import os

from telethon.tl.types import Message, WebPageEmpty, MessageMediaUnsupported, MessageMediaPoll

from loader import client
from utils import basename, upload_file
from utils.db_api.models import TgMessage, TgMedia
from slugify import slugify


async def create_model(msg: Message):
    tg_msg = TgMessage(
        id=f"{msg.peer_id.channel_id}.{msg.id}",
        msg_id=msg.id,
        channel_id=msg.peer_id.channel_id,
        date=msg.date.replace(tzinfo=None),
        text=msg.message,
        group_id=msg.grouped_id
    )
    try:
        await tg_msg.create()
    except Exception as ex:
        print(ex)
        # return

    if hasattr(msg, 'media') and msg.media is not None:
        await create_media(msg)

    print(tg_msg)


async def create_media(msg: Message):
    print(msg)
    media = find_media(msg)
    if isinstance(media, (WebPageEmpty, MessageMediaUnsupported, MessageMediaPoll)):
        print('Empty media')
        return
    path = ''
    try:
        path = await client.download_media(msg, 'media\\', progress_callback=callback)
        filename = basename(path)
        new_path = path.replace(filename, slugify(filename))
        if path != new_path:
            os.rename(path, new_path)
            path = new_path

    except Exception as ex:
        print(ex)
        exit('Выход при скачивании файла')

    try:
        tg_media = TgMedia(
            id=media.id,
            channel_id=msg.peer_id.channel_id,
            message_id=f"{msg.peer_id.channel_id}.{msg.id}",
            msg_id=msg.id,
            group_id=msg.grouped_id,
            file=path,
            date=media.date.replace(tzinfo=None)
        )
        await tg_media.create()
        is_upload = upload_file(tg_media.file, tg_media.file.replace('\\', '/'))
        if is_upload:
            await tg_media.update(storage=True).apply()
            os.remove(tg_media.file)
    except Exception as ex:
        print(ex)


def find_media(msg: Message):
    media = msg.media
    print(media)
    if hasattr(media, 'photo') and media.photo is not None:
        media = media.photo
        print('1', media)
    if hasattr(media, 'webpage') and media.webpage is not None:
        media = media.webpage
        print('2', media)
    if hasattr(media, 'document') and media.document is not None:
        media = media.document
        print('3', media)
    if hasattr(media, 'webpage') and media.webpage is not None:
        media = media.webpage
        print('4', media)
    if hasattr(media, 'photo') and media.photo is not None:
        media = media.photo
        print('5', media)
    print(media)
    return media


def callback(current, total):
    print('Downloaded', current, 'out of', total,
          'bytes: {:.2%}'.format(current / total))
