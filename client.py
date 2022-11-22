import asyncio
import json

import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


async def get_conn(host, port):
    reader, writer = await asyncio.open_connection(host, port)

    class Conn:

        async def send_data(self, message: str = None, user: str = "Anonymous", renew: bool = False, to_user: str = None):
            query = {'user': user,
                     'renew': renew,
                     'message': message,
                     'to_user': to_user}
            data_for_client = json.dumps(query).encode()
            writer.write(data_for_client)
            data = await reader.readline()
            await writer.drain()

            messages = json.loads(data.decode())
            for _, user, message, to_user in messages:
                if to_user:
                    logger.info('%s -> %s: %s', user, to_user, message)
                else:
                    logger.info('%s: %s', user, message)

        async def close(self):
            writer.close()

    return Conn()


class Client:

    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        self.host = host
        self.port = port

    async def __aenter__(self):
        self.conn = await get_conn(self.host, self.port)
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()


async def main():

    agent_smith_tasks = [
        {'user': "Agent Smith", 'renew': True},
        {'user': "Agent Smith", 'message': "Do you hear that, Mr. Anderson?"},
        {'user': "Agent Smith", 'message': "That is the sound of inevitability."},
        {'user': "Agent Smith", 'message': "That is the sound of your death."},
        {'user': "Agent Smith", 'message': "Goodbye, Mr. Anderson."},
        {'user': "Agent Smith", 'message': "pssss...", 'to_user': "Neo"},
    ]

    neo_tasks = [
        {'user': "Neo", 'renew': True},
        {'user': "Neo", 'message': "My name is Neo."}
    ]

    logger.info('\nЧат злобного агента Смита \n')

    for query in agent_smith_tasks:
        async with Client('127.0.0.1', 8000) as conn:
            await asyncio.create_task(conn.send_data(**query))

    logger.info('\nЧат богоподобного Нео \n')

    for query in neo_tasks:
        async with Client('127.0.0.1', 8000) as conn:
            await asyncio.create_task(conn.send_data(**query))


asyncio.run(main())

