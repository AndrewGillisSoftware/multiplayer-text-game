from comm_utils import *
from init_commands import *

#SERVER = "127.0.0.1"

ct = ClientTransport(None)

while True:
    user_input = input("Enter Command: ")
    parse(ct, user_input)
