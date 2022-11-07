import asyncio
import json
import sys
from asyncio import StreamReader, StreamWriter
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

# logger.info('Incoming data: %s', message)

async def client_connected(reader: StreamReader, writer: StreamWriter):
    # address = writer.get_extra_info('peername')

    while True:
        data = await reader.read(1024)
        print(data)
        message = json.loads(data.decode())
        if not message:
            break
        message_for_client = {'test': 'test'}
        data_for_client = json.dumps(message_for_client).encode()
        writer.write(data_for_client)
        await writer.drain()
    writer.close()


async def server(host: str = "127.0.0.1", port: int = 8000):
    srv = await asyncio.start_server(
        client_connected, host, port)

    async with srv:
        await srv.serve_forever()

asyncio.run(server())

