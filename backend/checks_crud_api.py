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

    def get_check_outage_summary(self, check_id, *args):
        # report defaults on one week according to documentation
        r = requests.get(f'https://api.pingdom.com/api/3.1/summary.outage/{check_id}', headers=self.auth)
        return r.json()

    def create_check(self, data):
        r = requests.post(f'https://api.pingdom.com/api/3.1/checks', headers=self.auth, json=data)
        return r.json()
