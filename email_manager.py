from bs4 import BeautifulSoup

from datetime import datetime
import hashlib
import random
from time import sleep
from pprint import pprint
import requests


class EmailManager:
    base_url: str = 'https://app.sonjj.com/'
    headers: dict = {
        'Accept':'application/json',
        'X-Api-Key': '931f2647f2db98f231af078a841b2b12'
    }

    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

        self.email_address: str = 'meaganbalderson.kn.n1.4@gmail.com'
        
    @classmethod
    def _get(cls, url: str) -> requests.Response:
        return requests.get(url, headers=cls.headers)
        
    def create_email_address(self) -> str:
        res = self._get(self.base_url + 'v1/temp_gmail/list/')
        self.email_address = random.choice(res.json()['data'])['email']
        return self.email_address
    
    def get_target_message(self, from_: int  = 0) -> dict:
        url = self.base_url +  f'v1/temp_gmail/inbox?email={self.email_address}&timestamp={from_}'
        print('URL TO GET MESSAGE', url)
        attempts = 5
        while attempts > 0:
            attempts -= 1
            res = self._get(url)
            print('STATUS', res.status_code, res.json())
            if messages := res.json()['messages']:
                target_message = [message for message in messages if 'VALR' in message['textFrom']][0]
                return target_message
            else:
                sleep(10)

            print('Current inbox messages')
            pprint(res.json())
    
    def get_verification_link(self, mid: str) -> str:
        res = self._get(self.base_url +  f'v1/temp_gmail/message?email={self.email_address}&mid={mid}')
        email_text = res.json()['body']
        soup = BeautifulSoup(email_text, 'html.parser')
        link = soup.find('a', href=True)
        return link['href']