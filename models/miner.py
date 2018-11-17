import datetime
from models.block import Block


class Miner:
    """
    Class that represents a miner that is trying to create a new block, solving the puzzle.
    Has two attributes:
    :param blockchain- the blockchain the miner is mining for.
    :param num_zeros - the amount of zeros that a hash function needs to have.
    """

    def __init__(self, blockchain, address, num_zeros=4):
        self.blockchain = blockchain
        self.num_zeros = num_zeros
        self.address = address

    def run_mining(self):
        """
        The function that is attempting to mine a block.
        :return: A Block object, which represents a new mined block.
        """
        new_block_index = self.blockchain.size()
        new_block_data = self.blockchain.get_transactions()
        new_block_prev_hash = self.blockchain.get_block().hash_block()

        nonce = 0
        new_block = Block(new_block_prev_hash, new_block_index,
                          datetime.datetime.today(), new_block_data, self.address, nonce)
        while not new_block.check_block():
            nonce += 1
            new_block = Block(new_block_prev_hash, new_block_index,
                              datetime.datetime.today(), new_block_data, self.address, nonce)

        print('I created new block and it is valid {}'.format(new_block.check_block()))

        return new_block


