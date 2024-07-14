from printable import *
import sys
import argparse
import shlex

from sms_command import *
from help_command import *
from connect_command import *
from disconnect_command import *
from passthrough_command import *
from sms_all_command import *
from get_players_command import *

general_parser = argparse.ArgumentParser(description="general")
general_parser.add_argument('command', type = str, help='')

# Key /command - handler
command_handlers = {}

def add_command(command_str, handling_function):
    command_handlers[command_str] = handling_function

def parse(client, raw_command):
    input_args = shlex.split(raw_command)

    try:
        general_args, _ = general_parser.parse_known_args(input_args)
    except argparse.ArgumentError as e:
        print_all(f"Error parsing arguments: {e}")
        return
    
    # Call Command handler
    try:
        command_handlers[general_args.command](client, input_args)
    except KeyError:
        print_all("Invalid command. try /help")