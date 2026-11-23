import socket
import threading

class Server:
    def __init__(self):
        self.host = 'localhost'  # Server host
        self.port = 5555  # Server port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        self.connections = {}  # Dictionary to store client connections
        self.lock = threading.Lock() 

    def start(self):
        # Start the server
        self.sock.bind((self.host, self.port))  # Bind socket to host and port
        self.sock.listen(5)  # Listen for incoming connections
        print("Server listening on port", self.port)
        # Start a thread to handle user input
        threading.Thread(target=self.handle_input).start()
        while True:
            # Accept incoming connections
            client_socket, address = self.sock.accept()
            # Start a new thread to handle each client
            threading.Thread(target=self.handle_client, args=(client_socket, address)).start()

    def handle_client(self, client_socket, address):
        port = address[1]  # Extract port from client address
        with self.lock:
            self.connections[port] = client_socket  # Add client socket to connections dictionary
        print(f"Node connected on port {port}")
        client_socket.sendall("OK".encode('utf-8'))  # Acknowledge connection
        while True:
            # Receive and process messages from the client
            data = client_socket.recv(1024)
            if not data:
                # If no data received, close connection and remove client from connections
                with self.lock:
                    del self.connections[port]
                print(f"Node on port {port} disconnected")
                break
            message = data.decode('utf-8')
            print(f"Received message from node on port {port}: {message}")

    def forward_message(self, message, recipient_port):
        # sent message to specified recipient or all clients
        if recipient_port == 'all':
            # Forward message to all connected clients
            for conn_port, conn_socket in list(self.connections.items()):
                try:
                    conn_socket.sendall(f"Server: {message}".encode('utf-8'))
                except Exception as e:
                    # Handle errors in sending message
                    print(f"Error sending data to port {conn_port}: {e}")
                    with self.lock:
                        del self.connections[conn_port]
        elif recipient_port.isdigit() and int(recipient_port) in self.connections:
            # send message to a specific client
            try:
                self.connections[int(recipient_port)].sendall(f"Server: {message}".encode('utf-8'))
            except Exception as e:
                # Handle errors in sending message
                print(f"Error sending data to port {recipient_port}: {e}")
                with self.lock:
                    del self.connections[int(recipient_port)]
        else:
            # Handle invalid recipient port number
            print("Invalid recipient port number.")

    def handle_input(self):
        # Handle user input to send messages or close the server
        while True:
            recipient_port = input("Enter the port of the node to send message (or 'all' to send to all nodes, 'exit' to close the server): ")
            if recipient_port.lower() == 'exit':
                # Close the server if 'exit' is entered
                self.close_server()
                break
            elif recipient_port.lower() == 'all':
                message = input("Enter the message to send: ")
            else:
                message = input("Enter the message to send: ")
            if message:
                self.forward_message(message, recipient_port)
            else:
                print("Message cannot be empty.")

    def close_server(self):
        # Close the server and clean up connections
        print("Closing server...")
        with self.lock:
            # Close connections and clear connections dictionary
            for conn_port, conn_socket in self.connections.items():
                conn_socket.close()
            self.connections.clear()
        self.sock.close()  # Close the server socket
        print("Server closed.")

if __name__ == "__main__":
    # Start the server 
    server = Server()
    server.start()
