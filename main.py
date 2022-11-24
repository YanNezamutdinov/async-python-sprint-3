import json
import logging
import sys
import asyncio
import uuid
from asyncio.streams import StreamReader, StreamWriter

import aiofiles

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


def files_init():
    with open("last_read_message.json", 'w') as f:
        _dict = dict()
        json.dump(_dict, f)

    with open("chats.json", 'w') as f:
        _dict = list()
        json.dump(_dict, f)


async def get_last_message_id(user: str) -> str:
    async with aiofiles.open("last_read_message.json", 'r') as f:
        contents = await f.read()
    try:
        last_read_messages = json.loads(contents)
        message_id = last_read_messages.get(user)
    except AttributeError:
        message_id = None
    return message_id


async def post_last_message_id(user: str, uuid: str):
    async with aiofiles.open("last_read_message.json", 'r') as f:
        contents = await f.read()
    last_read_messages = json.loads(contents)
    last_read_messages.update({user: uuid})
    async with aiofiles.open("last_read_message.json", 'w') as f:
        await f.write(json.dumps(last_read_messages))


async def get_messages(user: str) -> list:
    try:
        async with aiofiles.open("chats.json", 'r') as f:
            contents = await f.read()
        chat = json.loads(contents)
        message_id = await get_last_message_id(user)
        if message_id:
            index_last_read_message = [index for index, val in enumerate(chat) if val[0] == message_id][0]
            unread_raw_messages = chat[index_last_read_message + 1:]
        else:
            unread_raw_messages = chat[-20:]

        unread_messages = [item for item in unread_raw_messages if not item[3] or item[3] == user]
        await post_last_message_id(user, unread_messages[-1][0])

        return unread_messages
    except IndexError:
        return [["", "Admin", "No new messages", ""], ]


async def post_message(user: str, user_data: str, to_user: str) -> list:
    message = [str(uuid.uuid4()), user, user_data, to_user]
    async with aiofiles.open("chats.json", 'r') as f:
        contents = await f.read()
    chat = json.loads(contents)
    chat.append(message)
    async with aiofiles.open("chats.json", 'w') as f:
        await f.write(json.dumps(chat))
    await post_last_message_id(user, message[0])
    return message


class Connected:

    async def renew(self, user: str, writer: StreamWriter):
        messages = await get_messages(user)
        data_for_client = json.dumps(messages).encode()
        writer.write(data_for_client)
        await writer.drain()
        writer.close()

    async def receive_post(self, user: str, user_data: str|bytes, to_user: str, writer: StreamWriter):
        message = await post_message(user, user_data, to_user)
        data_for_client = json.dumps([message, ]).encode()
        writer.write(data_for_client)
        await writer.drain()
        writer.close()


async def client_connected(reader: StreamReader, writer: StreamWriter):

    while True:
        data = await reader.read(1024)
        if not data:
            break

        message = json.loads(data.decode())
        user, renew, user_data, to_user = message.values()
        conn = Connected()

        if renew:
            await conn.renew(user, writer)
        else:
            await conn.receive_post(user, user_data, to_user, writer)


async def main(host: str, port: int):

    files_init()

    srv = await asyncio.start_server(
        client_connected, host, port)

    logger.info('Сервер стартанул на %s', srv.sockets[0].getsockname())

    async with srv:
        await srv.serve_forever()


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 8000))
