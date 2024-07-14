from command_parser import *
from client_utils import *

# Create a command to key off of
GET_PLAYERS_COMMAND = '/get_players'

# Create the intended parser arguments
get_players_parser = argparse.ArgumentParser(description="Commands for sms commands")
get_players_parser.add_argument('command', type=str, help = 'Must be /get_players')

# Once parser is selected and disassembled what happens
def handle_get_players(client_transport, input_args):
    try:
        arguments = get_players_parser.parse_args(input_args)
    except:
        print_all(f"Error parsing arguments")
        return

    print_all(str(OTHER_CLIENT_NAME_TO_IP))