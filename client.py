import asyncio
import json


async def client(message: str = None, user: str = "Anonymous", to_user: str = None):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8000)
    with open("last_read_message.json", 'r') as f:
        try:
            _dict = json.load(f)
            last_uuid = _dict.get(user)
        except ValueError:
            _dict = dict()
            last_uuid = None
    query = {'user': user,
             'message': message,
             'last_read_message': last_uuid,
             "to_user": to_user}
    data_for_client = json.dumps(query).encode()
    writer.write(data_for_client)
    await writer.drain()
    data = await reader.read(9999)

    writer.close()
    await writer.wait_closed()

    message = json.loads(data.decode())
    for values in message:
        uuid, name, mes = values
        _dict[name] = uuid
        with open("last_read_message.json", 'w') as f:
            json.dump(_dict, f)
        print(f"name: {name}: {mes}")

asyncio.run(client(user="Agent Smith"))
asyncio.run(client(message="Do you hear that, Mr. Anderson?", user="Agent Smith"))
asyncio.run(client(message="That is the sound of inevitability.", user="Agent Smith"))
asyncio.run(client(message="That is the sound of your death.", user="Agent Smith"))
asyncio.run(client(message="Goodbye, Mr. Anderson.", user="Agent Smith"))
asyncio.run(client(user="Agent Smith"))
asyncio.run(client(user="Agent Smith"))
# asyncio.run(client(user="Neo"))
# asyncio.run(client(message="My name is Neo.", user="Neo"))





# class Client:
#     def __init__(self, server_host="127.0.0.1", server_port=8000):
#         pass
#
#     def send(self, message=""):
#         pass