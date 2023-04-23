import os
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

async def main():
    await asyncio.sleep(0.1)
    servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")
    nc = await nats.connect(servers=servers)

    await nc.publish("greet.joe", b"hello")


    sub = await nc.subscribe("greet.*")


    try:
        msg = await sub.next_msg(timeout=0.1)
    except TimeoutError:
        pass

    
    msg = bytes(input(), 'utf-8')
    await nc.publish("greet.joe", msg)
    await nc.publish("greet.pam", b"hello")


    msg = await sub.next_msg(timeout=0.2)
    print(f"{msg.data} on subject {msg.subject}")


    msg = await sub.next_msg(timeout=0.2)
    print(f"{msg.data} on subject {msg.subject}")


    await nc.publish("greet.bob", b"hello")


    msg = await sub.next_msg(timeout=0.2)
    print(f"{msg.data} on subject {msg.subject}")


    await sub.unsubscribe()
    await nc.drain()

if __name__ == '__main__':
    process = iniciar_server()
    clear()
    asyncio.run(main())
    process.terminate()
    process.wait()
    print("process terminated :D")
    