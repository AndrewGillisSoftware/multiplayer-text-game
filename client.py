from client_utils import *
from comm_utils import *
from init_commands import *
import time

#SERVER = "127.0.0.1"

ct = ClientTransport(None)

def handle_server_mail(mail:MailParcel):
    # Server to Client Communication: Should be used rarely. Client 0 is source of truth
    if mail.from_address == ct.server_address:
        if mail.purpose == EMPTY_PARCEL:
            return

        # What is the server asking for
        mail_command = mail.purpose

        # Add list of IPS from the server to client information
        if mail_command == GET_ACTIVE_CLIENTS_RESPONSE:
            mail_response = mail.message
            OTHER_CLIENT_IPS.clear()
            OTHER_CLIENT_IPS.extend(eval(mail_response))
            #print(OTHER_CLIENT_IPS)

def handle_client_to_client_mail(mail:MailParcel):
    # Client to Client Communication: Prevent a Infinite Loop
    if True: #mail.to_address != mail.from_address:
        # What is the client asking for
        mail_command = mail.purpose

        # Request from a client to get this clients name sent back to it
        #print(mail_command)
        if mail_command == GET_CLIENT_NAME:
            # Send Name to the requesting address
            ct.send_parcel(GET_CLIENT_NAME_RESPONSE, mail.from_address, get_client_name())
        
        elif mail_command == GET_CLIENT_NAME_RESPONSE:
            # We recieved a response from our name request assign them to our table of known users
            mail_response = mail.message
            # Add to other clients
            OTHER_CLIENT_NAME_TO_IP[mail_response] = mail.from_address
            #print(OTHER_CLIENT_NAME_TO_IP)
        elif mail_command == SMS_MSG:
            print(f"SMS:{get_other_client_name(mail.from_address)}: {mail.message}")
        
        else:
            "Unknown client mail command"

def discover_other_clients(ct):
    discovering_ips = False
    while True:
        # Ensure connection
        if not ct.connected:
            continue

        # Discover Ips
        if not discovering_ips:
            discover_other_client_ips(ct)
            discovering_ips = True

        # Ensure Ips were grabbed
        if len(OTHER_CLIENT_IPS) == 0:
            continue

        #print("Discovering Clients - GOT IPS")
        # Discover Names
        discover_other_client_names(ct)

        time.sleep(10)
        discovering_ips = True

def check_for_mail(ct):
    while True:
        time.sleep(0.5)
        if ct.connected:
            parcel = ct.get_next_parcel()
            if parcel.purpose != EMPTY_PARCEL:
                handle_server_mail(parcel)
                handle_client_to_client_mail(parcel)
                #print(parcel)


# Start Checking for mail
check_for_mail_thread = threading.Thread(target=check_for_mail, args=(ct,))
check_for_mail_thread.start()

discover_other_clients_thread = threading.Thread(target=discover_other_clients, args=(ct,))
discover_other_clients_thread.start()

while True:
    user_input = input("Enter Command: ")
    parse(ct, user_input)
