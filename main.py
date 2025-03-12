import random
import re
import time
from faker import Faker
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from chromedriver_autoinstaller import install
from email_manager import EmailManager
from extention import proxies
from twocaptcha_extension_python import TwoCaptcha


fake = Faker()

first_name = fake.first_name()
last_name = fake.last_name()

email_manager = EmailManager(first_name=first_name, last_name=last_name)
email = email_manager.create_email_address()
print('EMAIL GENERATED ', email)

username = 'IKUmhvPAcfZzlVIN'
password = 'mobile;bg;;;'
endpoint = 'proxy.soax.com'
port = '9000'
website = 'https://www.valr.com/en/signup'


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(TwoCaptcha("806126af0f402f205c1e49ffc88865f2").load())

proxies_extension = proxies(username, password, endpoint, port)

chrome_options.add_extension(proxies_extension)

chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(chrome, 20)

try:
    print('Step 1: Get signup page')
    chrome.get(website)
    time.sleep(5)
    starting_page_handle = chrome.current_window_handle
    for handle in chrome.window_handles:
        if handle != starting_page_handle:
            chrome.switch_to.window(handle)
            chrome.close()

    chrome.switch_to.window(starting_page_handle)

    print('Step 2: find input fields')
    first_name_field = wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
    last_name_field = wait.until(EC.presence_of_element_located((By.NAME, "lastName")))
    email_address_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    print('Step 3: fill input fields')
    first_name_field.send_keys(first_name)
    last_name_field.send_keys(last_name)
    email_address_field.send_keys(email)
    password_field.send_keys(password)
    chrome.execute_script("window.scrollBy(0, 500);")

    print('Step 4: Resolve captcha')
    WebDriverWait(chrome, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".captcha-solver_inner"))
    ).click()
    submit_button = WebDriverWait(chrome, 160).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )

    print('Step 5: Click submit')
    now = int(time.time())
    submit_button.click()

    print('Step 6: Get verification message')
    mid = email_manager.get_target_message(from_=now)['mid']

    print('Step 7: Get verification link')
    verification_link = email_manager.get_verification_link(mid=mid)
    print(verification_link)

    print('Step 8: Verify account')
    chrome.get(verification_link)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "signin")]'))).click()

    print('Step 9: Sign in')
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(email)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
    WebDriverWait(chrome, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".captcha-solver_inner"))
    ).click()
    submit_button = WebDriverWait(chrome, 160).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    ).click()

    print('Step 10: Fill phone number amd submit')
    phone_number = '087' + str(random.randint(1000000, 9999999))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.PhoneInputInput'))).send_keys(phone_number)
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    ).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="SMS"]]'))).click()

    print('Step 11: Check verify phone number title')
    check_element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[@class="styles__Title-eUrGdR"]')))
    assert check_element.text == 'Verify mobile number'
    

finally:
    time.sleep(100)
    parser = etree.HTMLParser(remove_blank_text=True)
    tree = etree.ElementTree(etree.HTML(chrome.page_source, parser))
    with open('src.xml', 'wb') as f:
        tree.write(f, pretty_print=True, encoding='utf-8', xml_declaration=True)

    chrome.quit()