import requests
import json
import xml.etree.ElementTree as ET

from fake_useragent import UserAgent

import traceback

class RequestHandler:
    def __init__(self, url):
        self.url = url
        self.ua = UserAgent()
    
    def fetch_data(self):
        try:
            headers = {'User-Agent': self.ua.random}
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
                        
            content_type = response.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                return response.json()
            elif 'application/xml' in content_type or 'text/xml' in content_type:
                xml_data = response.content.decode('windows-1251')
                return xml_data
            else:
                print("Unsupported Content-Type:", content_type)
                return None

        except requests.RequestException as e:
            print(f"[ERROR] Request failed: {e}")
            traceback.print_exc()
            return None
        
        
def start_request(url):
    print("[INFO] Sending GET request...")
    raw_data = RequestHandler(url).fetch_data()
    if not raw_data:
            print("[ERROR] Failed to fetch data.")
            return
    print("[INFO] Successfully retrieved data.")
    return raw_data
    