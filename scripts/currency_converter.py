import json

def convertor(amount, currency_code, json_file_path='./data/cbr_currency.json'):
    rates_data = get_data_from_file(json_file_path)
    results = {}
    
    currency_code_checker(currency_code, rates_data)
    
    if currency_code != 'RUB':
        currency_info = rates_data.get(currency_code)
        rate = currency_info.get('unit_rate')
        return convert_to_rub(amount, rate)
    
    else:
        # currency_codes = ['USD', 'EUR']
        return convert_from_rub(amount, currency_codes, rates_data)
      
def get_data_from_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('rates', {})
        
def currency_code_checker(currency_code, rates_data):
    if currency_code != 'RUB' and currency_code not in rates_data:
        raise ValueError(f"Код валюты {currency_code} не найден в данных")
    
def convert_to_rub(amount, rate):
    # currency_info = get_data_from_file(json_file_path).get(currency_code)
    # rate = currency_info.get('unit_rate')
    return amount * rate

def convert_from_rub(amount, data):
    # currency_info = get_data_from_file(json_file_path).get(currency_codes)
    # rate = currency_info.get('unit_rate')
    currency_amount = amount / rate
    return currency_amount

def convert_from_rub(amount, currency_codes, rates_data):
    results = {}
    for currency_code in currency_codes:
        currency_info = rates_data.get(currency_code)
        if currency_info:
            rate = currency_info.get('unit_rate')
            currency_amount = amount / rate
            results[currency_code] = currency_amount
        else:
            results[currency_code] = None  # Если курс не найден
    return results



if __name__ == '__main__':
    None