import base64
import math

from .globals import ENCODING, HASH_BITS, ENDIANNESS

def b64encode(bytez):
  return base64.b64encode(bytez).decode(ENCODING)

def b64decode(b64):
  return base64.b64decode(b64.encode(ENCODING))

def calc_difficulty(hash):
    hash_num = int.from_bytes(hash, ENDIANNESS)
    return hash_num / (2 ** HASH_BITS)
