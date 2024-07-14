from randomNameGenerator import *
from comm_utils import *

# Utility Functions
def generate_random_client_name():
    symbolDataFileName = "NameSymbolTable_v1.csv"
    symbolTable = loadSymbolTableData(symbolDataFileName)

    return generateName(symbolTable, genString="1#2#3 1$2&")

# GLOBAL VARIABLES
OTHER_CLIENT_IPS = []
OTHER_CLIENT_NAME_TO_IP = {} # Dictionary of other client ips and their names for traffic forwarding
CLIENT_NAME = generate_random_client_name()

# Global ACCESSOR
def get_client_name():
    return CLIENT_NAME

def get_other_client_name(ip):
    other_clients = OTHER_CLIENT_NAME_TO_IP.items()
    for client in other_clients:
        if ip == client[1]:
            return client[0]
    return "Unknown"

# Utility Functions
def discover_other_client_ips(ct:ClientTransport):
    ct.send_parcel(GET_ACTIVE_CLIENTS, ct.server_address, "")

def discover_other_client_names(ct:ClientTransport):
    if len(OTHER_CLIENT_IPS) == 0:
        return False

    # Send a Parcel to each known ip for their name
    for ip in OTHER_CLIENT_IPS:
        ct.send_parcel(GET_CLIENT_NAME, ip, "")

    return True