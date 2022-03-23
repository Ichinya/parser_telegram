from loader import db
from parser_tg import parse_msg, message, checker, channel
from utils.db_api.models import ParseChannel


async def start():
    await checker.check_media()
    try:
        channels = await ParseChannel.query.gino.all()
        for ch in channels:
            if ch.channel_id is None:
                channel_info = await channel.full_info(ch.channel_input)
                channel_id = channel_info.__dict__.get('full_chat').__dict__.get('id')
                await ch.update(channel_id=channel_id).apply()
    except Exception as ex:
        print(ex)
        exit()

    channels = await ParseChannel.query.gino.all()
    for ch in channels:
        print(ch.name)
        if ch.last_max_id is None or ch.last_max_id < 0:
            max_msg_id = 0
        else:
            max_msg_id = ch.last_max_id

        msgs = await parse_msg.request_msg(ch.channel_id, min_id=ch.last_max_id)
        for msg in msgs:
            if max_msg_id < msg.id:
                max_msg_id = msg.id

            await message.create_model(msg)

        print(max_msg_id)
        if max_msg_id != ch.last_max_id:
            await ch.update(last_max_id=max_msg_id, dt=db.func.now()).apply()


__all__ = ['start']
