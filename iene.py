import requests
from config import CURRENCYCONVERTER_API_KEY


def valor_iene():
    api_link = "https://free.currconv.com/api/v7/convert?q=" \
               "JPY_BRL&compact=ultra&apiKey={}".format(CURRENCYCONVERTER_API_KEY)

    request = requests.get(api_link)
    result_list = request.json()
    valor = result_list['JPY_BRL']

    return valor
