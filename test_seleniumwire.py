from seleniumwire import webdriver

proxy_host = "156.228.112.12"
proxy_port = "3128"

options = {
    'proxy': {
        'http': f'http://{proxy_host}:{proxy_port}',
        'https': f'https://{proxy_host}:{proxy_port}',
        'no_proxy': 'localhost,127.0.0.1'
    }
}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome(seleniumwire_options=options)

driver.get('https://www.coinbase.com/')

input()