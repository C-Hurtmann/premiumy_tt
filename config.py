import os
from dotenv import load_dotenv
from selenium import webdriver
from twocaptcha_extension_python import TwoCaptcha

from proxy_extension_builder import proxies


load_dotenv()

class Config:
    
    # proxy credentials
    proxy_username: str = os.getenv('PROXY_USERNAME')
    proxy_password: str = os.getenv('PROXY_PASSWORD')
    proxy_host: str = os.getenv('PROXY_HOST')
    proxy_port: str = os.getenv('PROXY_PORT')
    
    # two captcha api key
    two_captcha_api_key: str = os.getenv('TWO_CAPTCHA_API_KEY')

    @classmethod
    def setup(cls) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument(TwoCaptcha(cls.two_captcha_api_key).load())
        options.add_extension(
            proxies(
                username=cls.proxy_username,
                password=cls.proxy_password,
                endpoint=cls.proxy_host,
                port=cls.proxy_port
            )
        )
        return options