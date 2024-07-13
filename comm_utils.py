import socket
import threading
import datetime
import pickle
from shared_classes import *

HEADER_BYTES = 64
PORT = 5050
FORMAT = 'utf-8'
EMPTY_PARCEL = "!NETWORK_TRANSPORT_EMPTY!"
DISCONNECT_MESSAGE = "!NETWORK_TRANSPORT_DISCONNECTED!" # Payload has a very low chance to look like this

class MailParcel:
    def __init__(self, from_address, to_address, message):
        self.time_stamp = datetime.datetime.now()
        self.from_address = from_address
        self.to_address = to_address
        self.message = message
        return
    
    def get_message(self):
        return pickle.loads(self.message)

class MailBox:
    box = []

    def __init__(self, server_address, address):
        self.server_address = server_address
        self.address = address
        return

    def add_parcel(self, parcel):
        self.box.append(parcel)
        return

    def get_next_parcel(self) -> MailParcel:
        if len(self.box) == 0:
            # Return Empty Parcel
            return MailParcel(self.server_address, self.address, EMPTY_PARCEL)

        return self.box.pop()

class ClientTransport:
    def __init__(self, server_address, handle_server):
        self.server_address = server_address
        self.client_address = socket.gethostbyname(socket.gethostname())
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_address, PORT))
        return

    # If IP is server the message is for the server
    def send_parcel_and_get_response(self, to_address, any_object) -> MailParcel:
        # Create Parcel
        parcel = MailParcel(self.client_address, to_address, pickle.dumps(any_object))

        # Pickle Parcel
        pickled_parcel = pickle.dumps(parcel)

        # Get Size of Pickle Parcel
        pickle_parcel_length = len(pickled_parcel)

        # Send Pickle Parcel Length
        pickle_parcel_length_payload = str(pickle_parcel_length).encode(FORMAT)
        pickle_parcel_length_payload += b' ' * (HEADER_BYTES - len(pickle_parcel_length_payload))
        self.sendall(pickle_parcel_length_payload)

        # Send Pickle Parcel
        self.sendall(pickled_parcel)

        # Get Par


    """
    def send(self, msg):
        # Send
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER_BYTES - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

        # Response

        # Get addr_length payload
        addr_length = self.client.recv(HEADER_BYTES).decode(FORMAT)
        addr_length = int(addr_length)

        # Get Address
        addr = self.client.recv(addr_length).decode(FORMAT)

        # Get msg_length of payload
        msg_length = self.client.recv(HEADER_BYTES).decode(FORMAT)
        msg_length = int(msg_length)

        # Get response message
        response = self.client.recv(msg_length).decode(FORMAT)
    
        print(f"[Received Parcel of Mail from {addr}] {response}")
        return response
    """

    def disconnect(self):
        self.send_parcel_and_get_response(self.server_address, ParcelDisconnect)
        return

class ServerTransport:

    mail_boxes = []

    def __init__(self, handle_client):
        self.handle_client = handle_client
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = socket.gethostbyname(socket.gethostname())
        self.server.bind((self.address, PORT))
        return
    
    def __get_mailbox(self, address):
        # Ensure box does not already exist
        for box in self.mail_boxes:
            if box.address == address:
                return box
        return None

    def __register_client(self, address):
        # Ensure box does not already exist
        box = self.__get_mailbox(address)
        if box:
            return
        # Add client to list of active clients by creating a mailbox
        # self.address = Server Address
        self.mail_boxes.append(MailBox(self.address, address))
        return

    def __deregister_client(self, address):
        # Remove mail box
        box = self.__get_mailbox(address)
        if box:
            self.mail_boxes.remove(box)
        return
    
    def __send_to_client_proto(self, conn, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER_BYTES - len(send_length))
        conn.send(send_length)
        conn.send(message)

    def __handle_client_proto(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        self.__register_client(addr)
    
        connected = True
        while connected:
            msg_length = conn.recv(HEADER_BYTES).decode(FORMAT)
            if msg_length:
                # Get msg_length payload
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                
                print(f"[{addr}] {msg}")

                # Server reacts to clients hook
                if self.handle_client != None:
                    self.handle_client(msg)

                # Send address
                self.__send_to_client_proto(conn, addr)
                
                # Send next parcel to client
                box = self.__get_mailbox(addr)
                next_parcel_for_client = box.get_next_parcel()
                print(f"[Sending Next Parcel of Mail to {addr}] {next_parcel_for_client}")
                self.__send_to_client_proto(conn, next_parcel_for_client)
        
        self.__deregister_client(addr)
        conn.close()

    def start(self):
        print("[STARTING] server is starting...")
        self.server.listen()

        print(f"[LISTENING] Server is listening on {self.address}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.__handle_client_proto, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    
    def send_to_client(self, from_address, to_address, msg):
        mail = MailParcel(from_address, to_address, msg)
        self.client_mailbox_queue.append(mail)
