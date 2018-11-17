# This file represents a node in the P2P network.

from flask import Flask, request, jsonify
from models.blockchain import Blockchain
import json
from util import get_address, convert_to_transaction

from models.miner import Miner
import requests
import sys
from models.wallet import Wallet

app = Flask(__name__)

"""
This file represents one node in the P2P network.
Has 5 attributes:
:param blockchain - Blockchain object, which represents the current blockchain.
:param miner - Miner object, which helps the models mine if it wants.
:param neighbors - all the neighbors the models share its infromation to the in the P2P network.
:param address - the address the models is running on.
:param the port the models is running on.
"""

id = None
blockchain = Blockchain()
miner = None
neighbors = None
connector = ('127.0.0.1', '5000')
wallet = None
ip_address = None
port = None



@app.route('/peers', methods=['POST'])
def add_neighbor():
    """
    Adds a new neighbor to the current peer.
    :return:
    """
    global neighbors
    new_peer = json.loads(request.data)
    peer_id = new_peer['id']
    peer_address = new_peer['address']
    peer_port = new_peer['port']

    neighbors[peer_id] = (peer_address, peer_port)
    print('Now my peers are {}'.format(neighbors))

    return "Successfully added new peer", 200



@app.route('/transactions/update', methods=['POST'])
def transactions_update():
    """
    This request updates the models transaction pool, but does not spread the transaction among the network.
    This request happens automatically and is not being done by the user.
    """
    print('New transaction is being added to the transaction pool')

    posted_transaction = json.loads(request.data)

    transaction = convert_to_transaction(posted_transaction)

    if transaction.verify():
        blockchain.add_transaction(transaction)
        print('The transaction was successfully added')

        return "Transaction was successfully submitted", 201

    else:
        print('The transaction is not valid')
        return "The transaction is not valid", 400



@app.route('/transactions/post', methods=['POST'])
def post_transaction():
    """
    Spread the transaction among the network. This request is done by the user of the blockchain.
    """
    global blockchain
    data = json.loads(request.data)
    recipient = data['address']
    value = data['value']
    is_username = data['is_username']
    print('What happens with value? {}'.format(value))
    print("What happends with the address {}".format(recipient))
    print('what about username ? {}'.format(is_username))

    # check if the user is submitting transaction posting a username instead of address
    if is_username:
        response = requests.get(get_address(connector[0], connector[1]) + '/nodes/address/' + recipient)

        if response.status_code == 200:
            recipient = response.json()

        else:
            return "Invalid username", 409

    transaction = wallet.pay(recipient, value)

    blockchain.add_transaction(transaction)
    try:
        for key, value in neighbors.items():
            node_destination = get_address(value[0], value[1])
            requests.post(node_destination + '/transactions/update', data=json.dumps(transaction.to_json()))

        return "Transaction was submitted", 201
    except:

        return "The transaction is invalid", 409





@app.route('/blockchain/get', methods=['GET'])
def get_blockchain():
    json_chain = blockchain.to_json()
    print('Somebody has asked for my blockchain')

    return jsonify(json_chain), 200


@app.route('/blockchain/post', methods=['POST'])
def post_blockchain():
    global blockchain
    posted_blockchain = json.loads(request.data)
    print('This is what I got {}'.format(posted_blockchain))
    new_blockchain = Blockchain(posted_blockchain)
    print("{}: Demand to change my blockchain".format(request))
    valid_blockchain = new_blockchain.check_blockchain()
    longer_blockchain = new_blockchain.size() > blockchain.size()
    print("The validity of the blockchain {}".format(valid_blockchain))
    print("The blockchain is longer than mine {}".format(longer_blockchain))
    if longer_blockchain and valid_blockchain:
        blockchain = new_blockchain

        return "The blockchain has been updated", 201
    else:
        message = {'message': 'Your blockchain is either invalid or smaller than mine',
                   'blockchain': blockchain.to_json()}

        print('My blockchain size is now {}'.format(blockchain.size()))

        return jsonify(message), 409

@app.route('/blockchain/mine', methods=['GET'])
def run_miner():
    global blockchain
    """
    Any models in the network can become a miner and start mining blocks.
    :return:
    """
    miner = Miner(blockchain, wallet.get_address())
    new_block = miner.run_mining()
    blockchain.add_block(new_block)
    print('The blockchain is valid {}'.format(blockchain.check_blockchain()))
    print("{} models has mined a new block".format(id))
    print('New size of the blockchain is {}'.format(blockchain.size()))

    for key, value in neighbors.items():
        recipient = 'http://{}:{}/blockchain/post'.format(value[0], value[1])
        # send the new chain to all the miners
        print("sending ")
        requests.post(recipient, data=json.dumps(blockchain.to_json()))

    return 'The block was created', 200




#####################################################
# These are the helper functions for the routes


def collect_neighbors():
    """
    This function searches for the peers in the network.
    """
    global neighbors
    response = requests.get('http://{}:{}/nodes'.format(connector[0], connector[1]))
    if response.status_code == 200:
        peers = response.json()
        print("Node {} now has the following neighbors {}".format(id, peers))
        neighbors = peers
        if id in neighbors:
            del neighbors[id]


    else:
        print('Could not get neighbors, something has happened to the server')


def self_register():
    """
    This function is registering the models in the network.
    """
    data = {'id': id, 'address': ip_address, 'port': port, 'public_key': wallet.get_public_key()}
    response = requests.post("http://{}:{}/nodes".format(connector[0], connector[1]), data=json.dumps(data))

    if response.status_code == 200:
        print("{}: Successfully registered".format(id))


def get_updated():
    """
    Checks if somebody in the peers has a better blockchain
    :return:
    """
    global blockchain
    best_blockchain = blockchain
    for key, value in neighbors.items():
        node_destination = get_address(value[0], value[1])
        response = requests.get(node_destination + '/blockchain/get')

        if response.status_code == 200:
            peer_blockchain = Blockchain(response.json())

            if peer_blockchain.check_blockchain() and peer_blockchain.size() > best_blockchain.size():
                best_blockchain = peer_blockchain

    print('My blockchain size is now {}'.format(blockchain.size()))




################################################
# This is the main function that starts the application

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        ip_address = sys.argv[1]
        port = sys.argv[2]
        id = sys.argv[3]
    else:
        print("Illegal argument, cant start the models")
        sys.exit(0)

    # Creates its wallet
    wallet = Wallet(blockchain)

    # Node collects all the neighbors in the P2P network
    collect_neighbors()

    # Node registers itself in the P2P network
    self_register()

    # Node mines genesis if it is a first node in the network
    blockchain.mine_genesis()



    get_updated()
    app.run(host=ip_address, port=port)
