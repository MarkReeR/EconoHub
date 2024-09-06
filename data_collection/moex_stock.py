from datetime import datetime

from request_handler import start_request
from save_data import save_data

def parse_moex_data():
    moex_url = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json'
    filename = 'moex_stock.json'
    
    raw_data = start_request(moex_url)
    print("[INFO] Processing stock data...")
    processed_data = process_stock_data(raw_data)
    
    if processed_data:
        save_data(processed_data, filename)
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

if __name__ == "__main__":
    parse_moex_data()
