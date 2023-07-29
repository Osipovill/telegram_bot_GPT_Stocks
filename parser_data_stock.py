import datetime
import requests
from pprint import pprint


apikey = ''
url = 'https://www.alphavantage.co/query?'


# Эта служба, являющаяся облегченной альтернативой API временных рядов, возвращает самую свежую информацию о ценах и объемах для тикера по вашему выбору.
def get_quote_endpoint(symbol: str):
    response = requests.get(f'{url}function=GLOBAL_QUOTE&symbol={symbol}&datetype=json&apikey={apikey}')
    response.raise_for_status()
    return response.json()


# Поиск символов компании по названию
def get_symbol_search(keywords: str):
    response = requests.get(f'{url}function=SYMBOL_SEARCH&keywords={keywords}&datetype=json&apikey={apikey}')
    response.raise_for_status()
    return response.json()


# Просмотр рыночного статуса (открытый или закрытый) основных торговых площадок для акций, форекс и криптовалют по всему миру.
def get_market_status():
    response = requests.get(f'{url}function=MARKET_STATUS&apikey={apikey}')
    response.raise_for_status()
    return response.json()


#  Этот API возвращает текущие и исторические рыночные новости и данные о настроениях из большого и растущего выбора ведущих новостных агентств по всему миру,
#  охватывающих акции, криптовалюты, форекс и широкий круг тем, таких как фискальная политика, слияния и поглощения, IPO и т.д.
def get_top_gainers_losers():
    response = requests.get(f'{url}function=TOP_GAINERS_LOSERS&apikey={apikey}')
    response.raise_for_status()
    return response.json()


# Этот API возвращает информацию о компании, финансовые коэффициенты и другие ключевые показатели для указанного капитала.
# Данные, как правило, обновляются в тот же день, когда компания сообщает о своих последних доходах и финансовых показателях.
def get_overview(symbol: str):
    response = requests.get(f'{url}function=OVERVIEW&symbol={symbol}&apikey={apikey}')
    response.raise_for_status()
    return response.json()


# Этот API возвращает список доходов компании, ожидаемых в ближайшие 3.
def get_earnings_calendar(symbol: str):
    response = requests.get(f'{url}function=EARNINGS_CALENDAR&symbol={symbol}&apikey={apikey}')
    response.raise_for_status()
    return response.text
