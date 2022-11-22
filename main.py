import logging
import sys
import asyncio
from asyncio.streams import StreamReader, StreamWriter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


async def client_connected(reader: StreamReader, writer: StreamWriter):
    address = writer.get_extra_info('peername')
    logger.info('Входящий от %s', address)

    # while True:
    #     data = await reader.read(1024)
    #     # print(data)
    #     if not data:
    #         break
    #     print(writer.get_extra_info())
    #     writer.write(data)
    #     await writer.drain()
    #
    # # logger.info('Stop serving %s', address)
    # writer.close()


async def main(host: str, port: int):
    srv = await asyncio.start_server(
        client_connected, host, port)

    logger.info('Сервер стартанул на %s', srv.sockets[0].getsockname())

    async with srv:
        await srv.serve_forever()


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 8000))

