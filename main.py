import logging
from telethon.sync import TelegramClient, events
from config import api_id, api_hash, phone_number, session_name, LOGGING_LEVEL, LOGGING_FORMAT
from modules.text_processor import TextProcessor
from utils import get_keywords_and_channels
import asyncio

logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)
logger = logging.getLogger(__name__)

text_processor = TextProcessor()


async def fwr_message(client, event, res_txt, my_group):
    msg = event.message
    chat = await client.get_entity(event.chat_id)
    sender = await event.get_sender()

    msg_author = f"🧑‍💻 <b>Author:</b> https://t.me/{sender.username}"
    msg_link = f"✍️ <b>Message:</b> https://t.me/c/{chat.id}/{msg.id}"
    msg_chat_link = f"👥 <b>Chat:</b> https://t.me/{chat.username}"
    result_msg = f"{res_txt}\n\n{msg_author}\n{msg_link}\n{msg_chat_link}"

    await client.send_message(my_group, result_msg, link_preview=False, parse_mode='html')


async def event_handler(client):
    destination_channel_id, keywords = await get_keywords_and_channels()
    my_group = await client.get_entity(destination_channel_id[0])

    @client.on(events.NewMessage(incoming=True, func=lambda e: not e.is_private))
    async def handler(event):
        try:
            original_text = event.message.message
            res_text = text_processor.get_result(original_text, keywords)
            if res_text != original_text:
                await fwr_message(client, event, res_text, my_group)
                logger.info(f"Forwarded new message to chat {my_group.title}, text: {original_text}")
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
        await event_handler(client)

    except Exception as e:
        logger.error(f"Error: {e}")
        raise
    finally:
        await client.disconnected


if __name__ == '__main__':
    asyncio.run(main())
