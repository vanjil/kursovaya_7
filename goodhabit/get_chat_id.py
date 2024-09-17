from telegram import Bot
from decouple import config

TOKEN = config('TELEGRAM_API_TOKEN')
bot = Bot(token=TOKEN)

updates = bot.get_updates()
if updates:
    chat_id = updates[-1].message.chat_id
    print(f"Your chat ID is: {chat_id}")
else:
    print("No updates found. Please send a message to the bot first.")
