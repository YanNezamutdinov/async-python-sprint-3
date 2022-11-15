import asyncio
import json
import sys
import uuid
from asyncio import StreamReader, StreamWriter
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

# logger.info('Incoming data: %s', message)

GLOBAL_CHAT = str(uuid.uuid4())

open("chats.json", 'w')
open("last_read_message.json", 'w')
# open("chat_users.json", 'w')

with open("chat_users.json", 'w') as f:
    _dict = {GLOBAL_CHAT: "global"}
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
                    last_read_message = json.load(f)
                    message_ids = [(chat_name, message_id) for chat_name, message_id in last_read_message.get(_user)]
                except ValueError:
                    message_ids = dict()

            with open("chats.json", 'r') as f:
                try:
                    chats = json.load(f)
                    if message_ids:
                        for chat_name, message_id in message_ids:
                            chat = chats.get(chat_name)
                            index_last_message = [index for index, item in enumerate(chat) if item[0] == message_id][0]
                            unread_messages = chat[index_last_message+1:]
                            if unread_messages:
                                data_for_client = json.dumps(unread_messages).encode()
                                writer.write(data_for_client)
                                await writer.drain()
                    else:
                        pass

                except ValueError as e:
                    pass

        writer.close()



        # if _last_read_message and not _message:
        #     index_last_message = \
        #     [index for index, item in enumerate(general_chat) if item[0] == _last_read_message][0]
        #     no_read_message = general_chat[index_last_message+1:]
        #     data_for_client = json.dumps(no_read_message).encode()
        #     writer.write(data_for_client)
        #     await writer.drain()
        #
        # elif not _message:
        #     data_for_client = json.dumps(general_chat[-20:]).encode()
        #     writer.write(data_for_client)
        #     await writer.drain()
        #
        # elif not message.get('to_user'):
        #     rec = [str(uuid.uuid4()), _user, _message]
        #     general_chat.append(rec)
        #     data_for_client = json.dumps([rec,]).encode()
        #     writer.write(data_for_client)
        #     await writer.drain()
        #     with open("general_chat.json", 'w') as f:
        #         json.dump(general_chat, f)
        # else:
            # p2p
            # pass


async def server(host: str = "127.0.0.1", port: int = 8000):
    srv = await asyncio.start_server(
        client_connected, host, port)

    async with srv:
        await srv.serve_forever()

asyncio.run(server())

