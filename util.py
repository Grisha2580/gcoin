# This represents a util class, which contains helpful functions for the project.
import hashlib
import rsa

def hash_it(to_hash):
    hash = hashlib.sha256()
    hash.update(str(to_hash).encode())

    return hash.hexdigest()


def convert_to_block(json):
    from models.block import Block
    transactions = json['data']
    data = [convert_to_transaction(tr) for tr in transactions]

    return Block(json["prev_hash"], json["index"], json["timestamp"],
                 data, json['owner_address'], json["nonce"])

def convert_to_transaction(json):
    from models.transaction import Transaction

    signature = json['signature']
    signature = signature[2:][:-1]
    signature = signature.encode()
    signature = signature.decode('unicode-escape').encode('ISO-8859-1')

    public_key = rsa.PublicKey(json['public_key'][0], json['public_key'][1])

    return Transaction(json['recipient'], json['value'], public_key,timestamp=json['timestamp'], signature=signature)

def get_address(address, port):
    return 'http://' + address + ":" + port


def pub_to_json(public_key):
    return [public_key.n, public_key.e]

def json_to_pub(json):
    return rsa.PublicKey(json[0], json[1])

def transactions_to_json(data):
    json = []

    for transaction in data:
        json.append(transaction.to_json())

    return json