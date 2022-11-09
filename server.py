import asyncio
import json
import sys
import uuid
from asyncio import StreamReader, StreamWriter
import logging
from pprint import pprint

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

# logger.info('Incoming data: %s', message)
open("general_chat.json", 'w+')
with open("general_chat.json", 'r') as f:
    try:
        general_chat = json.load(f)
    except ValueError:
        general_chat = list()


async def client_connected(reader: StreamReader, writer: StreamWriter):
    # address = writer.get_extra_info('peername')

    while True:
        data = await reader.read(1024)
        if not data:
            break

        message = json.loads(data.decode())
        if not message.get('message'):
            data_for_client = json.dumps(general_chat).encode()
            writer.write(data_for_client)
            await writer.drain()
        elif not message.get('to_user'):
            rec = [str(uuid.uuid4()), message.get('user'), message.get('message')]
            # record = {str(uuid.uuid4()): {'user': message.get('user'), 'message': message.get('message')}}
            general_chat.append(rec)
            data_for_client = json.dumps([].append(rec)).encode()
            writer.write(data_for_client)
            await writer.drain()
            with open("general_chat.json", 'w') as f:
                json.dump(general_chat, f)
        else:
            # p2p
            pass
    writer.close()


async def server(host: str = "127.0.0.1", port: int = 8000):
    srv = await asyncio.start_server(
        client_connected, host, port)

    async with srv:
        await srv.serve_forever()

asyncio.run(server())

