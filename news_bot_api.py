import asyncio
import requests
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from aiogram import Bot, executor, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


ADMIN_ID = ''
TOKEN = ""
URL = ""

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

NEWS_API_KEY=''

async def news_get(message: types.Message):
    count = 0
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=ru&'
           'category=business&'
           'totalResults=10&'
           f'apiKey={NEWS_API_KEY}')
    response = requests.get(url)
    data = response.json()['articles']
    for news in data:
        author = news['author']
        title = news['title']
        publishedAt = news['publishedAt']
        url = news['url']
        post = f'\nАвтор:{author}' \
             f'\ntitle:{title}' \
             f'\nurl:{url}' \
             f'\nDate:{publishedAt}'
        await message.answer(text=post)
        count+=1
        if count==10:
            break


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    text = """
    Здравсвуйте! Напишите /news чтобы получить новости
    """
    await message.answer(text=text)



@dp.message_handler(commands=["news"])
async def send(message: types.Message):
    try:
        await news_get(message)
    except Exception as e:
        await message.answer(f'База новостей пока недоступна. Обратитесь завтра!')
        await bot.send_message(chat_id=ADMIN_ID, text=f'hello admin! We имеем problems с новостью: {e}')


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {'text': e, 'chat_id': ADMIN_ID}
        resp = requests.post(api_url, params=params)
