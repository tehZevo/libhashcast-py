import os
from threading import Thread

import asyncio
from websockets.server import serve
from protopost import ProtoPost
from protopost import protopost_client as ppcl

WS_PORT = int(os.getenv("WS_PORT", 80))
RX_HOST = os.getenv("RX_HOST", None)
TX_PORT = int(os.getenv("TX_PORT", 0))

def start_protopost():
    ProtoPost({
        "": transmit
    }).start(TX_PORT)

if TX_PORT > 0:
    Thread(target=start_protopost, daemon=True).start()

CLIENTS = set()

def transmit(message):
    for websocket in CLIENTS.copy():
        try:
            #TODO: need send sync?
            await websocket.send(message)
        except websockets.ConnectionClosed:
            pass

async def handler(websocket):
    CLIENTS.add(websocket)
    try:
        async for message in websocket:
            if RX_HOST is not None:
                ppcl(RX_HOST, message)
    finally:
        CLIENTS.remove(websocket)

async def main():
    async with serve(handler, "localhost", WS_PORT):
        await asyncio.Future()

asyncio.run(main())