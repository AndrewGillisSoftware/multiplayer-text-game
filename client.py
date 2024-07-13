from comm_utils import *

SERVER = "192.168.99.41"

ct = ClientTransport(None)
ct.connect(SERVER)

response = ct.send("Hello world")

ct.disconnect()

