# This file represents a wallet of one node
import rsa
from util import hash_it
from transaction import Transaction
class Wallet:
    """
    This class represents a wallet of one of the members of the P2P network.
    Has 2 attributes:
    :param public_key, public key of the wallet.
    :param private_key, private key of the wallet.
    :param blockchain, Blockchain object, which represents the blockchain this wallet is looking his amounts in.
    """
    def __init__(self, blockchain):
        self.public_key, self.__private_key = rsa.newkeys(256)
        self.address = hash_it(self.public_key)
        self.blockchain = blockchain

    def pay(self, recipient_address, value):
        transaction = Transaction(self.address, recipient_address, value, self.get_public_key())


        transaction.sign(self.__private_key)

        if value > self.balance():
            return transaction.to_json()
        else:
            raise ValueError('There is not enough money on your account.')

    def balance(self):
        """
        Gets the balance of the given wallet.
        :return: The amount of money this wallet has in the blockchain he currently has.
        """
        return  self.blockchain.get_balance(self.address)


    def get_public_key(self):
        """
        Gets the public key of the wallet.
        :return: JSON, representing public key of the wallet as [n, e]
        """

        return [self.public_key.n, self.public_key.e]



