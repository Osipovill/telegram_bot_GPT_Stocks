from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message
from parser_data_stock import *

TOKEN: str = ''

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['get_quote_endpoint'])
async def get_quote_endpoint_(message: types.Message):
    # Получаем название акции после команды get_quote_endpoint
    symbol = message.get_args()

    if not symbol:
        await message.reply("Вы не указали название акции. Попробуйте еще раз с командой get_quote_endpoint <i>название</i>.")
        return

    try:
        data = get_quote_endpoint(symbol)

        # Извлечение данных в переменные
        symbol = data['Global Quote']['01. symbol']
        open_price = data['Global Quote']['02. open']
        high_price = data['Global Quote']['03. high']
        low_price = data['Global Quote']['04. low']
        current_price = data['Global Quote']['05. price']
        volume = data['Global Quote']['06. volume']
        latest_trading_day = data['Global Quote']['07. latest trading day']
        previous_close = data['Global Quote']['08. previous close']
        change = data['Global Quote']['09. change']
        change_percent = data['Global Quote']['10. change percent']

        text = f'Символы:{symbol}' \
                f'\nЦена открытия:{open_price}' \
                f'\nВысшая цена:{high_price}' \
                f'\nНаименьшая цена:{low_price}' \
                f'\nТекущая цена:{current_price}' \
                f'\nУровень активности:{volume}' \
                f'\nКрайний день продаж:{latest_trading_day}' \
                f'\nЦена перед закрытием:{previous_close}' \
                f'\nИзменение:{change}' \
                f'\nИзменение в процентах:{change_percent}'
        await message.answer(text=text)

    except Exception as e:
        await message.answer(text='Произошла ошибка, проверьте корректность введенных данных!')


@dp.message_handler(commands=['get_symbol_search'])
async def get_symbol_search_(message: types.Message):
    # Получаем название акции после команды get_symbol_search
    symbol = message.get_args()

    if not symbol:
        await message.reply("Вы не указали название акции. Попробуйте еще раз с командой get_quote_endpoint <i>название</i>.")
        return

    try:
        data = get_symbol_search(symbol)
        text = ''
        # Извлечение данных для каждого символа из списка
        for match in data['bestMatches']:
            symbol = match['1. symbol']
            name = match['2. name']
            type_ = match['3. type']
            region = match['4. region']
            market_open = match['5. marketOpen']
            market_close = match['6. marketClose']
            timezone = match['7. timezone']
            currency = match['8. currency']
            match_score = match['9. matchScore']

            text += f'Символы:{symbol}' \
                    f'\nНазвание:{name}' \
                    f'\nТип:{type_}' \
                    f'\nРегион:{region}' \
                    f'\nВремя открытия рынка:{market_open}' \
                    f'\nВремя закрытия рынка:{market_close}' \
                    f'\nЧасовой пояс:{timezone}' \
                    f'\nВалюта:{currency}' \
                    f'\Match score:{match_score}'
            text += f'\n' \
                    f'\n'
        await message.answer(text=text)

    except Exception as e:
        await message.answer(text='Произошла ошибка, проверьте корректность введенных данных!')


@dp.message_handler(commands=['get_market_status'])
async def get_market_status_(message: types.Message):
    try:
        data = get_market_status()
        text = ''
        # Извлечение данных для каждого рынка из списка
        for market in data['markets']:
            current_status = market['current_status']
            local_close = market['local_close']
            local_open = market['local_open']
            market_type = market['market_type']
            notes = market['notes']
            primary_exchanges = market['primary_exchanges']
            region = market['region']

            text += f'Текущий статус:{current_status}' \
                    f'\nВремя закрытия:{local_close}' \
                    f'\nВремя открытия:{local_open}' \
                    f'\nТип:{market_type}' \
                    f'\nЗамечание:{notes}' \
                    f'\nПервичная биржа:{primary_exchanges}' \
                    f'\nРегион:{region}'
            text += f'\n' \
                    f'\n'
        await message.answer(text=text)

    except Exception as e:
        await message.answer(text='Произошла ошибка...')


@dp.message_handler(commands=['get_top_gainers_losers'])
async def get_top_gainers_losers_(message: types.Message):
    try:
        data = get_top_gainers_losers()

        # Извлечение данных из списка 'most_actively_traded'
        text='Most Actively Traded:'
        for item in data['most_actively_traded']:
            ticker = item['ticker']
            price = item['price']
            change_amount = item['change_amount']
            change_percentage = item['change_percentage']
            volume = item['volume']

            text += f'\n' \
                    f'\n'
            text += f'Символы:{ticker}' \
                    f'\nЦена:{price}' \
                    f'\nИзменение:{change_amount}' \
                    f'\nИзменение в процентах:{change_percentage}' \
                    f'\nАктивность:{volume}'
        await message.answer(text=text)

        # Извлечение данных из списка 'top_gainers'
        text='Top Gainers:'
        for item in data['top_gainers']:
            ticker = item['ticker']
            price = item['price']
            change_amount = item['change_amount']
            change_percentage = item['change_percentage']
            volume = item['volume']

            text += f'\n' \
                    f'\n'
            text += f'Символы:{ticker}' \
                    f'\nЦена:{price}' \
                    f'\nИзменение:{change_amount}' \
                    f'\nИзменение в процентах:{change_percentage}' \
                    f'\nАктивность:{volume}'
        await message.answer(text=text)

        # Извлечение данных из списка 'top_losers'
        text='Top Losers:'
        for item in data['top_losers']:
            ticker = item['ticker']
            price = item['price']
            change_amount = item['change_amount']
            change_percentage = item['change_percentage']
            volume = item['volume']

            text += f'\n' \
                    f'\n'
            text = f'Символы:{ticker}' \
                    f'\nЦена:{price}' \
                    f'\nИзменение:{change_amount}' \
                    f'\nИзменение в процентах:{change_percentage}' \
                    f'\nАктивность:{volume}'
        await message.answer(text=text)

    except Exception as e:
        await message.answer(text='Произошла ошибка...')


