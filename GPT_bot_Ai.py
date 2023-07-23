import g4f
import asyncio
import requests
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from aiogram import Bot, executor, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage



ADMIN_ID=''
TOKEN = ""
URL = ""

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=20, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message

        :param message:
        """
        # Get current handler
        handler = current_handler.get()

        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t)

            # Cancel current handler
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed

        :param message:
        :param throttled:
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await message.reply('Сликшом много запросов! ')

        # Sleep.
        await asyncio.sleep(delta)

        # Check lock status
        thr = await dispatcher.check_key(key)

        # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Разблокирован.')
#####


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    text = """
    Здравсвуйте! Данный чат-бот ответит на все ваши вопросы!
    Просто напишите любой текст и подождите.
    P.S.: Бот работает на моделях GTP3 и GPT4
    
    Введите ваш запрос:
    """
    await message.answer(text=text)

async def chat_gpt(message: types.Message):
    text = message.text
    try:
        responseGpt4 = g4f.ChatCompletion.create(model='gpt-3.5-turbo', messages=[
            {"role": "user",
             "content": text}], provider=g4f.Provider.DeepAi, stream=True)
        await message.answer('First GPT4:')
        resultGpt4 = ''.join([message for message in responseGpt4])
        await message.answer(f'{resultGpt4}')

    except Exception as e:
        await message.answer(f'Первый GPT4 не работает. Подождите ответ GPT3')
        await bot.send_message(chat_id=ADMIN_ID, text=f'Возникала ошибка: {e}. Первый GPT4 не работает')

    try:
        responseGpt42 = g4f.ChatCompletion.create(model='gpt-4', messages=[
            {"role": "user",
             "content": text}], provider=g4f.Provider.ChatgptAi, stream=False)

        resultGpt42 = ''.join([message for message in responseGpt42])
        await message.answer('Second GPT4:')
        await message.answer(f'{resultGpt42}')

    except Exception as e:
        await message.answer(f'Возникала ошибка. Второй GPT4 пока не работает')
        await bot.send_message(chat_id=ADMIN_ID, text=f'Возникала ошибка: {e}. Второй GPT4 пока не работает')

    try:
        await message.answer('GPT3:')
        await asyncio.sleep(6)
        responseGpt3 = g4f.ChatCompletion.create(model='gpt-3.5-turbo', messages=[
            {"role": "user",
             "content": text}], provider=g4f.Provider.GetGpt, stream=True)

        resultGpt3 = ''.join([message for message in responseGpt3])
        await asyncio.sleep(4)
        await message.answer(f'{resultGpt3}')

    except Exception as e:
        await message.answer(f'Возникала ошибка. GPT3 пока не работает')
        await bot.send_message(chat_id=ADMIN_ID, text=f'Возникала ошибка: {e}. GPT3 пока не работает')

@dp.message_handler(lambda message: message.from_user.id != bot.id)
async def send(message: types.Message):

    await asyncio.sleep(2)

    try:
        prompt = message
        if not prompt:
            await message.answer('Вы задали пустой запрос.')
        else:
            await message.answer('Ожидание ответа на ваш запрос...')
            await message.answer_chat_action('typing')
            await chat_gpt(prompt)
    except Exception as e:
        await message.answer(f'GPT пока не работает. Подождите, мы разбираемя!')
        await bot.send_message(chat_id=ADMIN_ID, text=f'hello admin! We имеем problems с GPT: {e}')


if __name__ == '__main__':
    try:
        dp.middleware.setup(ThrottlingMiddleware())
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {'text': e, 'chat_id': ADMIN_ID}
        resp = requests.post(api_url, params=params)