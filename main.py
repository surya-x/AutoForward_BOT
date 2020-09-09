from app.modules import *

driver = connecting_with_whatsapp()

# Fetching data from Excel/File:
to_forward = r"Only us"
employee = r"EMP"
client = r"CLT"

ss_path = str(os.getcwd()) + r"/app/screenshots/"
# Data Fetched...

check_unread_from_these(driver, ss_path, employee, client)

send_ss(driver, ss_path, to_forward)

sleep(randint(4, 7))
