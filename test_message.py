import random

from libhashcast.keys import generate_key
from libhashcast.stamp import get_current_time, create_stamp
from libhashcast.message import create_message, encode_message, decode_message

#generate a signing key
signing_key = generate_key()
#extract the verify key
verify_key = signing_key.verify_key.encode()

#create a stamp for the current time
time = get_current_time()
stamp, hash = create_stamp(verify_key, time)

#sign the message with our stamp
signed_message = create_message(stamp, b"hello world", signing_key)

print(signed_message)

#roundtrip our message
encoded_signed_message = encode_message(signed_message)
print(encoded_signed_message)

decoded_signed_message = decode_message(encoded_signed_message)
print(decoded_signed_message)

#verify our signed message
decoded_signed_message.verify()

# tamper with the message
# decoded_signed_message.content = b"eve was here"
# message is now corrupt
# decoded_signed_message.verify()
