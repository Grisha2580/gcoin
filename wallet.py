# This file represents a wallet of one node
import rsa
import sha
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
        self.public_key, self.private_key = rsa.newkeys(256)
        self.address = hash_it(self.public_key)
        self.blockchain = blockchain

    def pay(self, recepient_address, value):
        transaction = Transaction(self.address, recepient_address, value)
        signature = rsa.sign(transaction.to_json(), self.private_key, 'SHA-256')
        if value > self.balance():
            return [transaction.to_json(), signature]
        else:
            raise ValueError('There is not enough money on your account.')

    def balance(self):
        total = 0
        for block in self.blockchain:
            total += block.count_my_total()

        return total

