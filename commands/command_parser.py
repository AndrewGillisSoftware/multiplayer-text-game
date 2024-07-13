import argparse
import shlex
from sms import *

general_parser = argparse.ArgumentParser(description="general")
general_parser.add_argument('command', type = str, help='')

# Key /command - handler
command_handlers = {}

def add_command(command_str, handling_function):
    command_handlers[command_str] = handling_function

def parse(raw_command):
    input_args = shlex.split(raw_command)

    try:
        general_args, _ = general_parser.parse_known_args(input_args)
    except argparse.ArgumentError as e:
        print(f"Error parsing arguments: {e}")
        return
    
    # Call Command handler
    command_handlers[general_args.command](input_args)