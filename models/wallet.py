# This file represents a wallet of one node
import rsa
from util import hash_it, pub_to_json
from models.transaction import Transaction
class Wallet:
    """
    This class represents a wallet of one of the members of the P2P network.
    Has 2 attributes:
    :param public_key, public key of the wallet.
    :param private_key, private key of the wallet.
    :param blockchain, Blockchain object, which represents the blockchain this wallet is looking his amounts in.
    """
    def __init__(self, blockchain, private_key=None):
        if not private_key:
            self.public_key, self.__private_key = rsa.newkeys(512)
        else:
            self.public_key = rsa.PublicKey(private_key[0], private_key[1])
            self.__private_key = rsa.PrivateKey(private_key[0], private_key[1],
                                                private_key[2], private_key[3], private_key[4])
        self.address = hash_it(pub_to_json(self.public_key))
        self.blockchain = blockchain

    def pay(self, recipient_address, value):
        """
        Generates the transaction.
        :param recipient_address: the address of the recipient.
        :param value: the amount of money to pay.
        :return: signed Transaction as a dictionary.
        """
        transaction = Transaction(recipient_address, value, self.public_key)



        transaction.sign(self.__private_key)

        if value <= self.balance():
            return transaction
        else:
            raise ValueError('There is not enough money on your account.')

    def balance(self):
        """
        Gets the balance of the given wallet.
        :return: The amount of money this wallet has in the blockchain he currently has.
        """
        return  self.blockchain.get_balance(self.public_key)


    def get_public_key(self):
        """
        Gets the public key of the wallet.
        :return: JSON, representing public key of the wallet as [n, e]
        """

        return pub_to_json(self.public_key)

    def get_address(self):
        """
        Gets the address of this wallet.
        :return: str, address of the wallet.
        """

        return self.address



