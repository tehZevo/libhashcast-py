import random
import datetime
from dataclasses import dataclass
import json

from nacl.signing import VerifyKey

from .globals import HASH_ALGO, ENCODING
from .stamp import Stamp, hash_stamp, encode_stamp, decode_stamp
from .utils import b64encode, b64decode

def hash_content(content):
  return HASH_ALGO(content).digest()

@dataclass
class Message:
  stamp: bytes
  content: bytes
  signature: bytes

  def verify(self):
    #hash stamp and content, combine, and verify
    stamp_hash = hash_stamp(self.stamp)
    content_hash = hash_content(self.content)
    verify_key = VerifyKey(self.stamp.verify_key)
    verify_key.verify(stamp_hash + content_hash, self.signature)

def encode_message(message):
  return {
    "stamp": encode_stamp(message.stamp),
    "content": b64encode(message.content),
    "signature": b64encode(message.signature)
  }

def decode_message(message):
  stamp = decode_stamp(message["stamp"])
  content = b64decode(message["content"])
  signature = b64decode(message["signature"])
  return Message(stamp, content, signature)

def create_message(stamp, content, signing_key):
  stamp_hash = hash_stamp(stamp)
  content_hash = hash_content(content)
  signed = signing_key.sign(stamp_hash + content_hash)
  return Message(stamp, content, signed.signature)
