from command_parser import *

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
    except argparse.ArgumentTypeError as e:
        print(f"Error parsing arguments: {e}")
        return

    # Do whatever
    print(f"Sending SMS to {arguments.to}: {arguments.message}")
    
    client_transport.send_parcel(arguments.to, arguments.message)