import json

def load_currency_data():
    """
    Загружает данные курсов валют из файла cbr_currency.json
    """
    with open("./data/cbr_currency.json", "r", encoding="utf-8") as file:
        return json.load(file)