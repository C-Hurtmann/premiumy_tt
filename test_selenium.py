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

username = 'IKUmhvPAcfZzlVIN'
password = 'mobile;bg;;;'
endpoint = 'proxy.soax.com'
port = '9000'
website = 'https://www.valr.com/en/signup'


def save_page_source(source: str) -> None:
    parser = etree.HTMLParser(remove_blank_text=True)
    tree = etree.ElementTree(etree.HTML(source, parser))

    with open('src.xml', 'wb') as f:
        tree.write(f, pretty_print=True, encoding='utf-8', xml_declaration=True)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(TwoCaptcha("806126af0f402f205c1e49ffc88865f2").load())

proxies_extension = proxies(username, password, endpoint, port)

chrome_options.add_extension(proxies_extension)

chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(chrome, 20)

try:
    print('Step 1: Get signup page')
    chrome.get(website)

    print('Step 2: find input fields')
    first_name_field = wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
    last_name_field = wait.until(EC.presence_of_element_located((By.NAME, "lastName")))
    email_address_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    print('Step 3: fill input fields')
    first_name_field.send_keys(first_name)
    last_name_field.send_keys(last_name)
    email_address_field.send_keys(email)
    password_field.send_keys('G$9vL2@xM!b3#Z7q')
    chrome.execute_script("window.scrollBy(0, 500);")

    print('Step 4: Resolve capcha')
    captcha_solver = WebDriverWait(chrome, 30).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".captcha-solver_inner"))
    )
    captcha_solver.click()


    print('Step 5: Click submit')
    WebDriverWait(chrome, 160).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    ).click()

finally:
    time.sleep(50)
    save_page_source(chrome.page_source)
    chrome.quit()