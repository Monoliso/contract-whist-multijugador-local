import os
import threading
import asyncio
import subprocess

import nats
from nats.errors import TimeoutError

def clear():
    print("\033[H\033[J", end="")

def iniciar_server():
    dirname = os.path.dirname(__file__)
    archivo = os.path.join(dirname, "nats-server", "nats-server-v2.6.5-linux-amd64", "nats-server")
    p = subprocess.Popen([archivo])
    return p

async def suscribir(client):
    partida = input("Ingrese el nombre de la partida: ")
    while (partida == ""):
        print("Ingreso invalido, pruebe de vuelta...")
        partida = input("Ingrese el nombre de la partida: ")
    jugador = await client.subscribe(partida)

    return (partida, jugador)

async def unirse(client, nombre_jugador, partida: str):
    lista_jugadores = list()
    
    if partida=="":
        partida = input("Ingrese el nombre de la partida: ")

    partida_encontrada = False
    jugador = await client.subscribe(partida)
    msg = f"{nombre_jugador},hola".encode()

    while not partida_encontrada:
        await client.publish(partida, msg)
        await jugador.next_msg()
        try:
            reply = await jugador.next_msg(timeout=0.2)
            respuesta = reply.data.decode().split(",", 1)
        except TimeoutError:
            print("No se encontró la partida, intente de vuelta...")
            partida, jugador = await suscribir(client)
        else:
            if respuesta[1]=="PARTIDA_INICIADA":
                print("Partida ya iniciada, intente de vuelta...")
                partida, jugador = await suscribir(client)
            else:
                partida_encontrada = True
    
    while True:
        try:
            reply = await jugador.next_msg(timeout=0.2)
        except TimeoutError:
            pass
        else:
            respuesta = reply.data.decode().split(",")
            break

    lista_jugadores = reply.data.split(",")

    while True:
        try:
            reply = await jugador.next_msg()
            respuesta = reply.data.decode().split(",", 1)
        except TimeoutError:
            pass
        else:
            if respuesta[1]=="INICIAR_PARTIDA":
                break
            if respuesta[1]=="hola":
                continue
            else:
                lista_jugadores = reply.data.split(",")
                


async def hostear(client, partida):
    sub = await client.subscribe(partida)
    print("prueba")
    while True:
        try:
            reply = await sub.next_msg()
            respuesta = reply.data.decode().split(",", 1)
            print(respuesta)
        except TimeoutError:
            continue
        else:
            if respuesta[1]=="TERMINAR_PARTIDA":
                break
            if respuesta[1]=="INICIAR_PARTIDA":
                continue
            elif respuesta[1]=="hola":
                await client.publish(partida, b"host,hola")

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
    process = iniciar_server()
    clear()
    await asyncio.sleep(0.1)

    # connect to server
    servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")
    client = await nats.connect(servers=servers)

    # hostear o unirse a una partida
    ans = input("Crear sala(0) o unirse a una partida(1): ")
    while (ans != "0" and ans != "1"):
        print("Valor invalido, intente de vuelta...")
        ans = input("Crear sala(0) o unirse a una partida(1): ")

    nombre_jugador = input("Ingrese su nombre: ")
    nombre_partida = ""
    if ans:
        await unirse(client, nombre_jugador, nombre_partida)
    else:
        partida = input("Ingrese el nombre de la partida: ")
        await asyncio.gather(unirse(client, nombre_jugador, partida), hostear(client, partida))

    await client.drain()

    process.terminate()
    process.wait()
    print("process terminated :D")

if __name__ == '__main__':
    asyncio.run(main())
    