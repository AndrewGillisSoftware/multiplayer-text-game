from command_parser import *

# Create a command to key off of
DISCONNECT_COMMAND = '/disconnect'

# Create the intended parser arguments
disconnect_parser = argparse.ArgumentParser(description="")
disconnect_parser.add_argument('command', type=str, help = '')

# Once parser is selected and disassembled what happens
def handle_disconnect(client_transport, input_args):
    try:
        arguments = disconnect_parser.parse_args(input_args)
    except:
        print_all(f"Error parsing arguments")
        return

    # Do whatever
    print_all("Disconnecting")
    client_transport.disconnect()