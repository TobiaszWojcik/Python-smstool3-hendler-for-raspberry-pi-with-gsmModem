import os, datetime
from varibles import *
from common_f import add_sms, log_error

def update_date():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def check_modem_status():
    status = str(os.popen("/etc/init.d/smstools status").read())
    status = status.splitlines()[2].split(": ")[1].split(" ")[0]
    if status == "inactive":
        log_error("Restart smstools")
        os.system("sudo /etc/init.d/smstools restart")



def check_incoming():
    # print("chceck uruchomiony")

    sms_list = os.listdir(incoming_path)
    sms_sended_list = os.listdir(send_path)
    # print(sms_list)
    if len(sms_list) > 0:
        incoming_sms_counter = 0
        for sms in sms_list:
            incoming_sms_counter += 1
            sms_from = ''
            sms_text = ''
            sms_id = None
            sms_status = None
            with open(incoming_path+"/"+sms, 'r') as incoming_sms:
                # print("sprawdzanie plików")
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
            # print(sms_text, sms_from, sms_status)
            if not sms_status:
                # print("ponowne wysyłanie do admina")
                if add_sms(sms_text+" From: "+sms_from, admin_number, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')+str(incoming_sms_counter)):
                    # print("przenoszenie pliku")
                    os.popen("sudo mv {incoming}/{name} {outgoing}/{name}".format(incoming=incoming_path, name=sms, outgoing=checked_path))
            else:
                # print("to są statusy")
                sms_send_id = None
                for sms_send in sms_sended_list:
                    sms_send_id = None
                    with open(send_path + "/" + sms_send, 'r') as sended_sms:

                        for line in sended_sms:
                            line = (line.strip()).split(': ')
                            if line[0] == "Message_id":
                                sms_send_id = line[1]
                                break
                    # print(sms_id, sms_send_id)
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
