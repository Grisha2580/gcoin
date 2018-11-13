# This is the file for representing data in blockchain
import rsa
from util import hash_it

class Transaction:
    """
    Transaction has three attributes:
    :param sender - str, the address of the sender of money.
    :param recipient - str, the address of the one who gets the money.
    :param value - int, the amount of money to be sent.
    :param private_key - int, the private key of the sender of the transaction.
    """

    def __init__(self, recipient, value, public_key, signature=None):
        self.recipient = recipient
        self.value = value
        self.public_key = public_key
        self.signature = signature

    def to_json(self, get_signature=True):
        """
        Converts transaction to json.
        :param ignore_signature:
        :return:
        """
        message = {}
        message['recipient'] = self.recipient
        message['value'] = self.value
        message['public_key'] = self.public_key
        if get_signature:
            message['signature'] = str(self.signature)

    def get_owner(self):
        """
        Gets the address of the owner of this transaction.
        :return: owner address.
        """
        return hash_it(self.public_key)

    def sign(self, private_key):
        """
        Signs the transaction with the private_key.
        :param private_key:  the private key of the owner.
        :return: either
        """
        if not self.signature():
            self.signature = rsa.sign(self.to_json(False), private_key, 'SHA-256')

    def verify(self):
        try:
            rsa.verify(self.to_json(False), self.signature, self.public_key)
            return True
        except:
            return False

    def get_money(self, public_key):
        """
        Determines if the owner of this public key has gets anything from this transaction.

        :param public_key: the public key of the owner to check.
        :return: int, returns 0 it is not his transaction, negative number if he is the sender and positive number if
        he is a recipient.
        """
        total = 0

        if hash_it(self.public_key) == hash_it(public_key):
            total -= self.value
        elif hash_it(public_key) == self.recipient:
            total += self.value

        return total



