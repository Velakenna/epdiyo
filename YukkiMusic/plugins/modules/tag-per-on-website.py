from YukkiMusic import app
import random
import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic.plugins.modules.blast import open_me_markup

# Assuming you have defined the bot and dispatcher objects for the Telegram bot
bot = Bot(token="5327660504:AAHPaqv8Z-_nFAAlkSLF-1_oE6i2g-gJ6JI")
dp = Dispatcher(bot)

spam_chats = []

TAGMES = ["hi", "hello", "good morning", "good evening", "good night"]
EMOJI = ["😊", "👋", "🌞", "🌙"]

def get_random_quote():
    url = "https://quotes.toscrape.com/random"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    quote = soup.find("span", class_="text").text.strip()
    author = soup.find("span", class_="author").text.strip()
    return f"{quote}\n- {author}"

def get_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    data = response.json()
    return f"{data['setup']}\n{data['punchline']}"

@app.on_message(filters.command=(["tagu"], prefixes=["/","#","@"]))
async def tagme_handler(msg: types.Message):
    chat_id = msg.chat.id
    if chat_id in spam_chats:
        await msg.reply("The tagme command is already running in this chat.")
        return

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""

    async for usr in bot.iter_chat_members(chat_id):
        if not chat_id in spam_chats:
            break

        if usr.user.is_bot:
            continue

        usrnum += 1
        #usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id})"
        usrtxt += f"{usr.user.mention}"

        if usrnum == 1:
            markup = open_me_markup()            
            await msg.reply_text(f"{usrtxt} {random.choice(TAGMES)}", reply_markup=markup)

            # Generate a random sleep time between 10 and 30 seconds
            sleep_time = random.randint(0, 5)
            await asyncio.sleep(sleep_time)

            usrnum = 0
            usrtxt = ""

    try:
        spam_chats.remove(chat_id)
    except:
        pass

@app.callback_query_handler(lambda c: c.data == 'open_me')
async def on_open_me_button_click(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    time_of_day = "evening" if "good evening" in callback_query.message.text.lower() else "morning"
    if time_of_day == "morning":
        quote = get_random_quote()
        await bot.send_message(chat_id, f"Good morning! Here's a random quote:\n\n{quote}")
    else:
        joke = get_random_joke()
        await bot.send_message(chat_id, f"Good evening! Here's a random joke:\n\n{joke}")

    await callback_query.answer()

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(app, skip_updates=True)
