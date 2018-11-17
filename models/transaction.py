# This is the file for representing data in blockchain
import rsa
from util import hash_it, pub_to_json
import datetime

class Transaction:
    """
    Transaction has three attributes:
    :param sender - str, the address of the sender of money.
    :param recipient - str, the address of the one who gets the money.
    :param value - int, the amount of money to be sent.
    :param public_key - int, the public key of the sender of the transaction.
    """


    def __init__(self, recipient, value, public_key, timestamp = None, signature=None):
        self.recipient = recipient
        self.value = value
        self.public_key = public_key
        if not timestamp:
            self.timestamp = str(datetime.datetime.today())
        else:
            self.timestamp = str(timestamp)
        self.signature = signature


    def to_json(self, get_signature=True):
        """
        Converts transaction to json.
        :param ignore_signature: decides whether the signature should be added to the json.
        :return:
        """
        message = {}
        message['recipient'] = self.recipient
        message['value'] = self.value
        message['public_key'] = pub_to_json(self.public_key)
        message['timestamp'] = self.timestamp
        if get_signature:
            message['signature'] = str(self.signature)

        return message

    def hash(self):
        """
        Hashes the transaction.
        :return: the hash of this transaction.
        """
        header = self.recipient + str(self.value) + str(self.public_key) + str(self.signature)

        return hash_it(header)

    def __eq__(self, transaction):
        """
        Determines if self and given transactions are equal.
        :param transaction: Transaction object to compare to.
        :return: bool, representing if this is the same transaction.
        """
        return self.hash() == transaction.hash()

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
        if not self.signature:
            transaction = self.to_json(False)
            to_sign = str(transaction).encode()
            self.signature = rsa.sign(to_sign, private_key, 'SHA-256')

    def verify(self):
        """
        Verifies the signature on the transaction.
        :return: bool if the signature is valid.
        """
        try:
            rsa.verify(str(self.to_json(False)).encode(), self.signature, self.public_key)
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



