import os
import time
from threading import Thread
import json

from protopost import ProtoPost
from protopost import protopost_client as ppcl

from libhashcast.stamp import hash_stamp
from libhashcast.message import encode_message, decode_message
from libhashcast.client import Outbox, Client

PORT = int(os.getenv("PORT", 80))
PEERS = json.reads(os.getenv("PEERS", "[]"))

#TODO: niceness based on time to send to all peers
#TODO: env vars
DEFAULT_SLEEP = 1 #seconds
SEND_DELAY = 1/100. #100/s max

def on_validate(message):
    print("validated", message)
    outbox.enqueue(message, hash_stamp(message.stamp))

def outbox_send(message):
    m = encode_message(message)
    for peer in config["peers"]:
        ppcl(peer, m)
    
outbox = Outbox(send_callback=outbox_send)
client = Client(signing_key, read_callback=on_validate)

def receive(data):
    message = decode_message(data)
    client.receive(message)

def start_relay_server():
    ProtoPost({
        "": receive,
    }).start(RELAY_PORT)

Thread(target=start_relay_server, daemon=True).start()

while True:
    if len(outbox.messages) > 0:
        outbox.send_next()
        time.sleep(SEND_DELAY)
    else:
        time.sleep(DEFAULT_SLEEP)