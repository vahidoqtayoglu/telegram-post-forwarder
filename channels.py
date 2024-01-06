from telethon.sync import TelegramClient
import asyncio
import os
from dotenv import load_dotenv

# .env dosyasını yükleyin
load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
phone_number = os.getenv('phone_number')
bot_account = os.getenv('bot_account')


client = TelegramClient(phone_number, api_id, api_hash)

async def get_last_message(channel_username):
    messages = await client.get_messages(channel_username, limit=1)
    return messages[0] if messages else None


async def send_messages_to_user(messages, user_username):
    for message, channel_username in messages:
        if message.media:
            # If the message contains media, send the media
            await client.send_file(user_username, message.media, caption=f"{message.text}\n\nPaylaşdı: {channel_username}")
        elif message.text:
            # If the message is text, send it with the channel information
            await client.send_message(user_username, f"{message.text}\n\nPaylaşdı: {channel_username}")
        else:
            pass


async def watch_for_new_messages(channels, user_username):
    last_message_ids = {channel['username']: 0 for channel in channels}

    while True:
        all_messages = []
        for channel in channels:
            last_message = await get_last_message(channel['username'])
            last_message_id = last_message_ids[channel['username']]


            if last_message and last_message.id > last_message_id:
                all_messages.append((last_message, channel['name']))
                last_message_ids[channel['username']] = last_message.id

        if all_messages:
            await send_messages_to_user(all_messages, user_username)

        await asyncio.sleep(10)


async def main():
    #Start the session
    await client.start()

    #Channels
    channels_to_watch = [
    {'username': 'tass_agency', 'name': 'Tass'},
    {'username': 'belta_telegramm', 'name': 'Belta'},
    {'username': 'uniannet', 'name': 'Unian'},
]


    #Start the monitoring loop
    await watch_for_new_messages(channels_to_watch, bot_account)

if __name__ == '__main__':
    asyncio.run(main())
