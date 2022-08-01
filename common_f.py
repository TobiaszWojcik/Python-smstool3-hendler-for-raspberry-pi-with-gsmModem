import datetime
import random
from varibles import admin_number, text, test


def add_sms(sms_text, sms_number = admin_number, sms_id = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f'), sms_flash = "no"):
    try:
        # if()
        with open("/var/spool/sms/outgoing/out.{}".format(sms_id), 'w', encoding='utf-8') as sms:
            sms.write(text.format(number=sms_number, strings=sms_text, flash=sms_flash))
            log_sms("{} - {} - {}\n".format(datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'), sms_number, sms_text))
            # print("{} - {} - {}".format(sms_id, sms_number, sms_text))
        return True
    except Exception as exception_send_error:
        log_error(exception_send_error)
        return False


def log_error(e):
    try:
        with open('/home/pi/Logs/error.log', 'a+') as file:
            file.write("{} - {}\n".format(datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'), e))
    except Exception as er:
        try:
            with open('/home/pi/Logs/error_open.log', 'a+') as file:
                file.write(er)
        except Exception as err:
            print(err)


def log_sms(e):
    try:
        with open('/home/pi/Logs/sms.log', 'a') as file:
            file.write(e)
    except Exception as er:
        log_error(er)

def print_test(string):
    if test:
        print (string)