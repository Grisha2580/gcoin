import hashlib
from util import hash_it
class Block:
    """
    Represents one block in the blockchain.
    Has 5 attributes:
    The header of the block:
    :param prev_hash, hash of the previous block in the blockchain.
    :param index - int representing index of the block in the blockchain.
    :param timestamp - float, representing the time the block has been mined.
    :param nonce - the number needed for changing the hash, that uses the prof of work.
    :param next_hash - hash of the next block in blockchain.

    The body of the blog.
    :param data - (Not yet decided), representing the data in the blockchain.
    """

    def __init__(self, prev_hash, index, timestamp, data, nonce):
        self.prev_hash = prev_hash
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce

    def hash_block(self):
        """
        Creates a hash from the block, using a sha256 algorithm.
        :return: str, representing this hash.
        """
        header = self.prev_hash + str(self.index) + str(self.timestamp) + str(self.data) + str(self.nonce)

        return hash_it(header)

    def check_block(self):
        """
        Checks, whether it is a valid block.
        :return: bool, representing whether this block is valid.
        """
        hash = self.hash_block()

        return hash[:4] == '0000'

    def save(self):
        """
        The block is being saved to the database in the local storage so that everything is saved if the node crashes.
        """
        pass

    def to_json(self):
        """
        Converts the block to the JSON object.
        :return: JSON object, representing this block.
        """
        json = {}
        json['prev_hash'] = self.prev_hash
        json['index'] = str(self.index)
        json['timestamp'] = str(self.timestamp)
        json['data'] = self.data
        json['nonce'] = str(self.nonce)

        return json
