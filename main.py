from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def handler(event=None, context=None):
    url = event['url']
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--enable-javascript')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome("/opt/chromedriver", options=options)
    driver.get(url)
    element = WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.CLASS_NAME, 'notificationMessage')))
    notification = driver.find_element(By.CLASS_NAME, 'notificationMessage')
    if notification:
        print(f'[*] Found "Notification", text is {notification.text}')
        result = 'success'
    else:
        print('[!] Notification is not present!')
        result = 'failed'

    time.sleep(1)
    driver.quit()

    return {'result': result, 'html': driver.find_element(by=By.XPATH, value="//html").text}
