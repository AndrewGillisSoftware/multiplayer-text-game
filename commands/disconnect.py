from command_parser import *

# Create a command to key off of
DISCONNECT_COMMAND = '/disconnect'

# Create the intended parser arguments
disconnect_parser = argparse.ArgumentParser(description="")
disconnect_parser.add_argument('command', type=str, help = '')

# Once parser is selected and disassembled what happens
def handle_disconnect(input_args):
    try:
        arguments = disconnect_parser.parse_args(input_args)
    except argparse.ArgumentTypeError as e:
        print(f"Error parsing arguments: {e}")
        return

    # Do whatever
    print("Disconnecting")