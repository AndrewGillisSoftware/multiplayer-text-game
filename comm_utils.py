import socket
import threading

HEADER_BYTES = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!@#$%^&*()!DISCONNECT!DISCONNECT_NOW!@#$%^&*()" # Payload has a very low chance to look like this

class ClientTransport:
    def __init__(self, handle_server):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, address):
        self.client.connect((address, PORT))

    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER_BYTES - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def disconnect(self):
        self.send(DISCONNECT_MESSAGE)

class ServerTransport:
    # IPs of connected clients
    active_clients = []

    # (address, message) tuples that get sent to clients when clients ping the server
    # Once sent the tuple is removed from the mail box. Messages are sent based on when they were added to
    # the mailbox
    client_mailbox_queue = []

    def __init__(self, handle_client):
        self.handle_client = handle_client
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = socket.gethostbyname(socket.gethostname())
        self.server.bind((self.address, PORT))

    def __register_client(self, address):
        # Add Client to list of active clients
        self.active_clients.append(address)

    def __deregister_client(self, address):
        # Remove Client from active clients
        self.active_clients.remove(address)

        # Clean Mailbox for given client
        for client_message in self.client_mailbox_queue:
            if client_message[0] == address:
                self.client_mailbox_queue.remove(client_message)

    def __get_client_mail(self, address):
        mail = []
        # Clean Mailbox for given client
        for client_message in self.client_mailbox_queue:
            if client_message[0] == address:
                mail.append(client_message[1])
                self.client_mailbox_queue.remove(client_message)
        return mail

    def __handle_client_proto(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        self.__register_client(addr)
    
        connected = True
        while connected:
            msg_length = conn.recv(HEADER_BYTES).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                
                print(f"[{addr}] {msg}")

                if self.handle_client != None:
                    self.handle_client(msg)

                client_mail = self.__get_client_mail(addr)

                for message in client_mail:
                    print(f"[Sending Mail to {addr}] {message}")
        
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
    
    def send_to_client(self, client_address, msg):
        self.client_mailbox_queue.append((client_address, msg))

    def broadcast(self, msg):
        # For each client address
        for client_address in self.active_clients:
            # Add Message to Client's mailbox
            self.send_to_client(client_address, msg)