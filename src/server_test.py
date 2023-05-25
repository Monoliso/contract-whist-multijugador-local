import os
import threading
import asyncio
import subprocess

import nats
from nats.errors import TimeoutError

def clear():
    print("\033[H\033[J", end="")

def ingresar_partida():
    partida = input("Ingrese el nombre de la partida: ")
    while (partida == ""):
        print("Ingreso invalido, pruebe de vuelta...")
        partida = input("Ingrese el nombre de la partida: ")

    return partida

async def unirse(nombre_jugador, partida: str):
    # connect to server
    servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")
    client = await nats.connect(servers=servers)
    lista_jugadores = list()
    
    if partida=="":
        partida = ingresar_partida()

    partida_encontrada = False
    jugador = await client.subscribe(partida)
    msg = f"{nombre_jugador},hola".encode()

    while not partida_encontrada:
        await client.publish(partida, msg)
        print(await jugador.next_msg())
        try:
            reply = await jugador.next_msg(timeout=1)
        except TimeoutError:
            print("No se encontró la partida, intente de vuelta...")
            partida = ingresar_partida()
            jugador = await client.subscribe(partida)
        else:
            respuesta = reply.data.decode().split(",", 1)
            print(respuesta)
            if respuesta[1]=="PARTIDA_INICIADA":
                print("Partida ya iniciada, intente de vuelta...")
                partida = ingresar_partida()
                jugador = await client.subscribe(partida)
            if respuesta[1]=="hola":
                partida_encontrada = True
    
    # while True:
    #     try:
    #         reply = await jugador.next_msg(timeout=0.2)
    #     except TimeoutError:
    #         pass
    #     else:
    #         respuesta = reply.data.decode().split(",")
    #         break

    # lista_jugadores = reply.data.split(",")

    # while True:
    #     try:
    #         reply = await jugador.next_msg()
    #         respuesta = reply.data.decode().split(",", 1)
    #     except TimeoutError:
    #         pass
    #     else:
    #         if respuesta[1]=="INICIAR_PARTIDA":
    #             break
    #         if respuesta[1]=="hola":
    #             continue
    #         else:
    #             lista_jugadores = reply.data.split(",")


    # nombre = obtener_nombre_partida()
    # sub = client.subscribe(nombre)

    # # prueba publicar algo en "greet.joe"
    # await client.publish("greet.joe", b"hello")

    # # se suscribe a "greet.cualquier_cosa"
    # sub = await client.subscribe("greet.*")

    # try:
    #     msg = await sub.next_msg(timeout=0.1)
    # except TimeoutError:
    #     pass

    
    # msg = bytes(input(), 'utf-8')
    # await client.publish("greet.joe", msg)
    # await client.publish("greet.pam", b"hello")


    # msg = await sub.next_msg(timeout=0.2)
    # print(f"{msg.data} on subject {msg.subject}")


    # msg = await sub.next_msg(timeout=0.2)
    # print(f"{msg.data} on subject {msg.subject}")


    # await client.publish("greet.bob", b"hello")


    # msg = await sub.next_msg(timeout=0.2)
    # print(f"{msg.data} on subject {msg.subject}")

async def main():
    # hostear o unirse a una partida
    ans = input("Crear sala(0) o unirse a una partida(1): ")
    while (ans != "0" and ans != "1"):
        print("Valor invalido, intente de vuelta...")
        ans = input("Crear sala(0) o unirse a una partida(1): ")

    nombre_jugador = input("Ingrese su nombre: ")
    nombre_partida = ""
    server = None
    if ans=='0':
        print("anda esto????")
        nombre_partida = input("Ingrese el nombre de la partida: ")
        server = subprocess.Popen(["python3.8", "./server.py", nombre_partida])
        await asyncio.sleep(0.2)
        
    await unirse(nombre_jugador, nombre_partida)

    # await client.drain()

    if server:
        server.terminate()
        server.wait(1)
    print("process terminated :D")

    # clear()

if __name__ == '__main__':
    asyncio.run(main())
    