from app.modules import *
from app.config import logging

logging.info("\nProgram started from here.")
driver = connecting_with_whatsapp()

# Fetching data from Excel/File:
to_forward = r"Only us"
employee = r"EMP"
client = r"CLT"

ss_path = os.path.join(os.getcwd(), "app", "screenshots")
ss_path = ss_path + os.sep
# Data Fetched...

check_unread_from_these(driver, ss_path, employee, client)

send_ss(driver, ss_path, to_forward)
print("Successfully send the screenshots!!!...")

sleep(randint(7, 10))
delete_ss(ss_path)
logging.info("\nProgram ended here.\n")
