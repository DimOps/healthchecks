import requests
import os
from dotenv import load_dotenv


class ChecksCrudApi:
    def __init__(self):
        load_dotenv()
        self.url = 'https://api.pingdom.com/api/3.1'
        self.key = os.getenv('TOKEN')
        self.auth = {'Authorization': f'Bearer {self.key}'}

    def get_checks_list(self):
        r = requests.get(f'{self.url}/checks', headers=self.auth)
        return r.json()

    def get_check_outage_summary(self, check_id, **kwargs):
        q_params = []
        # report defaults on one week according to Pingdom API documentation
        if kwargs:
            q_params = [(k, v) for k, v in kwargs.items()]
        r = requests.get(f'{self.url}/summary.outage/{check_id}', headers=self.auth, params=q_params)
        return r.json()

    def create_check(self, data):
        r = requests.post(f'{self.url}/checks', headers=self.auth, json=data)
        return r.json()

    def delete_check(self, check_id):
        r = requests.delete(f'{self.url}/checks/{check_id}', headers=self.auth)
        return r.json()

    def delete_many_checks(self, list_ids):
        s = ','.join([str(i) for i in list_ids])
        data = {
                "delcheckids": f"{s}"
                }
        
        r = requests.delete(f'{self.url}/checks', headers=self.auth, json=data)
        return r.json()
