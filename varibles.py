import sys
from constans import ADMIN
if len(sys.argv) > 1:
    if sys.argv[1] == "t":
        print("Test mode")

spool_path = "/var/spool/sms/"
incoming_path = spool_path+"incoming"
outgoing_path = spool_path+"outgoing"
send_path = spool_path+"sent"
checked_path = spool_path+"checked_sms"
admin_number = ADMIN["NUMBER"]
sms_log = "/home"
test = True
if len(sys.argv) > 1:
    if sys.argv[1] == "t":
        print("Test mode")
        test = True



text = """To: {number}
Flash: {flash}
Report: yes
Alphabet: UTF-8

{strings}
"""

sql_check = "SELECT COUNT(`id`) FROM wp_sms WHERE `status` = 0 "
sql_update = "UPDATE `wp_sms` SET `status`='{status}',`data_w`='{data_w}' WHERE `id` = '{id}'"
sql_get = "SELECT `id`, `numer`, `tresc` FROM wp_sms WHERE `status` = 0 ORDER BY `id` LIMIT 1"
connection_counter = 0
miejsca = {"LISZNA":"goo.gl/maps/Ga17yTemvAUYanvU6",
           "MIĘDZYBRODZIE": "goo.gl/maps/oc1Zrd77McQ2",
           "MRZYGŁÓD": "goo.gl/maps/MbxQtFTya7G2",
           "MIEDZYBRODZIE": "goo.gl/maps/oc1Zrd77McQ2",
           "MRZYGLOD": "goo.gl/maps/MbxQtFTya7G2",
           "SANOK":"goo.gl/maps/TNxBkUxxebxtRUrJ8"
           }