import os
from threading import Thread

from websockets.sync.client import connect
from protopost import ProtoPost
from protopost import protopost_client as ppcl

#TODO: auto reconnect

WS_URL = os.getenv("WS_URL")
RX_HOST = os.getenv("RX_HOST", None)
TX_PORT = int(os.getenv("TX_PORT", 0))

websocket = connect(WS_URL)

def transmit(message):
    websocket.send(message)

def start_tx_server():
    ProtoPost({
        "": transmit
    }).start(TX_PORT)

if TX_PORT > 0:
    Thread(target=start_tx_server, daemon=True).start()

while True:
    message = websocket.recv()
    if RX_HOST is not None:
        ppcl(RX_HOST, message)