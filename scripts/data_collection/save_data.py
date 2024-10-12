import json

def save_data(data, filename):
    try:
        filepath = f"./data/{filename}"
        with open(filepath, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"[INFO] Data successfully saved to '{filepath}'.")
    except IOError as e:
        print(f"[ERROR] Failed to save data to '{filepath}': {e}")