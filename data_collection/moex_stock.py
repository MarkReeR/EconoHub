from request_handler import RequestHandler
import json
from datetime import datetime

def parse_moex_data():
    moex_url = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json'
    filename = 'moex_stock.json'
    
    print("[INFO] Sending GET request...")
    request_handler = RequestHandler(moex_url)
    raw_data = request_handler.fetch_data()
    
    if not raw_data:
        print("[ERROR] Failed to fetch data.")
        return
    
    print("[INFO] Processing stock data...")
    processed_data = process_stock_data(raw_data)
    
    if processed_data:
        save_to_json(processed_data, filename)
        print("[INFO] Data processing complete.")
    else:
        print("[ERROR] No data to save.")

def process_stock_data(data):
    securities_data = data.get('securities', {}).get('data', [])
    securities_columns = data.get('securities', {}).get('columns', [])
    
    market_data = data.get('marketdata', {}).get('data', [])
    market_columns = data.get('marketdata', {}).get('columns', [])
    
    if not securities_data or not market_data:
        return None
    
    securities_dict = {row[0]: dict(zip(securities_columns, row)) for row in securities_data}
    
    for row in market_data:
        secid = row[0]
        if secid in securities_dict:
            securities_dict[secid].update(dict(zip(market_columns, row)))
    
    return {
        "date": datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
        "rates": securities_dict
    }

def save_to_json(data, filename='moex_stock.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"[INFO] Data successfully saved to {filename}.")
    except IOError as e:
        print(f"[ERROR] Failed to save data to {filename}: {e}")

if __name__ == "__main__":
    parse_moex_data()
