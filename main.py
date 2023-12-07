import logging
from telethon.sync import TelegramClient, events
from config import api_id, api_hash, phone_number, session_name, LOGGING_LEVEL, LOGGING_FORMAT
import asyncio

# Configure logging
logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)
# Create logger
logger = logging.getLogger(__name__)


async def fwr_message(client, event, my_group):
    msg = event.message
    chat = await client.get_entity(event.chat_id)
    sender = await event.get_sender()

    msg_author = f"🧑‍💻 **Author:** https://t.me/{sender.username}"
    msg_link = f"✍️ **Message:** https://t.me/c/{chat.id}/{msg.id}"
    msg_chat_link = f"👥 **Chat:** https://t.me/{chat.username}"
    result_msg = f"{msg.message}\n\n{msg_author}\n{msg_link}\n{msg_chat_link}"

    await client.send_message(my_group, result_msg, link_preview=False)


async def event_handler(client, my_group):
    @client.on(events.NewMessage(incoming=True, func=lambda e: not e.is_private))
    async def handler(event):
        try:
            # For simplicity, let's forward all messages to the specified chat
            await fwr_message(client, event, my_group)
            logger.info(f"Forwarded new message to chat {my_group.title}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")


async def main():
    client = TelegramClient(
        session_name,
        api_id,
        api_hash,
        system_version='4.16.30-vxCUSTOM'
    )

    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input('Enter the code: '))

        logger.info(f'Bot is running. Waiting for messages... ')

        # Get the group for forwarding messages
        my_group = await client.get_entity('https://t.me/+Esv8sTKv1a04ZGU6')

        print(f'Работает парсинг сообщений и отправка их в чат "{my_group.title}"')
        await event_handler(client, my_group)

    except Exception as e:
        logger.error(f"Error: {e}")
        raise
    finally:
        await client.disconnected


if __name__ == '__main__':
    asyncio.run(main())
