import hashlib

NONCE_LENGTH = 4 #bytes
TIME_LENGTH = 8 #bytes
ENDIANNESS = "little"
HASH_ALGO = hashlib.sha256
HASH_BITS = 256
ENCODING = "utf8"
EARLY_STAMP_TIME = 5 #seconds
OLD_STAMP_TIME = 60 #seconds
