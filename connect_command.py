from command_parser import *

# Create a command to key off of
CONNECT_COMMAND = '/connect'

# Create the intended parser arguments
connect_parser = argparse.ArgumentParser(description="")
connect_parser.add_argument('command', type=str, help = '')
connect_parser.add_argument('name', type=str, help = '')
connect_parser.add_argument('host', type=str, help = '')

# Once parser is selected and disassembled what happens
def handle_connect(client_transport, input_args):
    try:
        arguments = connect_parser.parse_args(input_args)
    except:
        print(f"Error parsing arguments")
        return

    # Do whatever
    print(f"Connecting {arguments.name} to {arguments.host}!")
    
    client_transport.connect(arguments.host)