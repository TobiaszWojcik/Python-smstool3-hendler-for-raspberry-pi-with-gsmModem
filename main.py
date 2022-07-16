import mysql.connector
import time
from os import system
import atexit
from varibles import *
from check_modem import check_modem_status, check_incoming, update_date
from common_f import add_sms, log_error

@atexit.register
def goodbye():
    system("python /home/pi/PycharmProjects/pythonProject/main.py")

def is_integer(char):
    try:
        int(char)
        return True
    except ValueError as e:
        log_error(e)
        return False


def mark_as_delivered(id):
    mycursor.execute(sql_update.format(id=id[0], status=id[1], data_w=update_date()))

# time.sleep(30)
# system("sudo /etc/init.d/smstools restart")
while True:
    check_modem_status()
    try:
        mydb = mysql.connector.connect(
            host="bieszczadyaktywnie.atthost24.pl",
            user="13132_wp_1",
            password="BgYU0L9O",
            database="13132_wp_1",
            connection_timeout=10,
        )

        mydb.autocommit = True
        mycursor = mydb.cursor()
        # print("Serwer uruchomiony")
        log_error("Serwer uruchomiony")
        # add_sms("Serwer uruchomiony")
        while True:
            mycursor.execute(sql_check)
            myresult = mycursor.fetchall()

            try:
                if int(myresult[0][0]) > 0:

                    mycursor.execute(sql_get)
                    myresult = mycursor.fetchall()
                    sms_id = myresult[0][0]
                    sms_number = myresult[0][1]
                    if sms_number == "":
                        sms_number = admin_number
                    if len(sms_number) < 10:
                        sms_number = "+48" + sms_number
                    sms_text = myresult[0][2]
                    if is_integer(sms_text[0]):
                        sms_flash = "yes"
                    else:
                        sms_flash = "no"
                    if add_sms(sms_text, sms_number, sms_id, sms_flash):
                        print("Sms dodany!")
                        mycursor.execute(sql_update.format(id=sms_id, status=1, data_w=update_date()))

                action = check_incoming()
                if action:
                    mark_as_delivered(action)
            except Exception as e:
                log_error(e)
            time.sleep(1)
    except Exception as exception:
        log_error("problem z serwerem"+str(exception))
        add_sms(exception)

        time.sleep(60)

