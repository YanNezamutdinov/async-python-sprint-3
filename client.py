import asyncio
import json


async def client(message: str, user: str = "Anonymous"):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8000)
    query = {'user': user,
             'message': message}

    # print(f'Send: {message!r}')
    writer.write(json.dumps(query).encode())
    await writer.drain()

    data = await reader.read(100)
    # print(f'Received: {data.decode()!r}')

    # print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(client("Say HI!"))



# class Client:
#     def __init__(self, server_host="127.0.0.1", server_port=8000):
#         pass
#
#     def send(self, message=""):
#         pass