from selenium import webdriver
from twocaptcha_extension_python import TwoCaptcha

from proxy_extension_builder import proxies

class Config:
    
    # proxy credentials
    proxy_username: str = 'IKUmhvPAcfZzlVIN'
    proxy_password: str = 'mobile;bg;;;' 
    proxy_host: str = 'proxy.soax.com'
    proxy_port: str = '9000'
    

    two_captcha_api_key: str = '806126af0f402f205c1e49ffc88865f2'

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