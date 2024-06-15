import os
import time
from threading import Thread
import argparse
import dataclasses

import yaml
import json
from protopost import ProtoPost
from protopost import protopost_client as ppcl

from libhashcast.keys import generate_key
from libhashcast.stamp import create_stamp, hash_stamp, mine_stamp
from libhashcast.message import create_message, encode_message, decode_message
from libhashcast.utils import calc_difficulty
from libhashcast.client import Outbox, Client

#TODO: save/load keys
#TODO: determine diff from relay(s)

TX_HOST = os.getenv("TX_HOST")
PORT = os.getenv("PORT", 80)

DIFF = 0.9 #TODO: determine diff from relay(s)

#TODO: indicator for hashing and waiting to see message return from relay

#generate a signing key
signing_key = generate_key()
#extract the verify key
verify_key = signing_key.verify_key.encode()

def hash_and_broadcast(data):
    data = bytes(data, "utf8")
    stamp, stamp_hash = mine_stamp(verify_key, DIFF)
    signed_message = create_message(stamp, data, signing_key)
    m = encode_message(signed_message)
    ppcl(RELAY, m)

def receive(data):
    message = decode_message(data)
    #TODO: assume utf8 and decode
    print(message.content)

def start_receive_server():
    ProtoPost({
        "": receive,
    }).start(PORT)

Thread(target=start_receive_server, daemon=True).start()

while True:
    message = input().strip()
    
    if message == "":
        continue
    
    hash_and_broadcast(message)