from command_parser import *

# Create a command to key off of
PASSTHROUGH_COMMAND = '/passthrough'

# Create the intended parser arguments
passthrough_parser = argparse.ArgumentParser(description="Commands for passthrough commands")
passthrough_parser.add_argument('command', type=str, help = 'Must be /passthrough')
passthrough_parser.add_argument('to', type=str, help = 'Name of person to send message to')
passthrough_parser.add_argument('message', type=str, help = 'The message to send')

# Once parser is selected and disassembled what happens
def handle_passthrough(client_transport, input_args):
    try:
        arguments = passthrough_parser.parse_args(input_args)
    except:
        print(f"Error parsing arguments: {sys.exc_info()[0]}")
        return

    # Do whatever
    print(f"Sending Passthrough to {arguments.to}: {arguments.message}")
    
    client_transport.send_parcel(arguments.to, arguments.message)