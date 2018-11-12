# This is the file for representing data in blockchain
import rsa

class Transaction:
    """
    Transaction has three attributes:
    :param sender - str, the address of the sender of money.
    :param recipient - str, the address of the one who gets the money.
    :param value - int, the amount of money to be sent.
    :param private_key - int, the private key of the sender of the transaction.
    """

    def __init__(self, sender, recipient, value, public_key):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.public_key = public_key

    def to_json(self):
        message = {}
        message['sender'] = self.sender
        message['recipient'] = self.recipient
        message['value'] = self.value
        message['public_key'] = self.public_key


