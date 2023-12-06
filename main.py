import csv
import re
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, ChannelForbidden, ChatForbidden
from config import api_id, api_hash, phone_number, session_name
import asyncio

cache = {}


async def get_groups(client):
    if 'get_groups' in cache:
        return cache['get_groups']

    last_date = None
    size_chats = 200
    groups =[]

    dialogs = await client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=size_chats,
            hash=0
    ))

    for chat in dialogs.chats:
        try:
            if chat.megagroup and type(chat) != ChatForbidden and type(chat) != ChannelForbidden:
                groups.append(chat)
        except:
            continue

    cache['get_groups'] = groups
    return groups


async def parse_group(client):
    groups = await get_groups(client)

    print('Выберите номер группы из перечня:')
    i = 0
    for g in groups:
        print(f"{str(i)} - {g.title} | Кол-во учатников: {g.participants_count}")
        i += 1

    g_index = input("Введите нужную цифру: ")
    target_group = groups[int(g_index)]

    print("Узнаем пользователей...")
    all_participants = await client.get_participants(target_group.username)
    print("Парсинг участников группы успешно выполнен.")
    return all_participants, target_group


async def save_group_users_to_csv(client):
    all_participants, target_group = await parse_group(client)
    filename = re.sub(r'[^\w_.-]', '_', target_group.title)
    print(f"Сохраняем данные в файл {filename}.csv ...")
    with open(f"{filename}.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'name', 'group'])
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, name, target_group.title])
    print("Данные участников группы сохранены в csv файл.")


async def main():
    client = TelegramClient(
        session_name,
        api_id,
        api_hash,
        system_version='4.16.30-vxCUSTOM'
    )

    await client.start(phone_number)
    while True:
        await save_group_users_to_csv(client)
        answer = input("Хотите продолжить? (y/n): ")
        if answer.lower() != 'y':
            break

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())







