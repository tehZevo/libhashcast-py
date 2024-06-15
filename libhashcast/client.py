from .globals import OLD_STAMP_TIME, EARLY_STAMP_TIME
from .stamp import stamp_older_than, stamp_earlier_than, hash_stamp

#outbox's job is to sort and send messages
class Outbox:
  def __init__(self, send_callback=lambda m: None):
    self.messages = []
    self.send_callback = send_callback

  def enqueue(self, message, stamp_hash):
    self.messages.append((message, stamp_hash))
    #clear out messages with old stamps
    self.messages = [(m, h) for (m, h) in self.messages if not stamp_older_than(m.stamp, OLD_STAMP_TIME)]

  def send_next(self):
    #sort by hash, descending (larger hash = better)
    self.messages.sort(key=lambda x: x[1], reverse=True)
    m, h = self.messages.pop(0)
    self.send_callback(m)

#client's job is to validate and deduplicate messages
class Client:
  def __init__(self, read_callback=lambda m: None):
    self.read_callback = read_callback
    self.stamps = []

  def remember_stamp(self, stamp):
    stamp_hash = hash_stamp(stamp)
    self.stamps.append((stamp, stamp_hash))
    #clear out old stamps
    self.stamps = [(stamp, stamp_hash) for (stamp, stamp_hash) in self.stamps if not stamp_older_than(stamp, OLD_STAMP_TIME)]

  def seen_stamp(self, stamp):
    stamp_hash = hash_stamp(stamp)
    for _, other_hash in self.stamps:
      if stamp_hash == other_hash:
        return True

    return False

  def receive(self, message):
    try:
      message.verify()
    except:
      print("Message failed verification, ignoring.")
      return

    if stamp_earlier_than(message.stamp, EARLY_STAMP_TIME):
      print("Stamp came from too far in the future, ignoring.")
      return

    if stamp_older_than(message.stamp, OLD_STAMP_TIME):
      print("Stamp is too old, ignoring.")
      return

    if self.seen_stamp(message.stamp):
      print("Seen this stamp before, ignoring.")
      return

    print("Cool, a new message!")
    self.read_callback(message)

    #store stamp in memory
    self.remember_stamp(message.stamp)
