import asyncio
import json


async def client(message: str = None, user: str = "Anonymous", renew: bool = False, to_user: str = None):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8000)

    query = {'user': user,
             'renew': renew,
             'message': message,
             'to_user': to_user}
    data_for_client = json.dumps(query).encode()
    writer.write(data_for_client)
    await writer.drain()
    writer.close()
    # await writer.wait_closed()

    data = await reader.read(9999)
    message = json.loads(data.decode())
    print(message)

asyncio.run(client(user="Agent Smith", renew=True))
# asyncio.run(client(message="Do you hear that, Mr. Anderson?", user="Agent Smith"))
# asyncio.run(client(message="That is the sound of inevitability.", user="Agent Smith"))
# asyncio.run(client(message="That is the sound of your death.", user="Agent Smith"))
# asyncio.run(client(message="Goodbye, Mr. Anderson.", user="Agent Smith"))
# asyncio.run(client(user="Agent Smith"))
# asyncio.run(client(user="Agent Smith"))
# asyncio.run(client(user="Neo"))
# asyncio.run(client(message="My name is Neo.", user="Neo"))





# class Client:
#     def __init__(self, server_host="127.0.0.1", server_port=8000):
#         pass
#
#     def send(self, message=""):
#         pass