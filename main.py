import json
import logging
import sys
import asyncio
from asyncio.streams import StreamReader, StreamWriter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


async def get_last_message_id(user: str) -> str:
    async with open("last_read_message.json", 'r') as f:
        try:
            last_read_messages = json.load(f)
            message_id = last_read_messages.get(user)
        except AttributeError:
            message_id = None
    return message_id


async def post_last_message_id(user: str, uuid: str):
    async with open("last_read_message.json", 'r') as f:
        last_read_messages = json.load(f)
    try:
        last_read_messages.update({user: uuid})
    except IndexError:
        unread_messages = [["", "Admin", "No new messages", ""], ]
        return unread_messages



class Connected:
    async def renew(self):
        pass

    async def receive_post(self):
        pass





async def client_connected(reader: StreamReader, writer: StreamWriter):
    address = writer.get_extra_info('peername')
    logger.info('Входящий от %s', address)

    while True:
        data = await reader.read(1024)
        if not data:
            break

        message = json.loads(data.decode())
        user, renew, message, to_user = message.values()



async def main(host: str, port: int):
    srv = await asyncio.start_server(
        client_connected, host, port)

    logger.info('Сервер стартанул на %s', srv.sockets[0].getsockname())

    async with srv:
        await srv.serve_forever()


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 8000))

