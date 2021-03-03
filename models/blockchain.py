

from models.block import Block
import datetime
from util import convert_to_block


class Blockchain:
    """
    A class that represents a chain of blocks where all the information is stored.
    Has 1 attribute:
    :param __blockchain is a list of the Block object, representing a sequence of blocks inside the blockchain.
    :param peers is a list of all peers this models knows of in the P2P network.
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

        # check if the block is valid
        if valid_block:

            new_pool = []

            # remove all the transaction from the pool that are in this block.
            for transaction in self.__transactions_pool:
                if not block.transaction_exists(transaction):
                    new_pool.append(transaction)

            self.__transactions_pool = new_pool

            self.__blockchain.append(block)
        else:
            return False

    def mine_genesis(self):
        """
        Mines the genesis block in the blockchain if current blockchain is empty.
        :return:
        """
        if self.size() == 0:
            block = Block('0000', 0, datetime.datetime.today(), [], 1, 'This block does not bring money')
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
                block_index = len(self.__blockchain) - 1
            else:
                block_index = index

            return self.__blockchain[block_index]
        except:
            raise IndexError("The block with this index does not exist")

    def get_transactions(self):
        """
        Gets the transactions of blockchain that are not in blockchain yet.
        :return: a list of transactions.
        """
        return self.__transactions_pool

    def check_blockchain(self):
        """
        Checks if this blockchain is valid
        :return: bool, representing if this blockchain is valid.
        """
        previous_block = self.__blockchain[0]
        for block in self.__blockchain[1:]:
            right_hash = previous_block.hash_block() == block.prev_hash
            valid_block = block.check_block()

            if not (right_hash and valid_block):
                return False

        return True

    def add_transaction(self, transaction):
        """
        Adds the transaction to the pool of transactions if it is valid.
        :param transaction: Transaction object, representing the transaction to add.
        """
        print('this is my balance {}'.format(self.get_balance(transaction.public_key)))

        enough_money = self.get_balance(transaction.public_key) >= transaction.value
        valid_transaction = transaction.verify()

        if enough_money and valid_transaction \
                and not self.transaction_exists(transaction):
            self.__transactions_pool.append(transaction)
        else:
            if not enough_money:
                print('There are not enough money on your wallet')
            if not valid_transaction:
                print('The transaction is invalid')
            else:
                print('Transaction already exist')
            raise ValueError('The transactions cannot be varified')

    def get_balance(self, public_key):
        """
        Gets the balance of the user that has the given public key.
        :param public_key: PublicKey object, which represents a public key of the owner of this public key.
        :return: the amount of money this user has.
        """
        total = 0
        for block in self.__blockchain:
            total += block.balance(public_key)

        return total

    def transaction_exists(self, transaction):
        """
        Checks if this transaction exists in the blockchain.
        :param transaction: Transaction object.
        :return: bool, representing if the transaction exist in the blockchain.
        """
        for block in self.__blockchain:
            if block.transaction_exists(transaction):
                return True

        return False

    def to_json(self):
        """
        Converts blockchain to JSON object.
        :return: JSON, representing this blockchain.
        """
        message = []
        for block in self.__blockchain:
            message.append(block.to_json())

        return message




