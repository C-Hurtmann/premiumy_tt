import hashlib
from pprint import pprint
from faker import Faker
import requests


fake = Faker()


class EmailManager:
    base_url: str = 'https://privatix-temp-mail-v1.p.rapidapi.com/request/'
    headers: dict = {
        'x-rapidapi-host': 'privatix-temp-mail-v1.p.rapidapi.com',
        'x-rapidapi-key': 'e5d8f94a11msh0e0b78259340742p11851djsne46a022e76aa'
    }
    current_email_address: str

    @classmethod
    def _get(cls, url: str) -> requests.Response:
        return requests.get(url, headers=cls.headers)

        
    @classmethod
    def create_email_address(cls) -> str:
        res = cls._get(cls.base_url + 'domains/')
        email = f'{fake.last_name().lower()}.{fake.first_name().lower()[0]}' + res.json()[0]
        cls.current_email = email
        return email
    
    @classmethod
    def get_last_emails(cls):
        res = cls._get(cls.base_url +  'mail/id/' + hashlib.md5(cls.current_email_address.encode()).hexdigest())
        pprint(res.json())