import requests
from fake_useragent import UserAgent
import xml.etree.ElementTree as ET
import json


def fetch_exchange_rates():
    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="
    headers = {
        'User-Agent': UserAgent().random
    }
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        xml_data = response.content
        return xml_data
    except requests.exceptions.HTTPError as http_err:
        print(f"[ERROR] HTTP ошибка: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"[ERROR] Ошибка подключения: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"[ERROR] Ошибка таймаута: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"[ERROR] Неизвестная ошибка: {req_err}")
    return None

def parse_exchange_rates():
    xml_data = fetch_exchange_rates()

    if xml_data:
        root = ET.fromstring(xml_data)
        date = root.attrib.get("Date")
        rates = {}

        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            nominal = int(valute.find('Nominal').text)
            name = valute.find('Name').text
            value = float(valute.find('Value').text.replace(',', '.'))
            unit_rate = float(valute.find('VunitRate').text.replace(',', '.'))

            rates[char_code] = {
                'name': name,
                'nominal': nominal,
                'value': value,
                'unit_rate': unit_rate,
            }
        return date, rates
    else:
        return "[ERROR] No xml data."   

def convert_to_json(date, rates):
    data = {
        "date": date,
        "rates": rates
    }
    return json.dumps(data, indent=4, ensure_ascii=False)

def data_save(date, rates):
    json_data = convert_to_json(date, rates)
    with open(f'cbr_currency.json', 'w', encoding='utf-8') as file:
        file.write(json_data)

def main():
    date, rates = parse_exchange_rates()
    data_save(date, rates)

    print(f"Курсы валют на {date}:")
    for char_code, info in rates.items():
        print(f"{info['name']} ({char_code}): {info['nominal']} = {info['value']} RUB; 1 = {info['unit_rate']};")

if __name__ == "__main__":
    main()