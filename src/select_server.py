import sys
import socket
import selectors
import types
import time


sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]


def accept_wrapper(sock):
    nuevo_socket, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    nuevo_socket.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(nuevo_socket, events, data=data)
    return nuevo_socket, addr


# def service_connection(key, mask):
#     sock = key.fileobj
#     data = key.data
#     if mask & selectors.EVENT_READ:
#         recv_data = sock.recv(1024)  # Should be ready to read
#         if recv_data:
#             data.outb += recv_data
#         else:
#             print(f"Closing connection to {data.addr}")
#             sel.unregister(sock)
#             sock.close()
#     if mask & selectors.EVENT_WRITE:
#         if data.outb:
#             print(f"Echoing {data.outb!r} to {data.addr}")
#             sent = sock.send(data.outb)  # Should be ready to write
#             data.outb = data.outb[sent:]


def obtener_jugadores(ip_escucha: str, puerto: int) -> "list[tuple]":
    jugadores = list()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        listen_socket.bind((ip_escucha, puerto))
        listen_socket.listen()
        listen_socket.setblocking(False)
        print(f"Listening on {(ip_escucha, puerto)}")
        sel.register(listen_socket, selectors.EVENT_READ, data=None)

        print("Hasta acá")
        condicion = True
        while condicion:
            events = sel.select(timeout=None)
            print("Una vez agregado ya está ", end='')
            print(events)
            input()
            for key, mask in events:
                if key.data is None:
                    jugadores += accept_wrapper(key.fileobj)
                elif key == jugadores[0]:
                    condicion = False
                    # service_connection(key, mask)
            time.sleep(0.2)
        print("FUCK YEAH")
        return jugadores



if __name__ == "__main__":
    host, port = sys.argv[1], int(sys.argv[2])
    jugadores = obtener_jugadores(host, port)
    print(jugadores)