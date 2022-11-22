import asyncio
import json
import sys
import uuid
from asyncio import StreamReader, StreamWriter
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


with open("chats.json", 'w') as f:
    _dict = list()
    json.dump(_dict, f)


with open("last_read_message.json", 'w') as f:
    _dict = dict()
    json.dump(_dict, f)


async def client_connected(reader: StreamReader, writer: StreamWriter):

    while True:
        data = await reader.read(1024)
        if not data:
            break

        message = json.loads(data.decode())
        _user, _renew, _message, _to_user = message.values()

        if _renew:
            with open("last_read_message.json", 'r') as f:
                try:
                    last_read_messages = json.load(f)
                    message_id = last_read_messages.get(_user)
                except AttributeError:
                    message_id = None

            with open("chats.json", 'r') as f:
                chat = json.load(f)
                if message_id:
                    index_last_read_message = [index for index, val in enumerate(chat) if val[0] == message_id][0]
                    unread_messages = chat[index_last_read_message+1:]
                else:
                    unread_messages = chat[-20:]

                unread_messages = [item for item in unread_messages if not item[3] or item[3] == _user]

                with open("last_read_message.json", 'r') as f:
                    last_read_messages = json.load(f)
                try:
                    last_read_messages.update({_user: unread_messages[-1][0]})
                except IndexError:
                    unread_messages = [["", "Admin", "No new messages", ""], ]

                with open("last_read_message.json", 'w') as f:
                    json.dump(last_read_messages, f)

                data_for_client = json.dumps(unread_messages).encode()
                writer.write(data_for_client)
                await writer.drain()

        else:
            data = [str(uuid.uuid4()), _user, _message, _to_user]
            data_for_client = json.dumps([data, ]).encode()
            writer.write(data_for_client)
            await writer.drain()

            with open("chats.json", 'r') as f:
                chat = json.load(f)

            chat.append(data)

            with open("chats.json", 'w') as f:
                json.dump(chat, f)

            with open("last_read_message.json", 'r') as f:
                last_read_messages = json.load(f)

            last_read_messages.update({_user: data[0]})

            with open("last_read_message.json", 'w') as f:
                json.dump(last_read_messages, f)

        writer.close()


async def server(host: str = "127.0.0.1", port: int = 8000):
    srv = await asyncio.start_server(
        client_connected, host, port)

    logger.info('Сервер стартанул на %s', srv.sockets[0].getsockname())

    async with srv:
        await srv.serve_forever()

asyncio.run(server())

