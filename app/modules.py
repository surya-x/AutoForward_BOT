from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from random import randint
import xlrd
import logging


def connecting_with_whatsapp():
    logging.info("Connecting with whatsapp")
    # options = Options()

    # options.add_argument(
    #      r"user-data-dir=C:\Users\chief_surya01\AppData\Local\Google\Chrome\User Data")

    driver = webdriver.Chrome()

    # print("Please scan the QR code if prompted to login into Whatsapp")
    driver.get("https://web.whatsapp.com")

    try:  # To wait until the page loads
        element = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located(
                (By.XPATH, ''' //*[@id="pane-side"]/div[1]/div/div/div '''))
        )
    except TimeoutException:
        logging.error("Failed logging Whatsapp \nStart again...")
    except NoSuchElementException:
        logging.error("NoSuchElementException found..")
    except Exception as e:
        logging.error("Exception found in connecting_with_whatsapp")
        logging.error(e)
    else:
        logging.info("QR code scanned, You are logged into Whatsapp")

    return driver