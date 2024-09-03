import xml.etree.ElementTree as ET
import json

from request_handler import RequestHandler

# URL для получения ежедневных курсов валют с сайта Центрального банка России (ЦБР)
url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="

def parse_exchange_rates():
    request_handler = RequestHandler(url)
    xml_data = request_handler.fetch_data()

    # TODO rewrite
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
    
# def _parse_xml(data):
#     try:
#         root = ET.fromstring(data)
#         return self._xml_to_dict(root)
#     except ET.ParseError as e:
#         print(f"XML parsing failed: {e}")
#         return None

# def _xml_to_dict(element):
#     def parse_element(elem):
#         if len(elem) == 0:
#             return elem.text
#         return {child.tag: parse_element(child) for child in elem}
#     return {element.tag: parse_element(element)}

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


    # def _parse_json(self, data):
    #     try:
    #         return json.loads(data)
    #     except json.JSONDecodeError as e:
    #         print(f"JSON decoding failed: {e}")
    #         return None

    # def _parse_xml(self, data):
    #     try:
    #         root = ET.fromstring(data)
    #         return self._xml_to_dict(root)
    #     except ET.ParseError as e:
    #         print(f"XML parsing failed: {e}")
    #         return None

    # def _xml_to_dict(self, element):
    #     def parse_element(elem):
    #         if len(elem) == 0:
    #             return elem.text
    #         return {child.tag: parse_element(child) for child in elem}

    #     return {element.tag: parse_element(element)}