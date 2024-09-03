import requests
import json
import xml.etree.ElementTree as ET

from fake_useragent import UserAgent


class RequestHandler:
    def __init__(self, url):
        self.url = url
        self.ua = UserAgent()
    
    def fetch_data(self):
        try:
            headers = {'User-Agent': self.ua.random}
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()

            content_type = response.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                # return self._parse_json(response.text)
                return response.text
            elif 'application/xml' in content_type or 'text/xml' in content_type:
                #return self._parse_xml(response.text)
                return response.text
            else:
                print("Unsupported Content-Type:", content_type)
                return None
            
        except requests.RequestException as e:
            print('-'*128)
            print(f"[Error] Request failed: {e}")
            return None