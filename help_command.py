from command_parser import *

# Create a command to key off of
HELP_COMMAND = '/help'

# Create the intended parser arguments
help_parser = argparse.ArgumentParser(description="help")
help_parser.add_argument('command', type=str, help = 'Must be /help')

# Once parser is selected and disassembled what happens
def handle_help(client_transport, input_args):
    try:
        arguments = help_parser.parse_args(input_args)
    except:
        print_all(f"Error parsing arguments")
        return

    # Do whatever
    print_all("Get yo own help")