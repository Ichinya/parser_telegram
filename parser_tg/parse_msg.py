from telethon.tl.functions.messages import GetHistoryRequest

from loader import client


async def request_msg(channel, offset_msg: int = 0, limit_msg: int = 100, total_count_limit=0,
                      min_id=0, max_id=0) -> list:
    """
    Записывает json-файл с информацией о всех сообщениях канала/чата

    :param max_id: максимальный id сообщения:
    :param min_id: Минимальный id сообщения:
    :param channel:  канал:
    :param offset_msg: номер записи, с которой начинается считывание:
    :param limit_msg: максимальное число записей, передаваемых за один раз:
    :param total_count_limit: поменяйте это значение, если вам нужны не все сообщения:
    :return: Массив сообщений
    :rtype: list
    """
    all_messages = []  # список всех сообщений
    if limit_msg > total_count_limit & total_count_limit != 0:
        limit_msg = total_count_limit
    if min_id is None or min_id < 0:
        min_id = 0

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg, offset_date=None, add_offset=0,
            limit=limit_msg, max_id=max_id, min_id=min_id,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message)

        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        print(total_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
    return all_messages
