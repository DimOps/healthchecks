import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_checks_list():
    key = os.getenv('TOKEN')
    auth = {"Authorization": f"Bearer {key}"}
    r = requests.get('https://api.pingdom.com/api/3.1/checks', headers=auth)

    return r.content
