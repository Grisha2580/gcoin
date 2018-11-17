import hashlib
from util import hash_it, pub_to_json, transactions_to_json
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

    def __init__(self, prev_hash, index, timestamp, data, owner, nonce):
        self.prev_hash = prev_hash
        self.index = index
        self.timestamp = str(timestamp)
        self.data = data
        self.owner_address = owner
        self.nonce = nonce

    def hash_block(self):
        """
        Creates a hash from the block, using a sha256 algorithm.
        :return: str, representing this hash.
        """
        from util import hash_it

        header = self.prev_hash + str(self.index)\
                 + str(self.timestamp) + str(self.data) \
                 + str(self.nonce) + str(self.owner_address)

        return hash_it(header)

    def check_block(self):
        """
        Checks, whether it is a valid block.
        :return: bool, representing whether this block is valid.
        """
        hash = self.hash_block()


        # Make sure all transactions on the block are valid
        for transaction in self.data:
            if not transaction.verify():
                print('The transaction one the bock is invalid')
                return False

        valid_mine = hash[:4] == '0000'
        print('The block is validly mined {}'.format(valid_mine))

        return valid_mine

    def transaction_exists(self, transaction_other):
        """
        Checks if the given transaction exists in this block.
        :return: bool.
        """

        for transaction in self.data:
            if transaction == transaction_other:
                return True

        return False

    def save(self):
        """
        The block is being saved to the database in the local storage so that everything is saved if the models crashes.
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
        json['timestamp'] = self.timestamp
        json['data'] = transactions_to_json(self.data)
        json['nonce'] = str(self.nonce)
        json['owner_address'] = str(self.owner_address)

        return json

    def balance(self, public_key):
        """
        Checks how much money does the owner of this public key has in this current block.
        :return: int.
        """
        total = 0
        for transaction in self.data:

            total += transaction.get_money(public_key)

        print("I came here")
        print('This is owner address {}'.format(self.owner_address))
        print('This is send address {}'.format(hash_it(pub_to_json(public_key))))

        if self.owner_address == hash_it(pub_to_json(public_key)):
            total += 100

        print('These are the money I got from the block {} '.format(total))

        return total

