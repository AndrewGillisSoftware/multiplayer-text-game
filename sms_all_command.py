from command_parser import *
from client_utils import *

# Create a command to key off of
SMS_ALL_COMMAND = '/msg_all'

# Create the intended parser arguments
sms_all_parser = argparse.ArgumentParser(description="Commands for sms commands")
sms_all_parser.add_argument('command', type=str, help = 'Must be /msg_all')
sms_all_parser.add_argument('message', type=str, help = 'The message to send')

# Once parser is selected and disassembled what happens
def handle_sms_all(client_transport, input_args):
    try:
        arguments = sms_all_parser.parse_args(input_args)
    except:
        print_all(f"Error parsing arguments")
        return

    # Do whatever
    print_all(f"Sending SMS to Everyone: {arguments.message}")
    
    for ip in OTHER_CLIENT_IPS:
        client_transport.send_parcel(SMS_MSG, ip, arguments.message)