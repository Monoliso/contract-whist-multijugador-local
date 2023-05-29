import socketserver

MAX_CLIENTS = 6

# Define a custom request handler by subclassing socketserver.BaseRequestHandler
class ControladorTCP(socketserver.BaseRequestHandler):
    cant_clientes_conectados = 0
    clientes_conectados = list()
    jugadores_listos = False

    def controlar(self):
        self.cant_clientes_conectados += 1
        self.request.sendall("Hello World!".encode())
        print(self.cant_clientes_conectados)

        # Check if the maximum number of clients is reached or if the first client is ready
        if self.__class__.cant_clientes_conectados >= MAX_CLIENTS or self.__class__.jugadores_listos:
            self.__class__.jugadores_listos = True

        # Process requests while the match is not ready
        while not self.__class__.jugadores_listos:
            data = self.request.recv(1024)  # Adjust the buffer size as needed
            if data:
                # Check if the first client is ready
                if self.__class__.cant_clientes_conectados == 1 and data.decode().strip().lower() == 'ready':
                    self.__class__.jugadores_listos = True
                    break
                # Process the received data
                print(data.decode())

# Create a TCP server by subclassing socketserver.TCPServer
class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True  # Enable reuse of address and port

# Create an instance of the server by combining the server address and the custom request handler
server = MyTCPServer(('localhost', 5050), ControladorTCP)
ip, port = server.server_address
print(f"Ip: {ip}, port: {port}")

# Start the server by calling the serve_forever() method
server.serve_forever()
