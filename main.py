import configparser
import sys
from time import sleep
from loguru import logger

import keyring
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def main():
    """
        Loguru Log Levels:

        | Level name | Severity value | Logger method    |
        |------------|----------------|------------------|
        | TRACE      | 5              | logger.trace()   |
        | DEBUG      | 10             | logger.debug()   |
        | INFO       | 20             | logger.info()    |
        | SUCCESS    | 25             | logger.success() |
        | WARNING    | 30             | logger.warning() |
        | ERROR      | 40             | logger.error()   |
        | CRITICAL   | 50             | logger.critical()|
    """
    logger.remove()  # Removes the default handler, so that we can set a log level without duplicating messages.
    logger.add(sink=sys.stderr, level="TRACE")  # Configures the log handler.

    logger.info("Logger initiated!")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-data-dir=ChromeUserData')  # Creates a user profile, to remember the login.

    driver = webdriver.Chrome(chrome_options)
    driver.get('https://www.willhaben.at/iad/myprofile/myadverts')

    driver.maximize_window()
    driver.implicitly_wait(60)

    config = configparser.ConfigParser()
    config.read('config.ini')
    #
    # login = driver.find_element(By.LINK_TEXT, "Einloggen")
    # login.click()

    try:
        login_mail = driver.find_element(By.ID, "email")

        logger.info("Logging in...")
        user = keyring.get_password("willhaben-user", config.get('KEYRING', 'username'))

        login_mail.send_keys(user)

        password = keyring.get_password("willhaben-password", config.get('KEYRING', 'username'))

        login_password = driver.find_element(By.ID, "password")
        login_password.send_keys(password)

        # remember_me = driver.find_element(By.ID, "rememberMe")
        # remember_me.click()

        submit = driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
        submit.click()
    except:
        logger.warning("No login element found, there is probably an open session...")

    try:
        cookies = driver.find_element(By.ID, "didomi-notice-agree-button")
        cookies.click()
    except:
        logger.warning("Cookies not found.")

    # //button[@name='republish']

    # filter-status-select

    status = Select(driver.find_element(By.ID, 'filter-status-select'))
    status.select_by_visible_text("Abgelaufen")

    is_item_available = True
    while is_item_available:
        try:
            republish = driver.find_element(By.XPATH, '//button[@name="republish"][1]')
            republish.click()

            sleep(0.5)

            item_name = driver.find_element(By.ID, 'heading')
            logger.info("Republish Item... {s}", s=item_name.get_attribute("value"))

            submit = driver.find_element(By.XPATH, '//button[@data-testid="send-button"]')
            submit.click()

            sleep(0.5)

            submit = driver.find_element(By.XPATH, '//button[@data-testid="submitButton"]')
            submit.click()

            sleep(0.5)

            submit = driver.find_element(By.XPATH, '//button[@data-testid="submit-button"]')
            submit.click()

            sleep(0.5)

            meine_anzeigen = driver.find_element(By.LINK_TEXT, "Meine Anzeigen")
            meine_anzeigen.click()

            sleep(0.5)
        except:
            logger.warning("Something went wrong during republishing...")
            is_item_available = False

    logger.info("Done! Closing Browser...")

    driver.quit()

if __name__ == "__main__":
    main()
