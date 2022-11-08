import asyncio
import json


async def client(message: str = None, user: str = "Anonymous"):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8000)
    query = {'user': user,
             'message': message}
    data_for_client = json.dumps(query).encode()
    writer.write(data_for_client)
    await writer.drain()

    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = json.loads(data.decode())
        print(message)

    # message = )
    # print(message)
    # for record in message:
    #     if not record:
    #         print("В чате пока пусто")
    #     else:
    #         print(record)
    # print(f'Received: {data.decode()!r}')
    writer.close()
    await writer.wait_closed()

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