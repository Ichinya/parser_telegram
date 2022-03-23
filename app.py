import parser_tg
from data.config import POSTGRES_URI

from loader import client, db


async def on_startup():
    await db.set_bind(POSTGRES_URI)

    # await db.gino.drop_all()
    await db.gino.create_all()

    await parser_tg.start()

    await db.pop_bind().close()


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(on_startup())
