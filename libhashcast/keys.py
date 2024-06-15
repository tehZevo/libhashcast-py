from nacl.signing import SigningKey

def generate_key():
  return SigningKey.generate()
