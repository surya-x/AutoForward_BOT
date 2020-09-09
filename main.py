import selenium
from app.modules import *

driver = connecting_with_whatsapp()

# Fetching data from Excel/File:
to_forward = r"Only us"
employee_prefix = r"EMP"
client_prefix = r"CLT"

# Data Fetched...

check_unread_from_these(driver, employee_prefix, client_prefix)