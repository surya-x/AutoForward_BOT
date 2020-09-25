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

import sys
import os
import logging
import openpyxl


def connecting_with_whatsapp():
    logging.info("Connecting with whatsapp called : ")
    print("BOT Is Connecting with Whatsapp\n...")

    try:
        options = Options()

        # options.add_argument(
        #      r"user-data-dir=C:\Users\chief_surya01\AppData\Local\Google\Chrome\User Data")
        # options.add_argument(
        #      r"user-data-dir=/home/surya/.config/google-chrome")
        # driver = webdriver.Chrome(chrome_options=options)

        driver = webdriver.Chrome()

        # print("Please scan the QR code if prompted to login into Whatsapp")
        driver.get("https://web.whatsapp.com")

        # To wait until the page loads
        element = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located(
                (By.XPATH, ''' //*[@id="pane-side"]/div[1]/div/div/div '''))
        )
    except TimeoutException:
        logging.error("Failed logging Whatsapp \nStart again...")
        print("Failed logging into Whatsapp \nPlease Start again...")
        os.system("PAUSE")
        sys.exit()
    except NoSuchElementException:
        logging.error("NoSuchElementException found..")
        print("Please Try again after sometime \nIf it's not working even after some time "
              "please contact developer.")
        os.system("PAUSE")
        sys.exit()
    except Exception as e:
        logging.error("Exception found in connecting_with_whatsapp")
        logging.error(e)
        os.system("PAUSE")
        sys.exit()
    else:
        logging.info("QR code scanned, You are logged into Whatsapp")
        logging.info("returning driver successfully..")

    return driver


# To give the all the details in "parameter.xlsx"
def retrieve_file_parameter():
    logging.info("retrieve file parameter called")
    try:
        path = os.path.join(os.getcwd(), "parameters.xlsx")
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.worksheets[0]

        number = sheet["A2"].value

        return number
    except Exception as e:
        print("\nError : loading data from parameters.xlsx")
        print(e)
        logging.error(e)
        os.system("PAUSE")
        sys.exit()

# This method is used to type the parameter given to function into search
# bar of Whatsapp and will open the chat
def search_bar(driver, parameter):
    logging.info("search_bar called with parameter : " + parameter)
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
        os.system("PAUSE")
        sys.exit()
    except Exception as e:
        logging.error("Exception found in search_bar")
        logging.error(e)
        os.system("PAUSE")
        sys.exit()


def check_unread_from_these(driver, directory, employee, client):
    logging.info("Check unread msgs for these called : ")
    print("Checking for unread messages for employees & clients,\n"
          "\t& taking the screenshots if found")

    try:
        allcontacts_object = driver.find_elements_by_xpath(
            ''' //*[@id="pane-side"]/div[1]/div/div/div''')

        all_contacts = []
        for each1 in allcontacts_object:
            all_contacts.append(each1.text)

        for each in all_contacts:
            stringlist = each.split("\n")
            name = stringlist[0]
            code = name.split()[0]

            if code == employee or code == client:                      # prefix matches with the name
                if len(stringlist) > 3:                                 # unread msgs present
                    if stringlist[3] != ":" or stringlist[3] != ": ":   # if not muted chat
                        search_bar(driver, name)
                        dt_string = datetime.now().strftime("%dd%mm%Yy%H%M%S")
                        filename = directory + dt_string + ".png"
                        sleep(randint(2, 5))
                        driver.save_screenshot(filename)                # saving the ss
                        sleep(randint(3, 5))

                        logging.info("screenshot taken for contact : " + name +
                                     ", with filename : " + filename)
    except NoSuchElementException:
        logging.error("NoSuchElementException found..")
        print("Please Try again after sometime \nIf it's not working even after some time "
              "please contact developer.")
        os.system("PAUSE")
        sys.exit()
    except Exception as e:
        logging.error("ERROR FOUND IN CHECK UNREAD MSGS...")
        logging.error(e)


# This method is used to send the image to a chat which is already opened.
def send_img(driver, imgpath):
    logging.info("Sending image to open chats: ")

    try:
        # sleep is used to delay the scripts for 1-3 seconds
        sleep(randint(2, 4))
        driver.find_element_by_css_selector("span[data-icon = 'clip']").click()

        # sleep is used to delay the scripts for 1-3 seconds
        sleep(randint(2, 4))
        driver.find_element_by_css_selector(
            "input[type='file']").send_keys(imgpath)

        send = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span[data-icon='send']"))
        )
        # sleep is used to delay the scripts for 1-2 seconds
        sleep(randint(1, 3))
        send.click()
        logging.info("Image sent!!!\n")
    except NoSuchElementException:
        logging.error("NoSuchElementException found..")
        print("Please Try again after sometime \nIf it's not working even after some time "
              "please contact developer.")
        os.system("PAUSE")
        sys.exit()
    except Exception as e:
        logging.error("Exception found in send_img")
        logging.error(e)
        os.system("PAUSE")
        sys.exit()


def send_ss(driver, directory, tosend):
    tosend = str(tosend)
    logging.info("Sending the screenshot to contacts: " + str(tosend) )
    print("Sending the screenshots to contact listed")
    try:
        search_bar(driver, tosend)

        for each in os.listdir(directory):
            image_format = each.split(".")[-1]

            if image_format == "png" or image_format == "bmp" or image_format == "jpg" or image_format == "jpeg":
                filename = os.path.join(directory, each)
                send_img(driver, filename)
                # sleep is used to delay the scripts for 2-4 seconds
                sleep(randint(3, 8))

    except Exception as e:
        logging.error("Exception found in send_ss")
        logging.error(e)
        os.system("PAUSE")
        sys.exit()


def delete_ss(directory):
    try:
        os.chdir(directory)
        for each in os.listdir():
            image_format = each.split(".")[-1]
            if image_format == "png" or image_format == "bmp" or image_format == "jpg" or image_format == "jpeg":
                os.remove(each)
                logging.info("Deleted image named :- "+str(each))
    except Exception as e:
        logging.error("ERROR FOUND WHILE DELETING SS..")
        logging.error(e)
        print("NOTE : DUE TO INTERNAL ERROR SCREENSHOTS TAKEN AREN'T DELETED\n"
              "PLEASE FIND THE FOLDER SCREENSHOTS IN APP FOLDER, "
              "AND DELETE ALREADY TAKEN SCREENSHOTS TO AVOID TROUBLE IN NEXT RUN\n"
              "\n\t IF THE PROBLEM CONTINUES, CONTACT DEVELOPER.")
