import os
import random
import requests
import hashlib
from pprint import pprint
from pathlib import Path
import time

from faker import Faker

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
from fake_useragent import UserAgent


fake = Faker()


def save_page_source(source: str) -> None:
    parser = etree.HTMLParser(remove_blank_text=True)
    tree = etree.ElementTree(etree.HTML(source, parser))

    with open('src.xml', 'wb') as f:
        tree.write(f, pretty_print=True, encoding='utf-8', xml_declaration=True)


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
        res = cls._get(cls.base_url +  'mail/id/' + hashlib.md5(email.encode()).hexdigest())
        pprint(res.json())



with open(Path('proxyscrape_premium_http_proxies.txt')) as f:
    proxy = random.choice(f.readlines())


try:
    # Set up Chrome options
    options = Options()
    options.add_argument(f'--proxy-server=http://{proxy}')

    # Set up WebDriver with ChromeDriverManager
    print("Setting up driver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    # Main workflow
    print("Get welcome page...")
    driver.get('https://coinbase.com')
    wait = WebDriverWait(driver, 30)
    action = ActionChains(driver)

    print('Click signup button...')
    signup_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-testid="header-get-started-button"]')))
    time.sleep(6)
    action.move_to_element(signup_button).perform()
    signup_button.click()

    print('Create email...')
    email = EmailManager.create_email_address()

    print('Fill input field...')
    email_input_field = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
    action.move_to_element(email_input_field).perform()
    email_input_field.click()
    for char in email:
        time.sleep(random.uniform(0.1, 0.9))
        email_input_field.send_keys(char)

    print('Click submit button...')
    continue_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    time.sleep(3)
    action.move_to_element(continue_button).perform()
    continue_button.click()

    print('Wait until email received...')
    attempt = 0
    while attempt < 1:
        attempt += 1
        time.sleep(10)
        EmailManager.get_last_emails()

finally:
    time.sleep(30)
    save_page_source(source=driver.page_source)
    driver.quit()
