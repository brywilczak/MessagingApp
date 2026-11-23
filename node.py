import socket
import threading
import sys

class Node:
    def __init__(self, port, server_port=5555):
        # Initialize node with specified port and default server port
        self.host = 'localhost'
        self.port = port
        self.server_port = server_port

    def start(self):
        try:
            # Create a TCP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to the server
            self.sock.connect((self.host, self.server_port))
            # Send node's port to the server
            self.sock.sendall(str(self.port).encode('utf-8'))
            # Receive acknowledgment from the server
            server_ack = self.sock.recv(1024)
            # Check if the connection was successful
            if server_ack.decode('utf-8') == "OK":
                print("Connected to server")
                # Start a new thread to receive data from the server
                threading.Thread(target=self.receive_data).start()
                # Start sending data to the server
                self.send_data()
            else:
                print("Failed to connect to server")
        except KeyboardInterrupt:
            # Handle keyboard interrupt gracefully
            self.shutdown()
        finally:
            # Close the socket when done
            self.sock.close()

    def receive_data(self):
        # Continuously receive data from the server
        while True:
            data = self.sock.recv(1024)
            if data:
                print(data.decode('utf-8'))

    def send_data(self):
        try:
            # Continuously send data to the server
            while True:
                message = input("Enter message to send (type 'exit' to quit): ")
                if message.lower() == 'exit':
                    self.shutdown()
                    break
                self.sock.sendall(f"Node {self.port}: {message}".encode('utf-8'))
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        # Perform shutdown tasks
        print("Shutting down node...")
        self.sock.close()
        sys.exit()

class Main:
    def __init__(self):
        pass

    def run(self):
        if len(sys.argv) < 2:
            # Ensure correct usage of the script
            print("Usage: python node.py <port>")
            sys.exit(1)

        # Get the port number from command line arguments
        node_port = int(sys.argv[1])
        # Create a node instance
        node = Node(node_port)

        try:
            # Start the node
            node.start()
        except KeyboardInterrupt:
            # Handle keyboard interrupt gracefully
            print("\nKeyboard Interrupt detected.")
            node.shutdown()

if __name__ == "__main__":
    # Start the main program
    main = Main()
    main.run()
