from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from random import randint
from datetime import datetime

import os
import logging


def connecting_with_whatsapp():
    logging.info("Connecting with whatsapp")
    options = Options()

    # options.add_argument(
    #      r"user-data-dir=C:\Users\chief_surya01\AppData\Local\Google\Chrome\User Data")
    options.add_argument(
         r"user-data-dir=/home/surya/.config/google-chrome")

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


def check_unread_from_these(driver, directory, employee, client):
    logging.info("Check unread msgs for these called : ")

    allcontacts = driver.find_elements_by_xpath(
        ''' //*[@id="pane-side"]/div[1]/div/div/div''')

    i = 1
    for each in allcontacts:
        stringlist = each.text.split("\n")
        name = stringlist[0]
        code = name.split()[0]

        if code == employee or code == client:                                            # prefix matches with the name
            if len(stringlist) > 3:                                                       # unread msgs present
                if stringlist[3] != ":" or stringlist[3] != ": ":                         # if not muted chat

                    click_xpath = ''' //*[@id="pane-side"]/div[1]/div/div/div[''' + str(i) + "]"
                    driver.find_element_by_xpath(click_xpath).click()

                    filename = directory + str(datetime.now()) + ".png"
                    sleep(randint(3, 6))
                    driver.save_screenshot(filename)                                      # saving the ss
                    sleep(randint(2, 5))

                    logging.info("screenshot taken for contact " + name)
        i += 1


# This method is used to type the parameter given to function into search
# bar of Whatsapp and will open the chat
def search_bar(driver, parameter):
    logging.info("search_bar called: ")
    try:
        search = driver.find_element_by_xpath(
            '''//*[@id="side"]/div[1]/div/label/div/div[2]''')
        search.clear()
        search.send_keys(parameter, Keys.RETURN)
        # sleep is used to delay the scripts for 2-4 seconds
        sleep(randint(2, 5))

    except NoSuchElementException as e:
        logging.error("NoSuchElementException found in search_bar")
        logging.error(e)
    except Exception as e:
        logging.error("Exception found in search_bar")
        logging.error(e)


# This method is used to send the image to a chat which is already opened.
def send_img(driver, imgpath):
    logging.info("Sending image to open chats: ")
    try:

        # sleep is used to delay the scripts for 1-3 seconds
        sleep(randint(1, 4))
        driver.find_element_by_css_selector("span[data-icon = 'clip']").click()

        # sleep is used to delay the scripts for 1-3 seconds
        sleep(randint(1, 4))
        driver.find_element_by_css_selector(
            "input[type='file']").send_keys(imgpath)

        send = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span[data-icon='send']"))
        )
        # sleep is used to delay the scripts for 1-2 seconds
        sleep(randint(1, 3))
        send.click()
        logging.info("Image sent!!!\n")
    except NoSuchElementException as e:
        logging.error("NoSuchElementException found in send_img")
        logging.error(e)
    except Exception as e:
        logging.error("Exception found in send_img")
        logging.error(e)


def send_ss(driver, directory, tosend):
    logging.info("Sending screenshot to contacts: ")
    try:
        search_bar(driver, tosend)
        for each in os.listdir(directory):
            # sleep is used to delay the scripts for 2-4 seconds
            sleep(randint(2, 5))
            filename = os.path.join(directory, each)
            send_img(driver, filename)

    except Exception as e:
        logging.error("Exception found in send_ss")
        logging.error(e)
