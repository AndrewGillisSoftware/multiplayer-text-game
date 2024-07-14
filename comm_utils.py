import socket
import threading
import time
import json

HEADER_BYTES = 64
PORT = 5051
FORMAT = 'utf-8'

# SERVER REQUESTS
GET_ACTIVE_CLIENTS = "!NETWORK_TRANSPORT_GET_ACTIVE_CLIENTS_PARCEL!"
GET_ACTIVE_CLIENTS_RESPONSE = "!NETWORK_TRANSPORT_GET_ACTIVE_CLIENTS_PARCEL_RESPONSE!"
EMPTY_PARCEL = "!NETWORK_TRANSPORT_EMPTY_PARCEL!"
NEXT_PARCEL = "!NETWORK_TRANSPORT_SEND_NEXT_PARCEL!"
DISCONNECT_MESSAGE = "!NETWORK_TRANSPORT_DISCONNECTED!" # Payload has a very low chance to look like this

# CLIENT REQUESTS
GET_CLIENT_NAME = "GET_CLIENT_NAME"
GET_CLIENT_NAME_RESPONSE = "GET_CLIENT_NAME_RESPONSE"
SMS_MSG = "CLIENT_SMS"

class MailParcel:
    def __init__(self, purpose, from_address, to_address, message, time_stamp=None):
        self.purpose = purpose
        self.time_stamp = time_stamp if time_stamp else str(time.time())
        self.from_address = from_address
        self.to_address = to_address
        self.message = message
    
    def to_dict(self):
        return {
            'purpose' : self.purpose,
            'time_stamp': self.time_stamp,
            'from_address': self.from_address,
            'to_address': self.to_address,
            'message': self.message
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __repr__(self):
        return json.dumps(self.to_dict())

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
            return MailParcel(EMPTY_PARCEL, self.server_address, self.address, "")

        return self.box.pop()
    
def send_proto(conn, msg):
    # Encode Message
    message = str(msg).encode(FORMAT)

    # Encode Message Length
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER_BYTES - len(send_length))
    
    # Send Message Length
    conn.send(send_length)
    
    # Send Message
    conn.send(message)

def recv_proto(conn) -> str:
    # Get Message Length
    msg_length = conn.recv(HEADER_BYTES).decode(FORMAT)
    if msg_length:
        # Convert Message Length
        msg_length = int(msg_length)

        # Convert Message
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg
    return None

class ClientTransport:
    def __init__(self, handle_server):
        self.connected = False
        self.server_address = None
        self.client_address = socket.gethostbyname(socket.gethostname())
        self.client = None
        return
    
    def connect(self, server_address):
        self.server_address = server_address
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_address, PORT))
        self.connected = True
        return

    # If IP is server the message is for the server
    def send_parcel(self, purpose, to_address, string_message) -> MailParcel:
        # Create Parcel
        parcel = MailParcel(purpose, self.client_address, to_address, string_message)
        send_proto(self.client, parcel)
        return
    
    def get_next_parcel(self) -> MailParcel:
        # Create Parcel
        parcel = MailParcel(NEXT_PARCEL, self.client_address, self.server_address, "")
        send_proto(self.client, parcel)

        return MailParcel.from_dict(json.loads(recv_proto(self.client)))

    def disconnect(self):
        self.send_parcel(self.server_address, DISCONNECT_MESSAGE)
        self.connect = False
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
        server_address = self.address
        self.mail_boxes.append(MailBox(server_address, address))
        return

    def __deregister_client(self, address):
        # Remove mail box
        box = self.__get_mailbox(address)
        if box:
            self.mail_boxes.remove(box)
        return
    
    def __get_active_clients(self):
        client_ips = []
        for box in self.mail_boxes:
            client_ips.append(box.address)
        return client_ips

    def __handle_client_proto(self, conn, addr):
        client_address = addr[0]
        print(f"[NEW CONNECTION] {addr} connected.")

        self.__register_client(client_address)
    
        connected = True
        while connected:
            # Get Client Message
            client_message = recv_proto(conn)

            # Client Sent a Message
            if client_message:
                client_message_parcel : MailParcel = MailParcel.from_dict(json.loads(client_message))

                if DISCONNECT_MESSAGE == client_message_parcel.purpose:
                    print(f"[DISCONNECTED] {addr}")
                    connected = False
                    break
                elif NEXT_PARCEL == client_message_parcel.purpose:
                    # Send Client its mail if requested
                    box = self.__get_mailbox(client_address)
                    next_parcel_for_client = box.get_next_parcel()
                    if next_parcel_for_client.purpose != EMPTY_PARCEL:
                        print(f"[Sending Next Parcel of Mail to {client_address}] {next_parcel_for_client}")
                    send_proto(conn, next_parcel_for_client)
                elif GET_ACTIVE_CLIENTS == client_message_parcel.purpose:
                    self.send_to_client(GET_ACTIVE_CLIENTS_RESPONSE, self.address, client_address, str(self.__get_active_clients()))
                else:
                    cmp = client_message_parcel
                    self.send_to_client(cmp.purpose, cmp.from_address, cmp.to_address, cmp.message)
                    
                print(f"[{client_address}] {client_message}")

                # Server reacts to client
                if self.handle_client != None:
                    self.handle_client(client_message)
        
        self.__deregister_client(client_address)
        conn.close()
        print(f"[CLOSED / DEREGISTERED] {addr}")

    def start(self):
        print("[STARTING] server is starting...")
        self.server.listen()

        print(f"[LISTENING] Server is listening on {self.address}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.__handle_client_proto, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    
    def send_to_client(self, purpose, from_address, to_address, msg):
        mail = MailParcel(purpose, from_address, to_address, msg)
        box = self.__get_mailbox(to_address)
        box.add_parcel(mail)
        return
