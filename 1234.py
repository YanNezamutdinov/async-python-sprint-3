
open("chats.json", 'w')
open("last_read_message.json", 'w')
open("chat_name.json", 'w')



chats = {
    "chat_id_1": [[
        "message_id", "user_name", "message_text"
    ], [
        "message_id", "user_name", "message_text"
    ], [
        "message_id", "user_name", "message_text"
    ]],
    "chat_id_2": [[
        "message_id", "user_name", "message_text"
    ], [
        "message_id", "user_name", "message_text"
    ], [
        "message_id", "user_name", "message_text"
    ]],
}

last_read_message = {
    "user_name_1": {
        "chat_id_1": "message_id",
        "chat_id_2": "message_id",
        "chat_id_3": "message_id",
    },
    "user_name_2": {
        "chat_id_1": "message_id",
        "chat_id_2": "message_id",
        "chat_id_3": "message_id",
    }
}

chat_users = {
    "chat_id_1": None,
    "chat_id_2": ["user_name_1", "user_name_2"],
    "chat_id_3": ["user_name_2", "user_name_3"],
}