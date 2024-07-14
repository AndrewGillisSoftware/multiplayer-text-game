from comm_utils import *
from init_commands import *
import time

#SERVER = "127.0.0.1"

ct = ClientTransport(None)

def check_for_mail(ct):
    while True:
        time.sleep(0.5)
        if ct.server_address:
            parcel = ct.get_next_parcel()
            if parcel.message != EMPTY_PARCEL:
                print(parcel)


thread = threading.Thread(target=check_for_mail, args=(ct,))
thread.start()

while True:
    user_input = input("Enter Command: ")
    parse(ct, user_input)
