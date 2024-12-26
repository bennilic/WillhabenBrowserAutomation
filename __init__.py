import configparser
from time import sleep

import keyring
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-data-dir=ChromeUserData')

driver = webdriver.Chrome(chrome_options)
driver.get('https://www.willhaben.at/iad/myprofile/myadverts')

driver.maximize_window()
driver.implicitly_wait(10)

config = configparser.ConfigParser()
config.read('config.ini')

# cookies = driver.find_element(By.ID, "didomi-notice-agree-button")
# cookies.click()
#
# login = driver.find_element(By.LINK_TEXT, "Einloggen")
# login.click()

user = keyring.get_password("willhaben-user", config.get('KEYRING', 'username'))

login_mail = driver.find_element(By.ID, "email")
login_mail.send_keys(user)

password = keyring.get_password("willhaben-password", config.get('KEYRING', 'username'))

login_password = driver.find_element(By.ID, "password")
login_password.send_keys(password)

# remember_me = driver.find_element(By.ID, "rememberMe")
# remember_me.click()

submit = driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
submit.click()

# //button[@name='republish']


sleep(10)

driver.quit()