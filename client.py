from client_utils import *
from comm_utils import *
from init_commands import *
import time
import json

#SERVER = "127.0.0.1"

ct = ClientTransport(None)

def handle_server_mail(mail:MailParcel):
    # Server to Client Communication: Should be used rarely. Client 0 is source of truth
    if mail.from_address == ct.server_address:
        if mail.message == EMPTY_PARCEL:
            return

        # What is the server asking for
        segmented_message = mail.message.split(DELIMINATOR)
        mail_command = segmented_message[0]

        # Add list of IPS from the server to client information
        if mail_command == GET_ACTIVE_CLIENTS_RESPONSE:
            mail_response = segmented_message[1]
            OTHER_CLIENT_IPS.clear()
            OTHER_CLIENT_IPS.extend(json.loads(mail_response))
            print(OTHER_CLIENT_IPS)

def handle_client_to_client_mail(mail:MailParcel):
    # Client to Client Communication: Prevent a Infinite Loop
    if mail.to_address != mail.from_address:
        # What is the client asking for
        segmented_message = mail.message.split(DELIMINATOR)
        mail_command = segmented_message[0]

        # Request from a client to get this clients name sent back to it
        if mail_command == GET_CLIENT_NAME:
            # Send Name to the requesting address
            ct.send_parcel(mail.from_address, GET_CLIENT_NAME_RESPONSE + get_client_name())
        
        elif mail_command == GET_CLIENT_NAME_RESPONSE:
            # We recieved a response from our name request assign them to our table of known users
            mail_response = segmented_message[1]
            # Add to other clients
            OTHER_CLIENT_NAME_TO_IP[mail_response] = mail.from_address
            print(OTHER_CLIENT_NAME_TO_IP)
        
        else:
            "Unknown client mail command"

def block_on_condition(condition):
    while condition:
        pass

def discover_other_clients(ct:ClientTransport):
    while True:
        # Ensure connection
        block_on_condition(not ct.connected)
        # Discover Ips
        discover_other_client_ips(ct)
        # Ensure Ips were grabbed
        block_on_condition(len(OTHER_CLIENT_IPS) == 0)
        # Discover Names
        discover_other_client_names(ct)
        time.sleep(10)

def check_for_mail(ct):
    while True:
        time.sleep(0.5)
        if ct.connected:
            parcel = ct.get_next_parcel()
            if parcel.message != EMPTY_PARCEL:
                handle_server_mail(parcel)
                handle_client_to_client_mail(parcel)
                print(parcel)

def client_main_loop(ct):
    # Start Checking for mail
    check_for_mail_thread = threading.Thread(target=check_for_mail, args=(ct,))
    check_for_mail_thread.start()

    discover_other_clients_thread = threading.Thread(target=discover_other_clients, args=(ct,))
    discover_other_clients_thread.start()

thread = threading.Thread(target=client_main_loop, args=(ct,))
thread.start()

while True:
    user_input = input("Enter Command: ")
    parse(ct, user_input)
