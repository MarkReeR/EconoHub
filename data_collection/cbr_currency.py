import xml.etree.ElementTree as ET

from request_handler import start_request
from save_data import save_data


def parse_exchange_rates():
    # URL для получения ежедневных курсов валют с сайта Центрального банка России (ЦБР)
    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="
    filename = 'cbr_currency.json'
            
    raw_data = parse_xml(start_request(url))
    print("[INFO] XML parsing completed successfully.")
    processed_data = extract_date_and_rates(raw_data)
    
    if processed_data:
        save_data(processed_data, filename)
        print("[INFO] Data processing complete.")
    else:
        print("[ERROR] No data to save.")

def extract_date_and_rates(parsed_data):
    if not parsed_data:
        print("[ERROR] XML parsing failed.")
        return
    
    val_curs = parsed_data.get('ValCurs', {})
    date = val_curs.get('@Date')
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
    print(f"[INFO] Data received for {date}.")
    return {'date': date, 'rates': rates}

def parse_xml(data):
    try:
        root = ET.fromstring(data)
        return xml_to_dict(root)
    except ET.ParseError as e:
        print(f"[ERROR] XML parsing error: {e}")
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

if __name__ == "__main__":
    parse_exchange_rates()
