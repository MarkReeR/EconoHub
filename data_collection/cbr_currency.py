import xml.etree.ElementTree as ET
import json

from request_handler import RequestHandler

# URL для получения ежедневных курсов валют с сайта Центрального банка России (ЦБР)
CBR_URL = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="

def parse_exchange_rates(url):
    request_handler = RequestHandler(url)
    xml_data = request_handler.fetch_data()

    if not xml_data:
        print("[ERROR] Не удалось получить данные.")
        return None, None
    
    print("[INFO] Удалось получить данные.")
        
    parsed_data = parse_xml(xml_data)
    if not parsed_data:
        print("[ERROR] Парсинг XML неудачен.")
        return None, None
    
    print("[INFO] Парсинг XML успешно завершен.")
    return extract_date_and_rates(parsed_data)

def extract_date_and_rates(parsed_data):
    val_curs = parsed_data.get('ValCurs', {})
    date = val_curs.get('@Date', 'Дата отсутствует')
    rates = {}
    
    for valute in val_curs.get('Valute', []):
        valute_id = valute.get('@ID')
        num_code = valute.get('NumCode')
        char_code = valute.get('CharCode')
        nominal = int(valute.get('Nominal', '1'))
        name = valute.get('Name')
        value = float(valute.get('Value', '0').replace(',', '.'))
        unit_rate = float(valute.get('VunitRate', '0').replace(',', '.'))

        rates[char_code] = {
            'id': valute_id,
            'num_code': num_code,
            'name': name,
            'nominal': nominal,
            'value': value,
            'unit_rate': unit_rate,
        }
    
    if date == 'Дата отсутствует':
        print("[ERROR] Не удалось извлечь дату из данных.")
    else:
        print(f"[INFO] Данные получены для {date}.")
        save_rates_to_file(date, rates)
    
    return date, rates

def parse_xml(data):
    try:
        root = ET.fromstring(data)
        return xml_to_dict(root)
    except ET.ParseError as e:
        print(f"[ERROR] Ошибка парсинга XML: {e}")
        return None

def xml_to_dict(element):
    def parse_element(elem):
        if len(elem) == 0:
            return elem.text.strip() if elem.text else ''
        
        result = {}
        for child in elem:
            child_result = parse_element(child)
            if child.tag not in result:
                result[child.tag] = child_result
            else:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_result)
        
        result.update({f"@{attr}": elem.attrib[attr] for attr in elem.attrib})
        return result

    return {element.tag: parse_element(element)}

def save_rates_to_file(date, rates, filename='cbr_currency.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({'date': date, 'rates': rates}, f, ensure_ascii=False, indent=4) 
    print(f"[INFO] Курсы валют на {date} успешно сохранены в файл '{filename}'.")

if __name__ == "__main__":
    date, rates = parse_exchange_rates(CBR_URL)
