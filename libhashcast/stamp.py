import random
import datetime
from dataclasses import dataclass
import json

from .globals import NONCE_LENGTH, TIME_LENGTH, ENDIANNESS, HASH_ALGO
from .utils import b64encode, b64decode, calc_difficulty

@dataclass
class Stamp:
  verify_key: bytes
  time: bytes
  nonce: bytes

def hash_stamp(stamp):
  m = HASH_ALGO()
  m.update(stamp.verify_key)
  m.update(stamp.time)
  m.update(stamp.nonce)
  return m.digest()

#returns true if stamp came <seconds> seconds from the future
#TODO: test
def stamp_earlier_than(stamp, seconds):
  stamp_time = get_stamp_time(stamp)
  cur_time = int(datetime.datetime.now().timestamp())
  return stamp_time - cur_time >= seconds

#TODO: test
def stamp_older_than(stamp, seconds):
  stamp_time = get_stamp_time(stamp)
  cur_time = int(datetime.datetime.now().timestamp())
  return cur_time - stamp_time >= seconds

def get_stamp_time(stamp):
  return int.from_bytes(stamp.time, ENDIANNESS)

def get_current_time():
  #current time as unsigned 8 bytes little endian
  time = int(datetime.datetime.now().timestamp()).to_bytes(TIME_LENGTH, ENDIANNESS)
  return time

def encode_stamp(stamp):
  return {
    "verify_key": b64encode(stamp.verify_key),
    "time": b64encode(stamp.time),
    "nonce": b64encode(stamp.nonce)
  }

def decode_stamp(stamp):
  verify_key = b64decode(stamp["verify_key"])
  time = b64decode(stamp["time"])
  nonce = b64decode(stamp["nonce"])
  return Stamp(verify_key, time, nonce)

def create_stamp(verify_key, time=None, nonce=None):
  if nonce is None:
    nonce = random.randbytes(NONCE_LENGTH)
  if time is None:
    time = get_current_time()
  stamp = Stamp(verify_key, time, nonce)
  hash = hash_stamp(stamp)
  return stamp, hash

def mine_stamp(verify_key, min_difficulty, time=None, nonce=None):
    count = 0
    stamp, hash = create_stamp(verify_key, time=time, nonce=nonce)
    count += 1
    while calc_difficulty(hash) < min_difficulty:
        stamp, hash = create_stamp(verify_key, time=time, nonce=nonce)
        count += 1
        
    print("count", count)
    return stamp, hash