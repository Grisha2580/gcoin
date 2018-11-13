
from util import convert_to_block
from block import Block
import datetime
import json
import rsa
class Blockchain:
    """
    A class that represents a chain of blocks where all the information is stored.
    Has 1 attribute:
    :param __blockchain is a list of the Block object, representing a sequence of blocks inside the blockchain.
    :param peers is a list of all peers this node knows of in the P2P network.
    :param __transaction_pool are all the transactions that are not yet in blockchain.
    """

    def __init__(self, blockchain=None):
        # initialize an empty blockchain
        if blockchain:
            self.__blockchain = [convert_to_block(block) for block in blockchain]
        else:
            self.__blockchain = []

        self.mine_genesis()
        self.__transactions_pool = []

    def add_block(self, block):
        """
        Adds a block to the blockchain.
        :return:
        """
        valid_block = block.check_block()
        print('The block is valid {}'.format(valid_block))

        if valid_block:
            self.__blockchain.append(block)
        else:
            return False

    def mine_genesis(self):
        """
        Mines the genesis block in the blockchain if current blockchain is empty.
        :return:
        """
        if self.size() == 0:
            block = Block('0000', 0, datetime.datetime.today(), [], 1)
            self.__blockchain.append(block)


    def size(self):
        """
        The function that determines the length of the blockchain.
        :return: The length of the blockchain.
        """
        return len(self.__blockchain)

    def get_block(self, index=None):
        """
        Gets the block with the given index. If index is not specified - gets the last block.
        :param index: index of block to be taken.
        :return: block, which stands under this index in blockchain.
        """
        try:
            if not index:
                print('here')
                block_index = len(self.__blockchain) - 1
            else:
                block_index = index

            return self.__blockchain[block_index]
        except:
            raise IndexError("The block with this index does not exist")

    def get_transactions(self):
        return self.__transactions_pool

    def check_blockchain(self):
        """
        Checks if this blockchain is valid
        :return:
        """
        previous_block = self.__blockchain[0]
        for block in self.__blockchain[1:]:
            first = previous_block.hash_block() == block.prev_hash
            second = block.check_block()
            print('Prev block hash is the same {}'.format(first))
            print('The block is validly hashed {}'.format(second))

            if not (first and second):
                return False

        return True

    def add_transaction(self, transaction):

        if self.get_balance(transaction.public_key) >= transaction.value and transaction.verify():
            self.__transactions_pool.append(transaction)

    def get_balance(self, public_key):
        total = 0
        for block in self.__blockchain:
            total += block.balance(public_key)

        return total



    def to_json(self):
        """
        Converts blockchain to JSON object.
        :return: JSON, representing this blockchain.
        """
        message = []
        for block in self.__blockchain:
            message.append(block.to_json())

        print('This is what im going to send {}'.format(message))

        return message




