import asyncio
import json


async def client(message: str = None, user: str = "Anonymous"):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8000)
    last_uuid = ""
    query = {'user': user,
             'message': message,
             'last_read_message': last_uuid}
    data_for_client = json.dumps(query).encode()
    writer.write(data_for_client)
    await writer.drain()
    data = await reader.read(9999)

    writer.close()
    await writer.wait_closed()

    message = json.loads(data.decode())
    print(message)
    # for values in message:
    #
    #     print(f"{values[1]}: {values[2]}")

asyncio.run(client(user="Agent Smith"))
asyncio.run(client(message="Hi Neo!", user="Agent Smith"))
asyncio.run(client(message="I'm mister Smith", user="Agent Smith"))
asyncio.run(client(message="I see you!", user="Agent Smith"))
asyncio.run(client(message="...", user="Agent Smith"))
asyncio.run(client(message="...look back Neo...", user="Agent Smith"))



# ―Вы слышите, мистер Андерсон? Это рок, неизбежность. Шаги Вашей смерти. Прощайте, мистер Андерсон.
# ―Меня зовут Нео.

# class Client:
#     def __init__(self, server_host="127.0.0.1", server_port=8000):
#         pass
#
#     def send(self, message=""):
#         pass