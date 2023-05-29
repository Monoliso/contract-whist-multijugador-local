import sys
import socket
import json
import random

def conectar_jugadores(acceso: socket.socket, num_jugadores: int):
    conexiones_jugadores = list()
    jugadores = dict()
    
    while True:
        conexion_jugador, direccion_jugador = acceso.accept()
        conexiones_jugadores.append(conexion_jugador)
        nombre_jugador = conexion_jugador.recv(1024).decode("utf-8")
        # Creo que podemos mantener la representación interna de los jugadores,
        # valiéndonos del diccionario, nunca mejor usado, para comunicarnos

        # jugadores[direccion_jugador] = nombre_jugador
        jugadores[nombre_jugador] = direccion_jugador
        conexion_jugador.send(f"{nombre_jugador}, entraste a la sala!".encode("utf-8"))
        if len(jugadores) == num_jugadores: break
    print(jugadores)
    return conexiones_jugadores, jugadores


def desconectar_jugadores(jugadores: list) -> None:
    jugador: socket.socket
    for jugador in jugadores:
        print(f"Se cerró la conexión con {jugador}")
        jugador.close()
    jugadores.clear()


def obtener_conexion(direccion: tuple, conexiones_jugadores: list):
    conexion: socket.socket
    jugador = conexiones_jugadores[0]
    for conexion in conexiones_jugadores:
        if conexion.getpeername() == direccion:
            jugador = conexion
    return jugador


if __name__ == "__main__":
    num_jugadores = int(sys.argv[1])
    acceso = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    acceso.bind(("127.0.0.1", 5051))
    acceso.listen()
    conexiones_jugadores, jugadores = conectar_jugadores(acceso, num_jugadores)
    orden_mano = list(jugadores.keys())
    random.shuffle(orden_mano)
    print(f"El orden de la mano: {orden_mano}")
    jugador_x = obtener_conexion(jugadores["Andres"], conexiones_jugadores)
    print(jugador_x)
    jugador_x.send(f"Hola Andrew".encode("utf-8"))
    desconectar_jugadores(conexiones_jugadores)
    acceso.close()
    print(jugadores)