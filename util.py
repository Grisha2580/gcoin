# This represents a util class, which contains helpful functions for the project.
from block import Block
import hashlib
def convert_to_block(json):
    return Block(json["prev_hash"], json["index"], json["timestamp"], json["data"], json["nonce"])

def get_address(address, port):
    return address + ":" + port

def hash_it(to_hash):
    hash = hashlib.sha256()
    hash.update(to_hash.encode())

    return hash.hexdigest()