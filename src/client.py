# import sys, select
import socket
# import time


HEADER = 32
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect_ex(ADDR)

# Se puede hacer, pero de vuelta nos encontramos con concurrencia, ya sea de este lado o
# del server


# tiempo = 0
# print("Tenes 30 segundos para responder!\n")
# while True:
#     i, o, e = select.select( [sys.stdin], [], [], 0)
#     # nombre = sys.stdin.readline(0).strip()
#     nombre = sys.stdin.read()
#     if (nombre):
#         print(f"Dijiste {nombre}")
#         break
#     elif tiempo == 20:
#         print("\033[1AQuedan 10 segundos!\033[1B")
#     elif tiempo == 5:
#         print("\033[1A5 segundos!\033[1B")
#     time.sleep(1)
#     tiempo += 1
#     print(tiempo)

nombre = input("Ingrese su nombre: ")
client.send(nombre.encode("utf-8"))
print(client.recv(2048).decode("utf-8"))
mensaje = client.recv(2048).decode("utf-8")
print(mensaje)
# mensaje = input("")
# client.send(mensaje.encode())
# client.close()

# def send(msg):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     client.send(send_length)
#     client.send(message)
#     print(client.recv(2048).decode(FORMAT))

# if __name__ == "__main__":
#     send("Hello World!")
#     input()
#     send("Hello Everyone!")
#     input()
#     send("Hello Tim!")

#     send(DISCONNECT_MESSAGE)