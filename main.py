from app.modules import *
from app.config import logging

logging.info("\nProgram started from here.")
driver = connecting_with_whatsapp()

# Fetching data from Excel/File:
to_forward, pause_time = retrieve_file_parameter()
pause_time = int(pause_time)
employee = r"EPL"
client = r"CLT"

ss_path = os.path.join(os.getcwd(), "app", "screenshots")
ss_path = ss_path + os.sep
# Data Fetched...

while True:
    logging.info("\nWhile Loop started here.\n")
    # Deleting already exsisting screenshots.
    delete_ss(ss_path)

    check_unread_from_these(driver, ss_path, employee, client)

    send_ss(driver, ss_path, to_forward)
    print("Successfully send the screenshots!!!...")

    sleep(randint(7, 10))

    logging.info("\nWhile Loop ended here.\n")
    logging.info("\n\nWaiting for " + str(pause_time) + " minutes to re-run the bot.\n\n")

    print("\n\nWaiting for next " + str(pause_time) + " minutes to re-run the bot automatically.")
    print("Esperando los próximos " + str(pause_time) + " minutos para volver a ejecutar el bot automáticamente.\n\n")

    sleep(pause_time*60)
    print("Staring the loop process again.\n\n")
