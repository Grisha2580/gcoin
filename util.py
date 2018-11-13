# This represents a util class, which contains helpful functions for the project.
from block import Block
from transaction import Transaction
import hashlib
def convert_to_block(json):
    return Block(json["prev_hash"], json["index"], json["timestamp"], json["data"], json["nonce"])

def convert_to_transaction(json):
    signature = json['signature']
    signature = signature[2:][:-1]
    signature = signature.decode('unicode-escape').encode('ISO-8859-1')

    return Transaction(json['prev_hash'], json['value'], json['public_key'], signature)

def get_address(address, port):
    return 'http://' + address + ":" + port

def hash_it(to_hash):
    hash = hashlib.sha256()
    hash.update(to_hash.encode())

    return hash.hexdigest()