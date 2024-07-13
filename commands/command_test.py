from command_parser import *

add_command(SMS_COMMAND, handle_sms)

parse("/msg Isaac 'Hey there dumb head hows it going'")