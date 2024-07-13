from comm_utils import *
from commands.command_parser import *

SERVER = "192.168.99.41"
IP = socket.gethostbyname(socket.gethostname())

def parse_command(command):
    return

ct = ClientTransport(SERVER, None)
ct.connect(SERVER)

while True:
    command = input("Enter Command: ")

    # /msg_IP_
    parts = command.split('_')

    match parts[0]:
        case "/msg":
            match parts[1]:
                case "BROADCAST":
                    print("NOT SUPPORTED")
                case _:
                    # must be IP
                    ip_to_send_to = parts[1]
                    message_to_send = parts[2]
                    sms = ParcelSmsString(str(IP), message_to_send)
                    response = ct.send_parcel_and_get_response(ip_to_send_to, sms)
        case "/ping":
            response = ct.send_parcel_and_get_response(SERVER, ParcelPing())
                    
        case "/disconnect":
            ct.disconnect()
        case _:
            print("INVALID COMMAND")
