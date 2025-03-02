from command_parser import *
from client_utils import *

# Create a command to key off of
SMS_COMMAND = '/msg'

# Create the intended parser arguments
sms_parser = argparse.ArgumentParser(description="Commands for sms commands")
sms_parser.add_argument('command', type=str, help = 'Must be /msg')
sms_parser.add_argument('to', type=str, help = 'Name of person to send message to')
sms_parser.add_argument('message', type=str, help = 'The message to send')

# Once parser is selected and disassembled what happens
def handle_sms(client_transport, input_args):
    try:
        arguments = sms_parser.parse_args(input_args)
    except:
        print_all(f"Error parsing arguments")
        return

    # Do whatever
    print_all(f"Sending SMS to {arguments.to}: {arguments.message}")

    try:
        to_client_ip = OTHER_CLIENT_NAME_TO_IP[arguments.to]
    except:
        print_all(f"Unknown Name {arguments.to}")
        return
    
    client_transport.send_parcel(SMS_MSG, to_client_ip, arguments.message)