@dp.message_handler(commands=['get_overview'])
async def get_overview_(message: types.Message):
    # Получаем название акции после команды get_overview
    symbol = message.get_args()

    if not symbol:
        await message.reply("Вы не указали название акции. Попробуйте еще раз с командой get_quote_endpoint <i>название</i>.")
        return

    try:
        data = get_overview(symbol)

        # Извлечение данных в переменные
        symbol = data['Symbol']
        name = data['Name']
        sector = data['Sector']
        description = data['Description']
        price_to_earnings_ratio = data['PERatio']
        price_to_book_ratio = data['PriceToBookRatio']
        dividend_yield = data['DividendYield']
        earnings_per_share = data['EPS']
        market_capitalization = data['MarketCapitalization']

        text = f'Символы:{symbol}' \
                f'\nНазвание:{name}' \
                f'\nСектор:{sector}' \
                f'\nОписание:{description}' \
                f'\nPrice_to_earnings_ratio:{price_to_earnings_ratio}' \
                f'\nPrice_to_book_ratio:{price_to_book_ratio}' \
                f'\Дивиденды:{dividend_yield}' \
                f'\nEarnings_per_share:{earnings_per_share}' \
                f'\nMarket_capitalization:{market_capitalization}'
        await message.answer(text=text)

    except Exception as e:
        await message.answer(text='Произошла ошибка... Проверьте корректность введенных данных!')


@dp.message_handler(commands=['get_earnings_calendar'])
async def get_earnings_calendar_(message: types.Message):
    # Получаем название акции после команды get_earnings_calendar
    symbol = message.get_args()

    if not symbol:
        await message.reply("Вы не указали название акции. Попробуйте еще раз с командой get_quote_endpoint <i>название</i>.")
        return

    try:
        data = get_earnings_calendar(symbol)

        # Разделяем строки по переносу строки для получения списка строк
        lines = data.split('\r\n')

        # Пропускаем первую строку с заголовками и разделяем данные по запятой
        values = lines[1].split(',')

        # Извлекаем данные в переменные
        symbol = values[0]
        name = values[1]
        report_date = values[2]
        fiscal_date_ending = values[3]
        estimate = float(values[4])  # Конвертируем в числовой формат
        currency = values[5]

        text = f'Символы:{symbol}' \
                f'\nНазвание:{name}' \
                f'\nДата прогноза:{report_date}' \
                f'\nДата окончания прогноза:{fiscal_date_ending}' \
                f'\nПрогноз:{estimate}' \
                f'\nВалюта:{currency}'
        await message.answer(text=text)

    except Exception as e:
        await message.answer(text='Произошла ошибка... Проверьте корректность введенных данных!')


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    await message.answer('Привет!\nЭто бот парсинга акций!')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(f'/start - Запустить бота.' \
                        f'\n' \
                        f'\n/get_quote_endpoint - Поиск самой свежей информации о ценах и объемах для тикера по вашему выбору. (Введите символы акции через пробел после команды)' \
                        f'\n' \
                        f'\n/get_symbol_search - Поиск символов компании по названию. (Введите название компании через пробел после команды)' \
                        f'\n' \
                        f'\n/get_market_status - Просмотр рыночного статуса (открытый или закрытый) основных торговых площадок для акций, форекс и криптовалют по всему миру.' \
                        f'\n' \
                        f'\n/get_top_gainers_losers - Поиск текущих и исторических рыночных новости и данных о настроениях из большого и растущего выбора ведущих новостных агентств по всему миру,' \
                        f'\nохватывающих акции, криптовалюты, форекс и широкий круг тем, таких как фискальная политика, слияния и поглощения, IPO и т.д.' \
                        f'\n' \
                        f'\n/get_overview - Поиск информации о компании, финансовые коэффициентах и других ключевых показателях для указанного капитала.' \
                        f'(Введите символы акции через пробел после команды) ' \
                        f'\n' \
                        f'\n/get_earnings_calendar - Поиск списка доходов компании, ожидаемых в ближайшие 3 месяца. (Введите символы акции через пробел после команды)')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
