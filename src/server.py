import asyncio
import sys
import subprocess
import os

import nats
from nats.errors import TimeoutError

def iniciar_natsio_server():
    dirname = os.path.dirname(__file__)
    archivo = os.path.join(dirname, "nats-server", "nats-server-v2.6.5-linux-amd64", "nats-server")
    p = subprocess.Popen([archivo])
    return p

async def hostear(partida):
    process = iniciar_natsio_server()
    servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")
    client = await nats.connect(servers=servers)

    sub = await client.subscribe(partida)
    print("prueba")
    while True:
        try:
            reply = await sub.next_msg()
        except TimeoutError:
            continue

        respuesta = reply.data.decode().split(",", 1)
        print("respuesta: ", respuesta)
        if respuesta[1]=="TERMINAR_PARTIDA":
            break
        if respuesta[1]=="INICIAR_PARTIDA":
            continue
        elif respuesta[1]=="hola":
            await client.publish(partida, b"host,hola")
            await sub.next_msg()

    process.terminate()
    process.wait(1)

async def main():
    partida = sys.argv[1]

    await hostear(partida)

if __name__ == "__main__":
    asyncio.run(main())
