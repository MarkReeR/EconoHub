import json

def load_currency_data():
    with open("./data/cbr_currency.json", "r", encoding="utf-8") as file:
        return json.load(file)

currency_data = load_currency_data()

def get_currency_value(currency):
    return currency_data["rates"][currency]["value"]

def get_currency_data():
    return currency_data["date"]

    