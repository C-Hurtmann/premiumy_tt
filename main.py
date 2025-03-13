import argparse
import random
import time
from typing import Callable, Literal
from faker import Faker
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import chromedriver_autoinstaller
from email_manager import EmailManager
from contextlib import contextmanager

from config import Config


fake = Faker()


website = 'https://www.valr.com/en/signup'


class FlowControl:

    def __init__(self, driver):
        self.driver = driver

    @classmethod
    @contextmanager
    def start_driver(cls):
        chromedriver_autoinstaller.install()
        options = Config.setup()
        instance = cls(
                driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                options=options)
        )
        try:
            yield instance
    
        except Exception as e:
            print('EXCEPTION OCCURED')
            with open('page.html', 'w') as f:
                f.write(instance.driver.page_source)
            raise e

        finally:
            instance.driver.quit()

    def go_to(self, url: str, close_modal_pages: bool = False) -> None:
        self.driver.get(url)
        if close_modal_pages:
            time.sleep(3)
            starting_page_handle = self.driver.current_window_handle
            for handle in self.driver.window_handles:
                if handle != starting_page_handle:
                    self.driver.switch_to.window(handle)
                    self.driver.close()

            self.driver.switch_to.window(starting_page_handle)

    def get_element(
            self,
            by: By,
            selector: str,
            waiting_time: int = 20,
            locator_func: Callable = EC.presence_of_element_located,
        ) -> WebElement:
        if element := WebDriverWait(
            self.driver, waiting_time
        ).until(locator_func((by, selector))):
            return element
        raise KeyError(f'Selector {selector} not found')

    def scroll(self, direction: Literal['up', 'down']) -> None:
        point_1, point_2 = (0, 500) if direction == 'down' else (500, 0)
        self.driver.execute_script(f'window.scrollBy({point_1}, {point_2});')


def main(first_name, last_name, email, phone_number):
    password = 'b8Y$k2xL!eQ@7wZ9'
    with FlowControl.start_driver() as fc:
        print('Step 1: Get signup page')
        fc.go_to(website, close_modal_pages=True)

        print('Step 2: fill input fields')
        fc.get_element(By.NAME, 'firstName').send_keys(first_name)
        fc.get_element(By.NAME, 'lastName').send_keys(last_name)
        fc.get_element(By.NAME, 'email').send_keys(email)
        fc.get_element(By.NAME, 'password').send_keys(password)
        fc.scroll('down')

        print('Step 3: Resolve captcha')
        fc.get_element(By.CSS_SELECTOR, '.captcha-solver_inner', waiting_time=30).click()
        submit_button = fc.get_element(
            By.CSS_SELECTOR, 'button[type="submit"]',
            waiting_time=160,
            locator_func=EC.element_to_be_clickable
        )

        print('Step 4: Click submit')
        now = int(time.time())
        submit_button.click()

        print('Step 5: Verify account')
        mid = EmailManager.get_target_message(from_=now)['mid']
        verification_link = EmailManager.get_verification_link(mid=mid)
        fc.go_to(verification_link)
        fc.get_element(
            By.XPATH, '//a[contains(@href, "signin")]',
            locator_func=EC.element_to_be_clickable
        ).click()

        print('Step 6: Sign in')
        email_field = fc.get_element(By.NAME, 'email')
        email_field.clear()
        email_field.send_keys(email)
        fc.get_element(By.NAME, 'password').send_keys(password)
        fc.get_element(By.CSS_SELECTOR, '.captcha-solver_inner', waiting_time=30).click()
        fc.get_element(
            By.CSS_SELECTOR, 'button[type="submit"]',
            waiting_time=160,
            locator_func=EC.element_to_be_clickable
        ).click()

        print('Step 7: Fill phone number amd submit')
        fc.get_element(By.CSS_SELECTOR, 'input.PhoneInputInput').send_keys(phone_number)
        fc.get_element(
            By.CSS_SELECTOR, 'button[type="submit"]',
            locator_func=EC.element_to_be_clickable
        ).click()
        fc.get_element(By.XPATH, '//span[text()="SMS"]').click()

        print('Step 8: Check verify phone number title')
        time.sleep(5)
        check_element = fc.get_element(By.XPATH, '//p[contains(@class, "styles__Title")]')
        print(check_element.text)
        assert check_element.text == 'Verify mobile number'
        
        print('SUCCESS')
        fc.driver.get_screenshot_as_file('success.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script with arguments')
    parser.add_argument('--phone', type=str, help='Enter phone without country code (+359). Try number starts with 087')
    args = parser.parse_args()

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = EmailManager.create_email_address()
    if args.phone:
        phone_number = args.phone
    else:
        phone_number =  '087' + str(random.randint(1000000, 9999999))
        
    main(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number
    )