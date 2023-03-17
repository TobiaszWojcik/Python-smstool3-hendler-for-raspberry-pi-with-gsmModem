import os
import datetime
from varibles import *
from common_f import add_sms, log_error, print_test, send_email


def update_date():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def check_modem_status():
    status = str(os.popen("/etc/init.d/smstools status").read())
    status = status.splitlines()[2].split(": ")[1].split(" ")[0]
    print(status)
    if status == "inactive":
        send_email("Raspberry PI", "Restart Modemu")
        print("Restart smstools")
        log_error("Restart smstools")
        os.system("sudo /etc/init.d/smstools restart")


def check_incoming():
    sms_list = os.listdir(incoming_path)
    sms_sended_list = os.listdir(send_path)
    if len(sms_list) > 0:
        incoming_sms_counter = 0
        print_test(sms_list)
        for sms in sms_list:
            incoming_sms_counter += 1
            sms_from = ''
            sms_text = ''
            sms_id = None
            sms_status = None
            with open(incoming_path+"/"+sms, 'r') as incoming_sms:
                print_test("sprawdzanie plików")
                for line in incoming_sms:
                    line = (line.strip()).split(': ')
                    if len(line) == 1:
                        sms_text+= line[0]
                    elif line[0] == "From":
                        sms_from = line[1]
                    elif line[0] == "Message_id":
                        sms_id = line[1]
                    elif line[0] == "Status":
                        sms_status = line[1]
            print_test((sms_text, sms_from, sms_status))
            print_test(sms_from.find(admin_number))
            if not sms_status:
                if not sms_from.find(admin_number):

                    os.popen("sudo mv {incoming}/{name} {outgoing}/{name}".format(incoming=incoming_path, name=sms,
                                                                                  outgoing=checked_path))
                    print("\n\n\n\n{}\n\n\n\n".format(sms_text))
                    if not sms_text.upper().find("RESTART"):
                        os.system("sudo shutdown now -r")
                        break
                    elif not sms_text.upper().find("TEST"):
                        add_sms(os.popen("vcgencmd measure_temp").read())
                        break
                    elif not sms_text.upper().find("SUDO_DO:"):
                        print_message = os.popen(sms_text[8:]).read()
                        print(sms_text[8:])
                        log_error("made without feedback {} on Raspberry".format(sms_text))
                        break
                    elif not sms_text.upper().find("SUDO_EMAIL:"):
                        log_error("emailed feedback {} to admin".format(sms_text))
                        email_message = os.popen(sms_text[11:]).read()
                        send_email("Raspberry Modem CallBack", email_message)
                        break
                    elif not sms_text.upper().find("SUDO_SMS:"):
                        log_error("send feedback by sms {} to admin".format(sms_text))
                        sms_message = os.popen(sms_text[9:]).read()
                        add_sms(sms_message)
                        break
                if sms_text.upper().strip() in miejsca.keys():
                    print_test("żądanie miejsca")
                    if(add_sms("Przystań {}: {}".format(sms_text, miejsca[sms_text.upper()]), sms_from,
                            datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f') + str(incoming_sms_counter))):
                        os.popen("sudo mv {incoming}/{name} {outgoing}/{name}".format(incoming=incoming_path, name=sms, outgoing=checked_path))
                elif add_sms(sms_text+" From: "+sms_from, admin_number, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')+str(incoming_sms_counter)):
                    os.popen("sudo mv {incoming}/{name} {outgoing}/{name}".format(incoming=incoming_path, name=sms, outgoing=checked_path))
            else:
                sms_send_id = None
                for sms_send in sms_sended_list:
                    sms_send_id = None
                    with open(send_path + "/" + sms_send, 'r') as sended_sms:

                        for line in sended_sms:
                            line = (line.strip()).split(': ')
                            if line[0] == "Message_id":
                                sms_send_id = line[1]
                                print_test(sms_send_id)
                                break
                    if sms_id == sms_send_id:
                        temp_sms_id = sms_send.split('.')[1]
                        os.popen("sudo mv {from_sms}/{name} {to_sms}/modem1.{name_sms}".format(from_sms=incoming_path, name=sms ,name_sms = temp_sms_id, to_sms = checked_path))
                        os.popen(
                            "sudo mv {from_sms}/{name} {to_sms}/{name}".format(from_sms=send_path, name=sms_send,
                                                                                       to_sms=checked_path))

                        if len(temp_sms_id) < 10:

                            if sms_status == "0,Ok,short message received by the SME":
                                return [temp_sms_id, 2]
                            else:
                                return [temp_sms_id, 3]
                        return None
                os.popen("sudo rm {from_sms}/{name}".format(from_sms=incoming_path, name=sms))

    else:
        return None
