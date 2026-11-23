---
runme:
  id: 01HTB5KXPQTQ1R0SDR8Q4961G7
  version: v3
---

# Messaging Application

This is a simple messaging application implemented in Python. It consists of a server and multiple client nodes that can communicate with each other over a network.

## Features

- Server-client architecture for message exchange.
- Clients can connect to the server and send messages to each other.
- Server broadcasts messages to all connected clients.

## Prerequisites

- Python 3.x installed on your system.

- Terminal emulator to run the server and client nodes.

## Usage

### Starting the Server

1. Open a terminal and navigate to the project directory.

2. Run the following command to start the server:

```bash {"id":"01HTB5KXPQTQ1R0SDR8KB3NVHP"}
make server

```

This will start the server, and it will begin listening for incoming connections from client nodes.

### Starting a Client Node

1. Open another terminal and navigate to the project directory.

2. Run the following command to start a client node:

```bash {"id":"01HTB5KXPQTQ1R0SDR8N06VSYY"}
./run_node.sh 500

```

This will start a client node that connects to the server and allows you to send and receive messages.

3. Repeat step 2 to start additional client nodes with different port numbers if desired.

### Sending Messages

- Once the server and client nodes are running, you can send messages between nodes.
- Each client node will prompt you to enter a message, and you can send it to other connected nodes or broadcast it to all nodes.