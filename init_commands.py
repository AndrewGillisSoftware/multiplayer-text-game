from command_parser import *

add_command(SMS_COMMAND, handle_sms)
add_command(HELP_COMMAND, handle_help)
add_command(CONNECT_COMMAND, handle_connect)
add_command(DISCONNECT_COMMAND, handle_disconnect)
add_command(PASSTHROUGH_COMMAND, handle_passthrough)
add_command(GET_PLAYERS_COMMAND, handle_get_players)
add_command(SMS_ALL_COMMAND, handle_sms_all)