import hashlib
from pprint import pprint
import requests


class EmailManager:
    base_url: str = 'https://privatix-temp-mail-v1.p.rapidapi.com/request/'
    headers: dict = {
        'x-rapidapi-host': 'privatix-temp-mail-v1.p.rapidapi.com',
        'x-rapidapi-key': 'e5d8f94a11msh0e0b78259340742p11851djsne46a022e76aa'
    }

    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

        self.email_address: str
        
    @classmethod
    def _get(cls, url: str) -> requests.Response:
        return requests.get(url, headers=cls.headers)
        
    def create_email_address(self) -> str:
        res = self._get(self.base_url + 'domains/')
        email = f'{self.last_name.lower()}.{self.first_name.lower()[0]}' + res.json()[0]
        self.email_address = email
        return email
    
    def get_last_emails(self):
        res = self._get(self.base_url +  'mail/id/' + hashlib.md5(self.current_email_address.encode()).hexdigest())
        pprint(res.json())