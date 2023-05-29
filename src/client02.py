import socket
import subprocess

if __name__ == "__main__":
    # Ingreso y salida temporal
    # print("\t1) Unirse a una sala\n"
    #       "\t2) Crear una sala")
    # condicion = True
    # juego = 0
    # while condicion:
    #     juego = int(input("Cómo quiere jugar?"))
    #     if (juego == 1 or juego == 2):
    #         condicion = False
    #     else:
    #         print("Ingrese una opción válida.\n")
    # # 

    # if (juego == 1):
    #     dir_servidor = input("Ingrese la direccion IP: ")
    # else:
    #     dir_servidor = "127.0.1.1"
    #     subprocess.Popen(['python', "./server.py"], stdin=subprocess.PIPE,
    #                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.connect(("localhost", 5050))
        response = servidor.recv(1024)
        print('Server response:', response.decode())