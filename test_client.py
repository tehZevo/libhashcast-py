import random
import statistics

from libhashcast.keys import generate_key
from libhashcast.stamp import create_stamp, hash_stamp, mine_stamp
from libhashcast.message import create_message
from libhashcast.utils import calc_difficulty
from libhashcast.client import Outbox, Client

#TODO: protopost client that is configured with a list of nodes to spam to

#generate a signing key
signing_key = generate_key()
#extract the verify key
verify_key = signing_key.verify_key.encode()

outbox = Outbox(send_callback=lambda m: print("sending", m))
client = Client(read_callback=lambda m: outbox.enqueue(m, hash_stamp(m.stamp)))

# stamp, hash = create_stamp(verify_key)
stamps = [create_stamp(verify_key) for _ in range(1000)]
hashes = [hash for _, hash in stamps]
diffs = [calc_difficulty(hash) for hash in hashes]
diff = max(diffs) #statistics.mean(diffs)
# print("target diff:", 1 / (1 - diff))
stamp, hash = mine_stamp(verify_key, diff)
signed_message = create_message(stamp, b"hello world", signing_key)

client.receive(signed_message)
client.receive(signed_message)
signed_message.content = b"eve was here"
client.receive(signed_message)

#TODO: hmm...
outbox.send_next()
