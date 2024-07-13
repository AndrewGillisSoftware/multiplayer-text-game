import socket
import threading
import datetime
import json

HEADER_BYTES = 64
PORT = 5051
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
    
    def to_dict(self):
        return {
            'from_address': self.from_address,
            'to_address': self.to_address,
            'message': self.message
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __repr__(self):
        return json.dumps(self.to_dict()) #f"MailParcel(from_address={self.from_address}, to_address={self.to_address}, message={self.message})"

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
        self.server_address = None
        self.client_address = socket.gethostbyname(socket.gethostname())
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return
    
    def connect(self, server_address):
        self.server_address = server_address
        self.client.connect((server_address, PORT))
        return

    # If IP is server the message is for the server
    def send_parcel_and_get_response(self, to_address, string_message) -> MailParcel:
        # Create Parcel
        parcel = MailParcel(self.client_address, to_address, string_message)

        send_proto(self.client, parcel)

        return recv_proto(self.client)

    def disconnect(self):
        self.send_parcel_and_get_response(self.server_address, DISCONNECT_MESSAGE)
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

    def __handle_client_proto(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        self.__register_client(addr)
    
        connected = True
        while connected:
            # Get Client Message
            client_message = recv_proto(conn)

            # Client Sent a Message
            if client_message:
                client_message_parcel = MailParcel.from_dict(json.loads(client_message))
                if DISCONNECT_MESSAGE == client_message_parcel.message:
                    connected = False

                print(f"[{addr}] {client_message}")

                # Server reacts to client
                if self.handle_client != None:
                    self.handle_client(client_message)
            
            # Send Client its mail
            box = self.__get_mailbox(addr)
            next_parcel_for_client = box.get_next_parcel()
            print(f"[Sending Next Parcel of Mail to {addr}] {next_parcel_for_client}")
            send_proto(conn, next_parcel_for_client)
        
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
