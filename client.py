import asyncio
import json

import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


async def client(message: str = None, user: str = "Anonymous", renew: bool = False, to_user: str = None):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8000)

    query = {'user': user,
             'renew': renew,
             'message': message,
             'to_user': to_user}
    data_for_client = json.dumps(query).encode()
    writer.write(data_for_client)
    data = await reader.read(9999)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

    messages = json.loads(data.decode())
    for _, _user, _message, _to_user in messages:
        if _to_user:
            logger.info('%s -> %s: %s', _user, _to_user, _message)
        else:
            logger.info('%s: %s', _user, _message)

asyncio.run(client(user="Agent Smith", renew=True))
asyncio.run(client(user="Agent Smith", message="Do you hear that, Mr. Anderson?"))
asyncio.run(client(user="Agent Smith", message="That is the sound of inevitability."))
asyncio.run(client(user="Agent Smith", message="That is the sound of your death."))
asyncio.run(client(user="Agent Smith", message="Goodbye, Mr. Anderson."))
asyncio.run(client(user="Agent Smith", message="pssss...", to_user="Neo"))

