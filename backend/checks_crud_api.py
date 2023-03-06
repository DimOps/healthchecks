import requests
import os
from dotenv import load_dotenv


class ChecksCrudApi:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('TOKEN')
        self.auth = {'Authorization': f'Bearer {self.key}'}

    def get_checks_list(self):
        r = requests.get('https://api.pingdom.com/api/3.1/checks', headers=self.auth)
        return r.json()
