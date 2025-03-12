from bs4 import BeautifulSoup
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
    email_address: str
        
    @classmethod
    def _get(cls, url: str) -> requests.Response:
        return requests.get(url, headers=cls.headers)

    @classmethod
    def create_email_address(cls) -> str:
        res = cls._get(cls.base_url + 'v1/temp_gmail/list/')
        cls.email_address = random.choice(res.json()['data'])['email']
        return cls.email_address
    
    @classmethod
    def get_target_message(cls, from_: int  = 0) -> dict:
        url = cls.base_url +  f'v1/temp_gmail/inbox?email={cls.email_address}&timestamp={from_}'
        print('URL TO GET MESSAGE', url)
        attempts = 5
        while attempts > 0:
            attempts -= 1
            res = cls._get(url)
            print('STATUS', res.status_code, res.json())
            if messages := res.json()['messages']:
                target_message = [message for message in messages if 'VALR' in message['textFrom']][0]
                return target_message
            else:
                sleep(10)

            print('Current inbox messages')
            pprint(res.json())
    
    @classmethod
    def get_verification_link(cls, mid: str) -> str:
        res = cls._get(cls.base_url +  f'v1/temp_gmail/message?email={cls.email_address}&mid={mid}')
        email_text = res.json()['body']
        soup = BeautifulSoup(email_text, 'html.parser')
        link = soup.find('a', href=True)
        return link['href']
